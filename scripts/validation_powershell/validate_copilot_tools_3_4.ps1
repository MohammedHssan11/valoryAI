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
        name = "Docker Tools 3 + 4 Validation"
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

$toolLogicReferences = @(
    Select-String -Path "backend/app/services/copilot_tools_service.py" -Pattern @(
        "weighted_median",
        "weighted_quantile",
        "price_listing_cmt",
        "price_listing_ml",
        "synthetic compar"
    )
)
$fabricatedComparableDates = @(
    Select-String -Path "backend/app/services/router_service.py" -SimpleMatch -Pattern @(
        'listing_date="Recent"',
        'listing_date = "Recent"',
        "listing_date='Recent'",
        "listing_date = 'Recent'"
    )
)
if ($toolLogicReferences.Count -ne 0 -or $fabricatedComparableDates.Count -ne 0) {
    throw "Static TruthLayer boundary scan failed."
}

docker compose up -d --build db db-bootstrap backend
if ($LASTEXITCODE -ne 0) {
    throw "Docker stack build failed."
}
Wait-Backend

$baseUrl = "http://localhost:8000/v1/copilot"
$subject = "tools-3-4-$([guid]::NewGuid())"
$headers = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject $subject)" }
$otherHeaders = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject "other-$subject")" }

$workspace = Invoke-JsonRequest -Method POST -Uri "$baseUrl/workspaces" -Headers $headers -Body @{
    name = "Docker Tools 3 + 4 Workspace"
}
$property = Invoke-JsonRequest -Method POST -Uri "$baseUrl/properties" -Headers $headers -Body @{
    workspace_id = $workspace.id
    label = "Mivida Tools 3 + 4 Property"
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
    name = "Expanded Mivida Property"
    modifications = @{ size_sqm = 230 }
}
$baseValuation = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/valuation" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
}
$baseComparable = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/comparable" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    valuation_id = $baseValuation.valuation_id
}
$scenarioComparable = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/comparable" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    scenario_id = $scenario.id
}

$belowTarget = [Math]::Max(1, [int]$baseValuation.price_range.low - 1)
$withinTarget = [int]$baseValuation.fair_price
$aboveTarget = [int]$baseValuation.price_range.high + 1
$belowFairness = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/fairness" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    target_price_egp = $belowTarget
}
$withinFairness = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/fairness" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    target_price_egp = $withinTarget
}
$aboveFairness = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/fairness" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    target_price_egp = $aboveTarget
}
$scenarioFairness = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/fairness" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    scenario_id = $scenario.id
    target_price_egp = $withinTarget
}

$eventsBeforeRestart = Invoke-JsonRequest -Method GET -Uri "$baseUrl/workspaces/$($workspace.id)/tool-events" -Headers $headers
$scenarioComparableValuationEvent = $eventsBeforeRestart | Where-Object {
    $_.tool_name -eq "valuation" -and $_.payload.response.valuation_id -eq $scenarioComparable.valuation_id
} | Select-Object -First 1
$scenarioFairnessValuationEvent = $eventsBeforeRestart | Where-Object {
    $_.tool_name -eq "valuation" -and $_.payload.response.valuation_id -eq $scenarioFairness.valuation_id
} | Select-Object -First 1
$withinFairnessValuationEvent = $eventsBeforeRestart | Where-Object {
    $_.tool_name -eq "valuation" -and $_.payload.response.valuation_id -eq $withinFairness.valuation_id
} | Select-Object -First 1

$comparableTenantIsolationStatus = 0
try {
    Invoke-WebRequest -Method POST -Uri "$baseUrl/tools/comparable" -Headers $otherHeaders -ContentType "application/json" -Body (@{
        workspace_id = $workspace.id
        property_id = $property.id
    } | ConvertTo-Json) | Out-Null
}
catch {
    $comparableTenantIsolationStatus = [int]$_.Exception.Response.StatusCode
}

$fairnessTenantIsolationStatus = 0
try {
    Invoke-WebRequest -Method POST -Uri "$baseUrl/tools/fairness" -Headers $otherHeaders -ContentType "application/json" -Body (@{
        workspace_id = $workspace.id
        property_id = $property.id
        target_price_egp = $withinTarget
    } | ConvertTo-Json) | Out-Null
}
catch {
    $fairnessTenantIsolationStatus = [int]$_.Exception.Response.StatusCode
}

docker compose restart backend
if ($LASTEXITCODE -ne 0) {
    throw "Backend restart failed."
}
Wait-Backend
$comparableAfterBackendRestart = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/comparable" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    valuation_id = $baseValuation.valuation_id
}

