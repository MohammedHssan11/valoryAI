$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not $env:JWT_SECRET) {
    $env:JWT_SECRET = "valorai-local-docker-validation-secret-2026"
}
if (-not $env:JWT_ISSUER) {
    $env:JWT_ISSUER = "valorai"
}
if (-not $env:JWT_AUDIENCE) {
    $env:JWT_AUDIENCE = "valorai-api"
}

function ConvertTo-Base64Url {
    param([byte[]]$Bytes)
    return [Convert]::ToBase64String($Bytes).TrimEnd("=").Replace("+", "-").Replace("/", "_")
}

function New-ValidationJwt {
    param([string]$Subject)

    $now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $header = ConvertTo-Base64Url ([Text.Encoding]::UTF8.GetBytes('{"alg":"HS256","typ":"JWT"}'))
    $payload = ConvertTo-Base64Url ([Text.Encoding]::UTF8.GetBytes((@{
        sub = $Subject
        name = "Docker Tool Validation"
        iat = $now
        exp = $now + 3600
        iss = $env:JWT_ISSUER
        aud = $env:JWT_AUDIENCE
    } | ConvertTo-Json -Compress)))
    $unsigned = "$header.$payload"
    $hmac = [System.Security.Cryptography.HMACSHA256]::new([Text.Encoding]::UTF8.GetBytes($env:JWT_SECRET))
    try {
        $signature = ConvertTo-Base64Url ($hmac.ComputeHash([Text.Encoding]::UTF8.GetBytes($unsigned)))
    }
    finally {
        $hmac.Dispose()
    }
    return "$unsigned.$signature"
}

function Invoke-JsonRequest {
    param(
        [string]$Method,
        [string]$Uri,
        [hashtable]$Headers = @{},
        [hashtable]$Body
    )

    $params = @{
        Method = $Method
        Uri = $Uri
        Headers = $Headers
        ContentType = "application/json"
    }
    if ($null -ne $Body) {
        $params.Body = ($Body | ConvertTo-Json -Depth 20)
    }
    Invoke-RestMethod @params
}

function Wait-Backend {
    for ($attempt = 1; $attempt -le 60; $attempt++) {
        try {
            Invoke-RestMethod -Method GET -Uri "http://localhost:8000/health/ready" | Out-Null
            return
        }
        catch {
            Start-Sleep -Seconds 2
        }
    }
    throw "Backend did not become ready within 120 seconds."
}

docker compose up -d --build db db-bootstrap backend
Wait-Backend

$baseUrl = "http://localhost:8000/v1/copilot"
$subject = "tools-$([guid]::NewGuid())"
$headers = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject $subject)" }
$otherHeaders = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject "other-$subject")" }
$workspace = Invoke-JsonRequest -Method POST -Uri "$baseUrl/workspaces" -Headers $headers -Body @{
    name = "Docker Tool Workspace"
}
$property = Invoke-JsonRequest -Method POST -Uri "$baseUrl/properties" -Headers $headers -Body @{
    workspace_id = $workspace.id
    label = "Property A"
    location = "Mivida"
    area = 220
    bedrooms = 4
    bathrooms = 3
    amenities = @{ codes = @("BA", "SE") }
    valuation_inputs = @{
        lat = 30.00575065612793
        lng = 31.533998489379883
        compound_name = "Mivida"
    }
}
$scenario = Invoke-JsonRequest -Method POST -Uri "$baseUrl/scenarios" -Headers $headers -Body @{
    property_state_id = $property.id
    name = "Expanded Property"
    modifications = @{ size_sqm = 230 }
}
$baseValuation = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/valuation" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
}
$scenarioValuation = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/valuation" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    scenario_id = $scenario.id
}
$explainability = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/explainability" -Headers $headers -Body @{
    workspace_id = $workspace.id
    valuation_id = $scenarioValuation.valuation_id
}
$mlFallbackProperty = Invoke-JsonRequest -Method POST -Uri "$baseUrl/properties" -Headers $headers -Body @{
    workspace_id = $workspace.id
    label = "ML Fallback Property"
    location = "Central Cairo"
    area = 150
    bedrooms = 3
    bathrooms = 2
    amenities = @{ codes = @("BA", "SE") }
    valuation_inputs = @{
        lat = 30.0444
        lng = 31.2357
        target_price_egp = 30000
    }
}
$mlFallbackValuation = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/valuation" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $mlFallbackProperty.id
}
$mlFallbackExplainability = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/explainability" -Headers $headers -Body @{
    workspace_id = $workspace.id
    valuation_id = $mlFallbackValuation.valuation_id
}
$events = Invoke-JsonRequest -Method GET -Uri "$baseUrl/workspaces/$($workspace.id)/tool-events" -Headers $headers

