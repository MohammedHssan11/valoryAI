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
        name = "Docker What-if Validation"
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
$subject = "what-if-$([guid]::NewGuid())"
$headers = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject $subject)" }
$otherHeaders = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject "other-$subject")" }

$workspace = Invoke-JsonRequest -Method POST -Uri "$baseUrl/workspaces" -Headers $headers -Body @{
    name = "Docker What-if Workspace"
}
$property = Invoke-JsonRequest -Method POST -Uri "$baseUrl/properties" -Headers $headers -Body @{
    workspace_id = $workspace.id
    label = "Mivida Docker What-if Property"
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
$existingScenario = Invoke-JsonRequest -Method POST -Uri "$baseUrl/scenarios" -Headers $headers -Body @{
    property_state_id = $property.id
    name = "Existing Expanded Mivida Scenario"
    modifications = @{ size_sqm = 225 }
}

$baseWhatIf = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/what-if" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    modifications = @{
        size_sqm = 230
    }
}
$bedroomAmenityWhatIf = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/what-if" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    modifications = @{
        bedrooms = 3
        parking = $true
    }
}
$scenarioWhatIf = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/what-if" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    scenario_id = $existingScenario.id
    modifications = @{
        bathrooms = 4
        gym = $true
    }
}

$propertyAfterWhatIf = Invoke-JsonRequest -Method GET -Uri "$baseUrl/properties/$($property.id)" -Headers $headers
$scenarioAfterWhatIf = Invoke-JsonRequest -Method GET -Uri "$baseUrl/scenarios/$($existingScenario.id)" -Headers $headers
$eventsBeforeRestart = Invoke-JsonRequest -Method GET -Uri "$baseUrl/workspaces/$($workspace.id)/tool-events" -Headers $headers
$baseSandboxEvent = $eventsBeforeRestart | Where-Object {
    $_.tool_name -eq "valuation" -and $_.payload.response.valuation_id -eq $baseWhatIf.scenario_valuation_id
} | Select-Object -First 1
$baseFairnessEvent = $eventsBeforeRestart | Where-Object {
    $_.tool_name -eq "valuation" -and $_.payload.response.valuation_id -eq $baseWhatIf.fairness_valuation_id
} | Select-Object -First 1
$bedroomAmenitySandboxEvent = $eventsBeforeRestart | Where-Object {
    $_.tool_name -eq "valuation" -and $_.payload.response.valuation_id -eq $bedroomAmenityWhatIf.scenario_valuation_id
} | Select-Object -First 1
$scenarioBaseEvent = $eventsBeforeRestart | Where-Object {
    $_.tool_name -eq "valuation" -and $_.payload.response.valuation_id -eq $scenarioWhatIf.base_valuation_id
} | Select-Object -First 1
$scenarioSandboxEvent = $eventsBeforeRestart | Where-Object {
    $_.tool_name -eq "valuation" -and $_.payload.response.valuation_id -eq $scenarioWhatIf.scenario_valuation_id
} | Select-Object -First 1
$scenarioFairnessEvent = $eventsBeforeRestart | Where-Object {
    $_.tool_name -eq "valuation" -and $_.payload.response.valuation_id -eq $scenarioWhatIf.fairness_valuation_id
} | Select-Object -First 1

