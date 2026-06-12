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
        name = "Docker Investment Validation"
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

function Test-ForbiddenMetricField {
    param([object]$Value)

    if ($null -eq $Value) {
        return $false
    }
    if ($Value -is [string] -or $Value -is [ValueType]) {
        return $false
    }
    if ($Value -is [System.Collections.IDictionary]) {
        foreach ($key in $Value.Keys) {
            if ([string]$key -match "^(roi|irr|cagr|appreciation_forecast|future_price_prediction|rental_yield|investment_returns)$") {
                return $true
            }
            if (Test-ForbiddenMetricField -Value $Value[$key]) {
                return $true
            }
        }
        return $false
    }
    if ($Value -is [System.Collections.IEnumerable]) {
        foreach ($item in $Value) {
            if (Test-ForbiddenMetricField -Value $item) {
                return $true
            }
        }
        return $false
    }
    foreach ($property in $Value.PSObject.Properties) {
        if ($property.Name -match "^(roi|irr|cagr|appreciation_forecast|future_price_prediction|rental_yield|investment_returns)$") {
            return $true
        }
        if (Test-ForbiddenMetricField -Value $property.Value) {
            return $true
        }
    }
    return $false
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
$subject = "investment-$([guid]::NewGuid())"
$headers = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject $subject)" }
$otherHeaders = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject "other-$subject")" }

$workspace = Invoke-JsonRequest -Method POST -Uri "$baseUrl/workspaces" -Headers $headers -Body @{
    name = "Docker Investment Workspace"
}
$property = Invoke-JsonRequest -Method POST -Uri "$baseUrl/properties" -Headers $headers -Body @{
    workspace_id = $workspace.id
    label = "Mivida Docker Investment Property"
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
$sparseProperty = Invoke-JsonRequest -Method POST -Uri "$baseUrl/properties" -Headers $headers -Body @{
    workspace_id = $workspace.id
    label = "Sparse Central Cairo Docker Investment Property"
    location = "Central Cairo"
    area = 150
    bedrooms = 3
    bathrooms = 2
    amenities = @{ codes = @("BA") }
    valuation_inputs = @{
        lat = 30.0444
        lng = 31.2357
    }
}
$scenario = Invoke-JsonRequest -Method POST -Uri "$baseUrl/scenarios" -Headers $headers -Body @{
    property_state_id = $property.id
    name = "Expanded Mivida Investment Scenario"
    modifications = @{ size_sqm = 230 }
}
$baseValuation = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/valuation" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
}
$sparseValuation = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/valuation" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $sparseProperty.id
}
$scenarioValuation = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/valuation" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    scenario_id = $scenario.id
}

$strongTarget = [Math]::Max(1, [int]$baseValuation.price_range.low - 1)
$moderateTarget = [Math]::Max(1, [int]$sparseValuation.price_range.low - 1)
$fairTarget = [int]$baseValuation.fair_price
$cautionTarget = [int]$baseValuation.fair_price + 1
$highRiskTarget = [int]$baseValuation.price_range.high + 1
$scenarioHighRiskTarget = [int]$scenarioValuation.price_range.high + 1

$strongInvestment = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/investment" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    asking_price_egp = $strongTarget
}
$moderateInvestment = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/investment" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $sparseProperty.id
    asking_price_egp = $moderateTarget
}
$fairInvestment = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/investment" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    asking_price_egp = $fairTarget
}
$cautionInvestment = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/investment" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    asking_price_egp = $cautionTarget
}
$highRiskInvestment = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/investment" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    asking_price_egp = $highRiskTarget
}
$scenarioInvestment = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/investment" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    scenario_id = $scenario.id
    asking_price_egp = $scenarioHighRiskTarget
    what_if_modifications = @{ bathrooms = 4 }
}
$whatIf = $scenarioInvestment.what_if_summary.analysis

$eventsBeforeRestart = Invoke-JsonRequest -Method GET -Uri "$baseUrl/workspaces/$($workspace.id)/tool-events" -Headers $headers
$highRiskChildEvents = @($eventsBeforeRestart | Where-Object {
    $_.payload.response.valuation_id -eq $highRiskInvestment.valuation_id -and
    $_.tool_name -in @("valuation", "explainability", "comparable", "fairness", "negotiation", "investment")
})
$highRiskAuditEvent = $eventsBeforeRestart | Where-Object {
    $_.tool_name -eq "investment" -and $_.payload.response.valuation_id -eq $highRiskInvestment.valuation_id
} | Select-Object -First 1
$scenarioValuationEvent = $eventsBeforeRestart | Where-Object {
    $_.tool_name -eq "valuation" -and $_.payload.response.valuation_id -eq $scenarioInvestment.valuation_id
} | Select-Object -First 1