$tenantIsolationStatus = 0
try {
    Invoke-WebRequest -Method POST -Uri "$baseUrl/tools/valuation" -Headers $otherHeaders -ContentType "application/json" -Body (@{
        workspace_id = $workspace.id
        property_id = $property.id
    } | ConvertTo-Json) | Out-Null
}
catch {
    $tenantIsolationStatus = [int]$_.Exception.Response.StatusCode
}

docker compose restart backend
Wait-Backend
$afterBackendRestart = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/explainability" -Headers $headers -Body @{
    workspace_id = $workspace.id
    valuation_id = $scenarioValuation.valuation_id
}

docker compose restart db backend
Wait-Backend
$afterPostgresRestartEvents = Invoke-JsonRequest -Method GET -Uri "$baseUrl/workspaces/$($workspace.id)/tool-events" -Headers $headers
$scenarioEvent = $events | Where-Object {
    $_.tool_name -eq "valuation" -and $_.payload.request.scenario_id -eq $scenario.id
} | Select-Object -First 1

$result = [ordered]@{
    workspace_id = $workspace.id
    property_id = $property.id
    scenario_id = $scenario.id
    base_valuation_id = $baseValuation.valuation_id
    scenario_valuation_id = $scenarioValuation.valuation_id
    base_source = $baseValuation.source
    scenario_source = $scenarioValuation.source
    base_engine = $baseValuation.engine_used
    scenario_engine = $scenarioValuation.engine_used
    scenario_routing_reason = $scenarioValuation.routing_reason
    scenario_router_size_sqm = $scenarioEvent.payload.request.router_request.size_sqm
    explainability_summary_present = [bool]$explainability.summary
    explainability_fairness_present = [bool]$explainability.fairness_status
    explainability_feature_drivers_count = @($explainability.feature_drivers).Count
    explainability_comparable_evidence_count = @($explainability.comparable_evidence).Count
    ml_fallback_engine = $mlFallbackValuation.engine_used
    ml_fallback_reason = $mlFallbackValuation.routing_reason
    ml_fallback_explainability_summary_present = [bool]$mlFallbackExplainability.summary
    ml_fallback_feature_drivers_count = @($mlFallbackExplainability.feature_drivers).Count
    tenant_isolation_status = $tenantIsolationStatus
    tool_events_before_restart = @($events).Count
    explainability_after_backend_restart = ($afterBackendRestart.valuation_id -eq $scenarioValuation.valuation_id)
    tool_events_after_postgres_restart = @($afterPostgresRestartEvents).Count
}

if (
    $result.base_source -ne "TruthLayer" -or
    $result.scenario_source -ne "TruthLayer" -or
    $result.base_engine -ne "CMT" -or
    $result.scenario_engine -ne "CMT" -or
    $result.scenario_routing_reason -ne "GoldilocksZone" -or
    $result.scenario_router_size_sqm -ne 230 -or
    -not $result.explainability_summary_present -or
    -not $result.explainability_fairness_present -or
    $result.explainability_comparable_evidence_count -lt 1 -or
    $result.ml_fallback_engine -ne "ML" -or
    $result.ml_fallback_reason -ne "Fallback_CMT_Failure" -or
    -not $result.ml_fallback_explainability_summary_present -or
    $result.ml_fallback_feature_drivers_count -lt 1 -or
    $result.tenant_isolation_status -ne 404 -or
    $result.tool_events_before_restart -lt 5 -or
    -not $result.explainability_after_backend_restart -or
    $result.tool_events_after_postgres_restart -lt 6
) {
    $result | ConvertTo-Json
    throw "Copilot tools Docker validation failed."
}

$result | ConvertTo-Json