$tenantIsolationStatus = 0
try {
    Invoke-WebRequest -Method POST -Uri "$baseUrl/tools/what-if" -Headers $otherHeaders -ContentType "application/json" -Body (@{
        workspace_id = $workspace.id
        property_id = $property.id
        modifications = @{ size_sqm = 230 }
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
$whatIfAfterBackendRestart = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/what-if" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $property.id
    scenario_id = $existingScenario.id
    modifications = @{ bathrooms = 4 }
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

$baseModifiedFeatures = @($baseWhatIf.feature_changes.modified | ForEach-Object { $_.feature })
$bedroomAmenityAddedFeatures = @($bedroomAmenityWhatIf.feature_changes.added | ForEach-Object { $_.feature })
$bedroomAmenityModifiedFeatures = @($bedroomAmenityWhatIf.feature_changes.modified | ForEach-Object { $_.feature })
$scenarioAddedFeatures = @($scenarioWhatIf.feature_changes.added | ForEach-Object { $_.feature })
$scenarioModifiedFeatures = @($scenarioWhatIf.feature_changes.modified | ForEach-Object { $_.feature })
$result = [ordered]@{
    workspace_id = $workspace.id
    property_id = $property.id
    existing_scenario_id = $existingScenario.id
    base_valuation_id = $baseWhatIf.base_valuation_id
    scenario_valuation_id = $baseWhatIf.scenario_valuation_id
    fairness_valuation_id = $baseWhatIf.fairness_valuation_id
    base_valuation = $baseWhatIf.base_valuation
    scenario_valuation = $baseWhatIf.scenario_valuation
    delta_value = $baseWhatIf.delta_value
    delta_calculation_valid = (($baseWhatIf.scenario_valuation - $baseWhatIf.base_valuation) -eq $baseWhatIf.delta_value)
    source = $baseWhatIf.source
    explainability_source = $baseWhatIf.explainability.source
    comparable_source = $baseWhatIf.comparables.source
    comparable_count = @($baseWhatIf.comparables.comparables).Count
    comparable_refresh_valuation_id = $baseWhatIf.comparables.valuation_id
    fairness_refresh_is_distinct = ($baseWhatIf.fairness_valuation_id -ne $baseWhatIf.scenario_valuation_id)
    base_router_size_sqm = $baseSandboxEvent.payload.request.router_request.size_sqm
    bedroom_router_bedrooms = $bedroomAmenitySandboxEvent.payload.request.router_request.bedrooms
    amenity_router_has_parking = @($bedroomAmenitySandboxEvent.payload.request.router_request.amenities) -contains "CP"
    fairness_router_target_price_egp = $baseFairnessEvent.payload.request.router_request.target_price_egp
    scenario_base_router_size_sqm = $scenarioBaseEvent.payload.request.router_request.size_sqm
    scenario_router_size_sqm = $scenarioSandboxEvent.payload.request.router_request.size_sqm
    scenario_router_bathrooms = $scenarioSandboxEvent.payload.request.router_request.bathrooms
    scenario_router_has_gym = @($scenarioSandboxEvent.payload.request.router_request.amenities) -contains "SY"
    scenario_fairness_router_has_gym = @($scenarioFairnessEvent.payload.request.router_request.amenities) -contains "SY"
    base_property_area_unchanged = ([decimal]$propertyAfterWhatIf.area -eq 220)
    base_property_bedrooms_unchanged = ($propertyAfterWhatIf.bedrooms -eq 4)
    base_property_amenities_unchanged = (@($propertyAfterWhatIf.amenities.codes) -join "," -eq "BA,SE")
    existing_scenario_unchanged = ([decimal]$scenarioAfterWhatIf.modifications.size_sqm -eq 225)
    base_modified_features = $baseModifiedFeatures
    bedroom_amenity_added_features = $bedroomAmenityAddedFeatures
    bedroom_amenity_modified_features = $bedroomAmenityModifiedFeatures
    scenario_added_features = $scenarioAddedFeatures
    scenario_modified_features = $scenarioModifiedFeatures
    assumptions_include_furnished_unknown = @($baseWhatIf.assumptions_used) -contains "Furnished = Unknown"
    tenant_isolation_status = $tenantIsolationStatus
    what_if_events_before_restart = @($eventsBeforeRestart | Where-Object { $_.tool_name -eq "what_if" }).Count
    what_if_events_after_postgres_restart = @($eventsAfterPostgresRestart | Where-Object { $_.tool_name -eq "what_if" }).Count
    restart_what_if_source = $whatIfAfterBackendRestart.source
    forbidden_tool_logic_references = $toolLogicReferences.Count
}

if (
    $result.source -ne "TruthLayer" -or
    $result.explainability_source -ne "TruthLayer" -or
    $result.comparable_source -ne "TruthLayer" -or
    $result.comparable_count -lt 1 -or
    $result.comparable_refresh_valuation_id -ne $baseWhatIf.scenario_valuation_id -or
    -not $result.fairness_refresh_is_distinct -or
    -not $result.delta_calculation_valid -or
    $result.base_router_size_sqm -ne 230 -or
    $result.bedroom_router_bedrooms -ne 3 -or
    -not $result.amenity_router_has_parking -or
    $result.fairness_router_target_price_egp -ne $baseWhatIf.base_valuation -or
    $result.scenario_base_router_size_sqm -ne 225 -or
    $result.scenario_router_size_sqm -ne 225 -or
    $result.scenario_router_bathrooms -ne 4 -or
    -not $result.scenario_router_has_gym -or
    -not $result.scenario_fairness_router_has_gym -or
    -not $result.base_property_area_unchanged -or
    -not $result.base_property_bedrooms_unchanged -or
    -not $result.base_property_amenities_unchanged -or
    -not $result.existing_scenario_unchanged -or
    -not ($result.base_modified_features -contains "Size") -or
    -not ($result.bedroom_amenity_added_features -contains "Parking") -or
    -not ($result.bedroom_amenity_modified_features -contains "Bedrooms") -or
    -not ($result.scenario_added_features -contains "Gym") -or
    -not ($result.scenario_modified_features -contains "Bathrooms") -or
    -not $result.assumptions_include_furnished_unknown -or
    $result.tenant_isolation_status -ne 404 -or
    $result.what_if_events_before_restart -ne 3 -or
    $result.what_if_events_after_postgres_restart -lt 4 -or
    $result.restart_what_if_source -ne "TruthLayer" -or
    $result.forbidden_tool_logic_references -ne 0
) {
    $result | ConvertTo-Json -Depth 20
    throw "Copilot What-if Docker validation failed."
}

$result | ConvertTo-Json -Depth 20
