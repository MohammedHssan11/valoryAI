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
        name = "Broker Adapter Docker Validation"
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

$directRouteReferences = @(
    Get-ChildItem -Path "backend/app/broker" -Recurse -Filter "*.py" |
        Select-String -Pattern "pricing_routes|rent_fair_price\("
)
if ($directRouteReferences.Count -ne 0) {
    throw "Broker adapter still contains a direct pricing route reference."
}

docker compose up -d --build db db-bootstrap backend
Wait-Backend

$copilotUrl = "http://localhost:8000/v1/copilot"
$brokerUrl = "http://localhost:8000/v1/broker"
$subject = "broker-adapter-$([guid]::NewGuid())"
$headers = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject $subject)" }
$otherHeaders = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject "other-$subject")" }

$workspace = Invoke-JsonRequest -Method POST -Uri "$copilotUrl/workspaces" -Headers $headers -Body @{
    name = "Broker Adapter Docker Workspace"
}
$property = Invoke-JsonRequest -Method POST -Uri "$copilotUrl/properties" -Headers $headers -Body @{
    workspace_id = $workspace.id
    label = "Mivida Broker Property"
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
$baseScenario = Invoke-JsonRequest -Method POST -Uri "$copilotUrl/scenarios" -Headers $headers -Body @{
    property_state_id = $property.id
    name = "Broker Base Scenario"
    modifications = @{}
}
$expandedScenario = Invoke-JsonRequest -Method POST -Uri "$copilotUrl/scenarios" -Headers $headers -Body @{
    property_state_id = $property.id
    parent_scenario_id = $baseScenario.id
    name = "Broker Expanded Scenario"
    modifications = @{ size_sqm = 230 }
}

# The legacy request remains accepted as a trigger, but workspace state is authoritative.
$legacyTrigger = @{
    lat = 30.00575065612793
    lng = 31.533998489379883
    property_type = "Apartment"
    bedrooms = 4
    bathrooms = 3
    size_sqm = 111
}

$baseSessionId = "broker-base-$([guid]::NewGuid().ToString('N').Substring(0, 10))"
$baseBroker = Invoke-JsonRequest -Method POST -Uri "$brokerUrl/chat" -Headers $headers -Body @{
    session_id = $baseSessionId
    workspace_id = $workspace.id
    scenario_id = $baseScenario.id
    message = "Run the broker valuation analysis for this workspace property."
    valuation_request = $legacyTrigger
}
$explanationBroker = Invoke-JsonRequest -Method POST -Uri "$brokerUrl/chat" -Headers $headers -Body @{
    session_id = $baseSessionId
    workspace_id = $workspace.id
    scenario_id = $baseScenario.id
    message = "Explain why this valuation was returned and show the grounded evidence."
    valuation_request = $legacyTrigger
}

$scenarioSessionId = "broker-scenario-$([guid]::NewGuid().ToString('N').Substring(0, 10))"
$scenarioBroker = Invoke-JsonRequest -Method POST -Uri "$brokerUrl/chat" -Headers $headers -Body @{
    session_id = $scenarioSessionId
    workspace_id = $workspace.id
    scenario_id = $expandedScenario.id
    message = "Run the expanded scenario valuation."
    valuation_request = $legacyTrigger
}

$workspaceContext = Invoke-JsonRequest -Method GET -Uri "$brokerUrl/session/$baseSessionId" -Headers $headers
$eventsBeforeRestart = Invoke-JsonRequest -Method GET -Uri "$copilotUrl/workspaces/$($workspace.id)/tool-events" -Headers $headers
$scenarioEvent = $eventsBeforeRestart | Where-Object {
    $_.tool_name -eq "valuation" -and $_.payload.request.scenario_id -eq $expandedScenario.id
} | Select-Object -Last 1

$tenantIsolationStatus = 0
try {
    Invoke-WebRequest -Method GET -Uri "$brokerUrl/session/$baseSessionId" -Headers $otherHeaders | Out-Null
}
catch {
    $tenantIsolationStatus = [int]$_.Exception.Response.StatusCode
}

docker compose restart backend
Wait-Backend

$recoveredContext = Invoke-JsonRequest -Method GET -Uri "$brokerUrl/session/$baseSessionId" -Headers $headers
$afterRestartBroker = Invoke-JsonRequest -Method POST -Uri "$brokerUrl/chat" -Headers $headers -Body @{
    session_id = $baseSessionId
    workspace_id = $workspace.id
    scenario_id = $baseScenario.id
    message = "Explain the recovered valuation context after restart."
    valuation_request = $legacyTrigger
}
$eventsAfterRestart = Invoke-JsonRequest -Method GET -Uri "$copilotUrl/workspaces/$($workspace.id)/tool-events" -Headers $headers

$baseToolNames = @($baseBroker.data.tool_results | ForEach-Object { $_.tool_name })
$explanationToolNames = @($explanationBroker.data.tool_results | ForEach-Object { $_.tool_name })
$scenarioToolNames = @($scenarioBroker.data.tool_results | ForEach-Object { $_.tool_name })
$afterRestartToolNames = @($afterRestartBroker.data.tool_results | ForEach-Object { $_.tool_name })
$expectedToolNames = @("valuation_analysis", "explainability")

$result = [ordered]@{
    workspace_id = $workspace.id
    property_id = $property.id
    base_scenario_id = $baseScenario.id
    expanded_scenario_id = $expandedScenario.id
    broker_valuation_degraded = $baseBroker.data.degraded_mode
    broker_valuation_grounding = $baseBroker.data.grounding.status
    broker_valuation_source = $baseBroker.data.response.authoritative_values.source
    broker_valuation_tool_names = $baseToolNames
    broker_explainability_degraded = $explanationBroker.data.degraded_mode
    broker_explainability_source = $explanationBroker.data.context.explainability.source
    broker_explainability_summary_present = [bool]$explanationBroker.data.context.explainability.summary
    broker_explainability_tool_names = $explanationToolNames
    scenario_valuation_degraded = $scenarioBroker.data.degraded_mode
    scenario_router_size_sqm = $scenarioEvent.payload.request.router_request.size_sqm
    scenario_tool_names = $scenarioToolNames
    workspace_context_session_id = $workspaceContext.data.session_id
    workspace_context_workspace_id = $workspaceContext.data.workspace_id
    workspace_context_scenario_id = $workspaceContext.data.scenario_id
    tenant_isolation_status = $tenantIsolationStatus
    restart_session_retrieved = ($recoveredContext.data.session_id -eq $baseSessionId)
    restart_broker_degraded = $afterRestartBroker.data.degraded_mode
    restart_tool_names = $afterRestartToolNames
    tool_events_before_restart = @($eventsBeforeRestart).Count
    tool_events_after_restart = @($eventsAfterRestart).Count
    direct_pricing_route_references = $directRouteReferences.Count
}

if (
    $result.broker_valuation_degraded -or
    $result.broker_valuation_grounding -ne "passed" -or
    $result.broker_valuation_source -ne "TruthLayer" -or
    (Compare-Object $baseToolNames $expectedToolNames -SyncWindow 0) -or
    $result.broker_explainability_degraded -or
    $result.broker_explainability_source -ne "TruthLayer" -or
    -not $result.broker_explainability_summary_present -or
    (Compare-Object $explanationToolNames $expectedToolNames -SyncWindow 0) -or
    $result.scenario_valuation_degraded -or
    $result.scenario_router_size_sqm -ne 230 -or
    (Compare-Object $scenarioToolNames $expectedToolNames -SyncWindow 0) -or
    $result.workspace_context_session_id -ne $baseSessionId -or
    $result.workspace_context_workspace_id -ne $workspace.id -or
    $result.workspace_context_scenario_id -ne $baseScenario.id -or
    $result.tenant_isolation_status -ne 404 -or
    -not $result.restart_session_retrieved -or
    $result.restart_broker_degraded -or
    (Compare-Object $afterRestartToolNames $expectedToolNames -SyncWindow 0) -or
    $result.tool_events_before_restart -lt 6 -or
    $result.tool_events_after_restart -lt 8 -or
    $result.direct_pricing_route_references -ne 0
) {
    $result | ConvertTo-Json -Depth 10
    throw "Broker adapter Docker validation failed."
}

$result | ConvertTo-Json -Depth 10
