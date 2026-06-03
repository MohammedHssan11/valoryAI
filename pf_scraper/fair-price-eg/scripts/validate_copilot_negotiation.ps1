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
        name = "Docker Negotiation Validation"
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
        $params.Body = ($Body | ConvertTo-Json -Depth 30)
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
if ($toolLogicReferences.Count -ne 0) {
    throw "Static TruthLayer boundary scan failed."
}

docker compose up -d --build db db-bootstrap backend
if ($LASTEXITCODE -ne 0) {
    throw "Docker stack build failed."
}
Wait-Backend

$baseUrl = "http://localhost:8000/v1/copilot"
$subject = "negotiation-$([guid]::NewGuid())"
$headers = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject $subject)" }
$otherHeaders = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject "other-$subject")" }

$workspace = Invoke-JsonRequest -Method POST -Uri "$baseUrl/workspaces" -Headers $headers -Body @{
    name = "Docker Negotiation Workspace"
}
$property = Invoke-JsonRequest -Method POST -Uri "$baseUrl/properties" -Headers $headers -Body @{
    workspace_id = $workspace.id
    label = "Mivida Docker Negotiation Property"
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
    name = "Expanded Mivida Negotiation Scenario"
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

$belowTarget = [Math]::Max(1, [int]$baseValuation.price_range.low - 1)
$withinTarget = [int]$baseValuation.fair_price
$aboveTarget = [int]$baseValuation.price_range.high + 1
$scenarioAboveTarget = [int]$scenarioValuation.price_range.high + 1

$belowNegotiation = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/negotiation" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    asking_price_egp = $belowTarget
}
$withinNegotiation = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/negotiation" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    asking_price_egp = $withinTarget
}
$aboveNegotiation = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/negotiation" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    asking_price_egp = $aboveTarget
}
$scenarioNegotiation = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/negotiation" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    scenario_id = $scenario.id
    asking_price_egp = $scenarioAboveTarget
    what_if_modifications = @{ bathrooms = 4 }
}
$whatIf = $scenarioNegotiation.what_if_analysis

$eventsBeforeRestart = Invoke-JsonRequest -Method GET -Uri "$baseUrl/workspaces/$($workspace.id)/tool-events" -Headers $headers
$aboveChildEvents = @($eventsBeforeRestart | Where-Object {
    $_.payload.response.valuation_id -eq $aboveNegotiation.valuation_id -and
    $_.tool_name -in @("valuation", "explainability", "comparable", "fairness")
})
$aboveValuationEvent = $aboveChildEvents | Where-Object { $_.tool_name -eq "valuation" } | Select-Object -First 1
$aboveFairnessEvent = $aboveChildEvents | Where-Object { $_.tool_name -eq "fairness" } | Select-Object -First 1
$aboveAuditEvent = $eventsBeforeRestart | Where-Object {
    $_.tool_name -eq "negotiation" -and $_.payload.response.valuation_id -eq $aboveNegotiation.valuation_id
} | Select-Object -First 1
$scenarioValuationEvent = $eventsBeforeRestart | Where-Object {
    $_.tool_name -eq "valuation" -and $_.payload.response.valuation_id -eq $scenarioNegotiation.valuation_id
} | Select-Object -First 1

$tenantIsolationStatus = 0
try {
    Invoke-WebRequest -Method POST -Uri "$baseUrl/tools/negotiation" -Headers $otherHeaders -ContentType "application/json" -Body (@{
        workspace_id = $workspace.id
        property_id = $property.id
        scenario_id = $scenario.id
        asking_price_egp = $scenarioAboveTarget
    } | ConvertTo-Json) | Out-Null
}
catch {
    $tenantIsolationStatus = [int]$_.Exception.Response.StatusCode
}

docker compose restart backend
if ($LASTEXITCODE -ne 0) {
    throw "Backend restart failed."
}
Wait-Backend
$negotiationAfterBackendRestart = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/negotiation" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    asking_price_egp = $withinTarget
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