$tenantIsolationStatus = 0
try {
    Invoke-WebRequest -Method POST -Uri "$baseUrl/tools/investment" -Headers $otherHeaders -ContentType "application/json" -Body (@{
        workspace_id = $workspace.id
        property_id = $property.id
        scenario_id = $scenario.id
        asking_price_egp = $scenarioHighRiskTarget
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
$investmentAfterBackendRestart = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/investment" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    asking_price_egp = $fairTarget
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

$allInvestments = @(
    $strongInvestment,
    $moderateInvestment,
    $fairInvestment,
    $cautionInvestment,
    $highRiskInvestment,
    $scenarioInvestment
)
$allStrengthsTraceable = @(
    $allInvestments |
        ForEach-Object { @($_.strengths) } |
        Where-Object { @($_.evidence).Count -eq 0 }
).Count -eq 0
$allRisksTraceable = @(
    $allInvestments |
        ForEach-Object { @($_.risks) } |
        Where-Object { @($_.evidence).Count -eq 0 }
).Count -eq 0
$allPositionsTraceable = @(
    $allInvestments |
        Where-Object { @($_.investment_position_evidence).Count -eq 0 }
).Count -eq 0
$forbiddenMetricFields = @(
    $allInvestments |
        Where-Object { Test-ForbiddenMetricField -Value $_ }
).Count
$highRiskAllowedPrices = @($highRiskInvestment.comparable_summary.observed_prices) + @([int]$highRiskInvestment.fair_price)
$highRiskOfferLowGrounded = $highRiskAllowedPrices -contains [int]$highRiskInvestment.negotiation_summary.recommended_offer_band.low
$highRiskOfferHighGrounded = $highRiskAllowedPrices -contains [int]$highRiskInvestment.negotiation_summary.recommended_offer_band.high

$result = [ordered]@{
    workspace_id = $workspace.id
    property_id = $property.id
    sparse_property_id = $sparseProperty.id
    scenario_id = $scenario.id
    strong_valuation_id = $strongInvestment.valuation_id
    moderate_valuation_id = $moderateInvestment.valuation_id
    fair_valuation_id = $fairInvestment.valuation_id
    caution_valuation_id = $cautionInvestment.valuation_id
    high_risk_valuation_id = $highRiskInvestment.valuation_id
    scenario_valuation_id = $scenarioInvestment.valuation_id
    strong_position = $strongInvestment.investment_position
    moderate_position = $moderateInvestment.investment_position
    fair_position = $fairInvestment.investment_position
    caution_position = $cautionInvestment.investment_position
    high_risk_position = $highRiskInvestment.investment_position
    strong_confidence = $strongInvestment.confidence_level
    strong_comparable_count = $strongInvestment.comparable_summary.comparable_count
    moderate_confidence = $moderateInvestment.confidence_level
    moderate_comparable_count = $moderateInvestment.comparable_summary.comparable_count
    high_risk_price_gap_valid = ($highRiskInvestment.price_gap -eq ($highRiskInvestment.asking_price - $highRiskInvestment.fair_price))
    high_risk_offer_endpoints_grounded = ($highRiskOfferLowGrounded -and $highRiskOfferHighGrounded)
    no_what_if_status = $strongInvestment.what_if_summary.status
    no_what_if_source = $strongInvestment.what_if_summary.source
    what_if_status = $scenarioInvestment.what_if_summary.status
    what_if_source = $scenarioInvestment.what_if_summary.source
    what_if_scenario_grounded = ($whatIf.scenario_valuation_id -ne $whatIf.base_valuation_id)
    scenario_router_size_sqm = $scenarioValuationEvent.payload.request.router_request.size_sqm
    scenario_audit_state_id = ($eventsBeforeRestart | Where-Object {
        $_.tool_name -eq "investment" -and $_.payload.response.valuation_id -eq $scenarioInvestment.valuation_id
    } | Select-Object -First 1).scenario_state_id
    all_strengths_traceable = $allStrengthsTraceable
    all_risks_traceable = $allRisksTraceable
    all_positions_traceable = $allPositionsTraceable
    forbidden_metric_fields = $forbiddenMetricFields
    same_snapshot_child_tools = ((@($highRiskChildEvents | ForEach-Object { $_.tool_name }) -join ",") -eq "valuation,explainability,comparable,fairness,negotiation,investment")
    audit_asking_price_egp = $highRiskAuditEvent.payload.request.asking_price_egp
    audit_investment_position = $highRiskAuditEvent.payload.response.investment_position
    tenant_isolation_status = $tenantIsolationStatus
    investment_events_before_restart = @($eventsBeforeRestart | Where-Object { $_.tool_name -eq "investment" }).Count
    investment_events_after_postgres_restart = @($eventsAfterPostgresRestart | Where-Object { $_.tool_name -eq "investment" }).Count
    restart_investment_source = $investmentAfterBackendRestart.source
    forbidden_tool_logic_references = $toolLogicReferences.Count
}

if (
    $result.strong_position -ne "Strong Opportunity" -or
    $result.moderate_position -ne "Moderate Opportunity" -or
    $result.fair_position -ne "Fairly Priced" -or
    $result.caution_position -ne "Caution" -or
    $result.high_risk_position -ne "High Risk" -or
    $result.strong_confidence -ne "High" -or
    $result.strong_comparable_count -lt 1 -or
    $result.moderate_confidence -ne "Low" -or
    $result.moderate_comparable_count -ne 0 -or
    -not $result.high_risk_price_gap_valid -or
    -not $result.high_risk_offer_endpoints_grounded -or
    $result.no_what_if_status -ne "Insufficient Evidence" -or
    $result.no_what_if_source -ne "Insufficient Evidence" -or
    $result.what_if_status -ne "Available" -or
    $result.what_if_source -ne "TruthLayer" -or
    -not $result.what_if_scenario_grounded -or
    $result.scenario_router_size_sqm -ne 230 -or
    $result.scenario_audit_state_id -ne $scenario.id -or
    -not $result.all_strengths_traceable -or
    -not $result.all_risks_traceable -or
    -not $result.all_positions_traceable -or
    $result.forbidden_metric_fields -ne 0 -or
    -not $result.same_snapshot_child_tools -or
    $result.audit_asking_price_egp -ne $highRiskTarget -or
    $result.audit_investment_position -ne "High Risk" -or
    $result.tenant_isolation_status -ne 404 -or
    $result.investment_events_before_restart -ne 6 -or
    $result.investment_events_after_postgres_restart -lt 7 -or
    $result.restart_investment_source -ne "TruthLayer" -or
    $result.forbidden_tool_logic_references -ne 0
) {
    $result | ConvertTo-Json -Depth 20
    throw "Copilot Investment Docker validation failed."
}

$result | ConvertTo-Json -Depth 20