docker compose restart db backend
if ($LASTEXITCODE -ne 0) {
    throw "PostgreSQL restart failed."
}
Wait-Backend
$eventsAfterPostgresRestart = Invoke-JsonRequest -Method GET -Uri "$baseUrl/workspaces/$($workspace.id)/tool-events" -Headers $headers

docker compose exec -T backend python -m app.scripts.run_migrations --verify
if ($LASTEXITCODE -ne 0) {
    throw "Migration verification failed."
}

$firstComparablePropertyNames = @($baseComparable.comparables[0].PSObject.Properties.Name)
$result = [ordered]@{
    workspace_id = $workspace.id
    property_id = $property.id
    scenario_id = $scenario.id
    base_valuation_id = $baseValuation.valuation_id
    scenario_comparable_valuation_id = $scenarioComparable.valuation_id
    scenario_fairness_valuation_id = $scenarioFairness.valuation_id
    base_comparable_count = @($baseComparable.comparables).Count
    scenario_comparable_count = @($scenarioComparable.comparables).Count
    comparable_source = $baseComparable.source
    comparable_item_sources_valid = (@($baseComparable.comparables | Where-Object { $_.source -ne "TruthLayer" }).Count -eq 0)
    comparable_ids_present = (@($baseComparable.comparables | Where-Object { -not $_.comparable_id }).Count -eq 0)
    comparable_reasons_present = (@($baseComparable.comparables | Where-Object { -not $_.similarity_reason }).Count -eq 0)
    compound_name_field_present = ($firstComparablePropertyNames -contains "compound_name")
    listing_date_field_absent = -not ($firstComparablePropertyNames -contains "listing_date")
    below_fairness_status = $belowFairness.fairness_status
    within_fairness_status = $withinFairness.fairness_status
    above_fairness_status = $aboveFairness.fairness_status
    fairness_source = $withinFairness.source
    scenario_comparable_router_size_sqm = $scenarioComparableValuationEvent.payload.request.router_request.size_sqm
    scenario_fairness_router_size_sqm = $scenarioFairnessValuationEvent.payload.request.router_request.size_sqm
    fairness_router_target_price_egp = $withinFairnessValuationEvent.payload.request.router_request.target_price_egp
    comparable_tenant_isolation_status = $comparableTenantIsolationStatus
    fairness_tenant_isolation_status = $fairnessTenantIsolationStatus
    comparable_after_backend_restart = ($comparableAfterBackendRestart.valuation_id -eq $baseValuation.valuation_id)
    tool_events_before_restart = @($eventsBeforeRestart).Count
    tool_events_after_postgres_restart = @($eventsAfterPostgresRestart).Count
    comparable_events_before_restart = @($eventsBeforeRestart | Where-Object { $_.tool_name -eq "comparable" }).Count
    fairness_events_before_restart = @($eventsBeforeRestart | Where-Object { $_.tool_name -eq "fairness" }).Count
    forbidden_tool_logic_references = $toolLogicReferences.Count
    fabricated_comparable_dates = $fabricatedComparableDates.Count
}

if (
    $result.base_comparable_count -lt 1 -or
    $result.scenario_comparable_count -lt 1 -or
    $result.comparable_source -ne "TruthLayer" -or
    -not $result.comparable_item_sources_valid -or
    -not $result.comparable_ids_present -or
    -not $result.comparable_reasons_present -or
    -not $result.compound_name_field_present -or
    -not $result.listing_date_field_absent -or
    $result.below_fairness_status -ne "Below Fair Value" -or
    $result.within_fairness_status -ne "Within Fair Value" -or
    $result.above_fairness_status -ne "Above Fair Value" -or
    $result.fairness_source -ne "TruthLayer" -or
    $result.scenario_comparable_router_size_sqm -ne 230 -or
    $result.scenario_fairness_router_size_sqm -ne 230 -or
    $result.fairness_router_target_price_egp -ne $withinTarget -or
    $result.comparable_tenant_isolation_status -ne 404 -or
    $result.fairness_tenant_isolation_status -ne 404 -or
    -not $result.comparable_after_backend_restart -or
    $result.tool_events_before_restart -lt 12 -or
    $result.tool_events_after_postgres_restart -lt 13 -or
    $result.comparable_events_before_restart -lt 2 -or
    $result.fairness_events_before_restart -ne 4 -or
    $result.forbidden_tool_logic_references -ne 0 -or
    $result.fabricated_comparable_dates -ne 0
) {
    $result | ConvertTo-Json -Depth 10
    throw "Copilot Tools 3 + 4 Docker validation failed."
}

$result | ConvertTo-Json -Depth 10