$aboveAllowedPrices = @($aboveNegotiation.comparable_summary.observed_prices) + @([int]$aboveNegotiation.fair_price)
$aboveEndpointLowAllowed = $aboveAllowedPrices -contains [int]$aboveNegotiation.recommended_offer_band.low
$aboveEndpointHighAllowed = $aboveAllowedPrices -contains [int]$aboveNegotiation.recommended_offer_band.high
$allTalkingPointsTraceable = @(
    $aboveNegotiation.broker_talking_points | Where-Object { @($_.evidence).Count -eq 0 }
).Count -eq 0
$allRiskNotesTraceable = @(
    @($aboveNegotiation.risk_notes) + @($scenarioNegotiation.risk_notes) |
        Where-Object { @($_.evidence).Count -eq 0 }
).Count -eq 0
$allPositionsTraceable = @(
    @($belowNegotiation, $withinNegotiation, $aboveNegotiation, $scenarioNegotiation) |
        Where-Object { @($_.negotiation_position_evidence).Count -eq 0 }
).Count -eq 0
$result = [ordered]@{
    workspace_id = $workspace.id
    property_id = $property.id
    scenario_id = $scenario.id
    below_valuation_id = $belowNegotiation.valuation_id
    within_valuation_id = $withinNegotiation.valuation_id
    above_valuation_id = $aboveNegotiation.valuation_id
    scenario_valuation_id = $scenarioNegotiation.valuation_id
    below_fairness_status = $belowNegotiation.fairness_status
    within_fairness_status = $withinNegotiation.fairness_status
    above_fairness_status = $aboveNegotiation.fairness_status
    below_negotiation_position = $belowNegotiation.negotiation_position
    within_negotiation_position = $withinNegotiation.negotiation_position
    above_negotiation_position = $aboveNegotiation.negotiation_position
    below_offer_band_is_empty = ($null -eq $belowNegotiation.recommended_offer_band.low -and $null -eq $belowNegotiation.recommended_offer_band.high)
    within_offer_band_reuses_fair_price = (
        $withinNegotiation.recommended_offer_band.low -eq $withinNegotiation.fair_price -and
        $withinNegotiation.recommended_offer_band.high -eq $withinNegotiation.fair_price
    )
    above_offer_low = $aboveNegotiation.recommended_offer_band.low
    above_offer_high = $aboveNegotiation.recommended_offer_band.high
    above_offer_endpoints_grounded = ($aboveEndpointLowAllowed -and $aboveEndpointHighAllowed)
    above_comparable_count = $aboveNegotiation.comparable_summary.comparable_count
    above_price_gap_valid = ($aboveNegotiation.price_gap -eq ($aboveNegotiation.asking_price - $aboveNegotiation.fair_price))
    all_talking_points_traceable = $allTalkingPointsTraceable
    all_risk_notes_traceable = $allRiskNotesTraceable
    all_positions_traceable = $allPositionsTraceable
    same_snapshot_child_tools = ((@($aboveChildEvents | ForEach-Object { $_.tool_name }) -join ",") -eq "valuation,explainability,comparable,fairness")
    above_router_target_price_egp = $aboveValuationEvent.payload.request.router_request.target_price_egp
    above_fairness_reuses_valuation_id = ($aboveFairnessEvent.payload.response.valuation_id -eq $aboveNegotiation.valuation_id)
    audit_asking_price_egp = $aboveAuditEvent.payload.request.asking_price_egp
    audit_fairness_status = $aboveAuditEvent.payload.response.fairness_status
    audit_negotiation_position = $aboveAuditEvent.payload.response.negotiation_position
    scenario_router_size_sqm = $scenarioValuationEvent.payload.request.router_request.size_sqm
    what_if_source = $whatIf.source
    what_if_scenario_grounded = ($whatIf.scenario_valuation_id -ne $whatIf.base_valuation_id)
    what_if_negotiation_integrated = ($null -ne $scenarioNegotiation.what_if_analysis)
    tenant_isolation_status = $tenantIsolationStatus
    negotiation_events_before_restart = @($eventsBeforeRestart | Where-Object { $_.tool_name -eq "negotiation" }).Count
    negotiation_events_after_postgres_restart = @($eventsAfterPostgresRestart | Where-Object { $_.tool_name -eq "negotiation" }).Count
    restart_negotiation_source = $negotiationAfterBackendRestart.source
    forbidden_tool_logic_references = $toolLogicReferences.Count
}

if (
    $result.below_fairness_status -ne "Below Fair Value" -or
    $result.within_fairness_status -ne "Within Fair Value" -or
    $result.above_fairness_status -ne "Above Fair Value" -or
    $result.below_negotiation_position -ne "Strong Buy Opportunity" -or
    $result.within_negotiation_position -ne "Fair Market Position" -or
    $result.above_negotiation_position -ne "Overpriced" -or
    -not $result.below_offer_band_is_empty -or
    -not $result.within_offer_band_reuses_fair_price -or
    -not $result.above_offer_endpoints_grounded -or
    $result.above_comparable_count -lt 1 -or
    -not $result.above_price_gap_valid -or
    -not $result.all_talking_points_traceable -or
    -not $result.all_risk_notes_traceable -or
    -not $result.all_positions_traceable -or
    -not $result.same_snapshot_child_tools -or
    $result.above_router_target_price_egp -ne $aboveTarget -or
    -not $result.above_fairness_reuses_valuation_id -or
    $result.audit_asking_price_egp -ne $aboveTarget -or
    $result.audit_fairness_status -ne "Above Fair Value" -or
    $result.audit_negotiation_position -ne "Overpriced" -or
    $result.scenario_router_size_sqm -ne 230 -or
    $result.what_if_source -ne "TruthLayer" -or
    -not $result.what_if_scenario_grounded -or
    -not $result.what_if_negotiation_integrated -or
    $result.tenant_isolation_status -ne 404 -or
    $result.negotiation_events_before_restart -ne 4 -or
    $result.negotiation_events_after_postgres_restart -lt 5 -or
    $result.restart_negotiation_source -ne "TruthLayer" -or
    $result.forbidden_tool_logic_references -ne 0
) {
    $result | ConvertTo-Json -Depth 20
    throw "Copilot Negotiation Docker validation failed."
}

$result | ConvertTo-Json -Depth 20
