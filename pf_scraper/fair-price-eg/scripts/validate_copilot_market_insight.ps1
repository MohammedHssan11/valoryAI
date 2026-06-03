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
        name = "Docker Market Insight Validation"
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

function Test-StatementsTraceable {
    param([object]$Insight)
    return @($Insight.evidence_summary.statements | Where-Object { @($_.evidence).Count -eq 0 }).Count -eq 0
}

function Test-ForbiddenMarketField {
    param([object]$Value)

    if ($null -eq $Value) {
        return $false
    }
    if ($Value -is [string] -or $Value -is [ValueType]) {
        return $false
    }
    if ($Value -is [System.Collections.IDictionary]) {
        foreach ($key in $Value.Keys) {
            if ([string]$key -match "(forecast|future_price|expected_appreciation|predicted_inflation|predicted_return|synthetic_trend)") {
                return $true
            }
            if (Test-ForbiddenMarketField -Value $Value[$key]) {
                return $true
            }
        }
        return $false
    }
    if ($Value -is [System.Collections.IEnumerable]) {
        foreach ($item in $Value) {
            if (Test-ForbiddenMarketField -Value $item) {
                return $true
            }
        }
        return $false
    }
    foreach ($property in $Value.PSObject.Properties) {
        if ($property.Name -match "(forecast|future_price|expected_appreciation|predicted_inflation|predicted_return|synthetic_trend)") {
            return $true
        }
        if (Test-ForbiddenMarketField -Value $property.Value) {
            return $true
        }
    }
    return $false
}

docker compose up -d --build db db-bootstrap backend
if ($LASTEXITCODE -ne 0) {
    throw "Docker stack build failed."
}
Wait-Backend

$baseUrl = "http://localhost:8000/v1/copilot"
$subject = "market-insight-$([guid]::NewGuid())"
$headers = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject $subject)" }
$otherHeaders = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject "other-$subject")" }

$workspace = Invoke-JsonRequest -Method POST -Uri "$baseUrl/workspaces" -Headers $headers -Body @{
    name = "Docker Market Insight Workspace"
}
$mividaApartment = Invoke-JsonRequest -Method POST -Uri "$baseUrl/properties" -Headers $headers -Body @{
    workspace_id = $workspace.id
    label = "Mivida Docker Apartment"
    location = "Mivida"
    area = 150
    bedrooms = 3
    bathrooms = 2
    property_type = "Apartment"
    amenities = @{ codes = @("BA", "SE") }
    valuation_inputs = @{
        lat = 30.00575065612793
        lng = 31.533998489379883
        compound_name = "Mivida"
    }
}
$mividaVilla = Invoke-JsonRequest -Method POST -Uri "$baseUrl/properties" -Headers $headers -Body @{
    workspace_id = $workspace.id
    label = "Mivida Docker Villa"
    location = "Mivida"
    area = 220
    bedrooms = 4
    bathrooms = 3
    property_type = "Villa"
    amenities = @{ codes = @("BA", "SE") }
    valuation_inputs = @{
        lat = 30.00575065612793
        lng = 31.533998489379883
        compound_name = "Mivida"
    }
}
$cairoApartment = Invoke-JsonRequest -Method POST -Uri "$baseUrl/properties" -Headers $headers -Body @{
    workspace_id = $workspace.id
    label = "Central Cairo Docker Apartment"
    location = "Central Cairo"
    area = 150
    bedrooms = 3
    bathrooms = 2
    property_type = "Apartment"
    amenities = @{ codes = @("BA") }
    valuation_inputs = @{
        lat = 30.0444
        lng = 31.2357
    }
}

$mividaApartmentValuation = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/valuation" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $mividaApartment.id
}
$mividaVillaValuation = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/valuation" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $mividaVilla.id
}
$cairoApartmentValuation = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/valuation" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $cairoApartment.id
}

$h3Res9 = (docker compose exec -T backend python -c "import h3; print(h3.latlng_to_cell(30.00575065612793, 31.533998489379883, 9))").Trim()
if ($LASTEXITCODE -ne 0 -or -not $h3Res9) {
    throw "H3 resolution failed."
}

$overall = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/market-insight" -Headers $headers -Body @{
    workspace_id = $workspace.id
}
$compound = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/market-insight" -Headers $headers -Body @{
    workspace_id = $workspace.id
    compound_name = "Mivida"
}
$area = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/market-insight" -Headers $headers -Body @{
    workspace_id = $workspace.id
    h3_res9 = $h3Res9
}
$propertyType = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/market-insight" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_type = "Villa"
}
$history = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/market-insight" -Headers $headers -Body @{
    workspace_id = $workspace.id
    time_window = "30d"
}
$empty = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/market-insight" -Headers $headers -Body @{
    workspace_id = $workspace.id
    compound_name = "No Persisted Compound"
}

$eventsBeforeRestart = Invoke-JsonRequest -Method GET -Uri "$baseUrl/workspaces/$($workspace.id)/tool-events" -Headers $headers
$overallAudit = $eventsBeforeRestart | Where-Object {
    $_.tool_name -eq "market_insight" -and $_.payload.response.valuation_volume -eq 3
} | Select-Object -First 1

$tenantIsolationStatus = 0
try {
    Invoke-WebRequest -Method POST -Uri "$baseUrl/tools/market-insight" -Headers $otherHeaders -ContentType "application/json" -Body (@{
        workspace_id = $workspace.id
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
$afterBackendRestart = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/market-insight" -Headers $headers -Body @{
    workspace_id = $workspace.id
}

docker compose restart db backend
if ($LASTEXITCODE -ne 0) {
    throw "PostgreSQL restart failed."
}
Wait-Backend
$afterPostgresRestart = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/market-insight" -Headers $headers -Body @{
    workspace_id = $workspace.id
}
$eventsAfterPostgresRestart = Invoke-JsonRequest -Method GET -Uri "$baseUrl/workspaces/$($workspace.id)/tool-events" -Headers $headers

docker compose exec -T backend python -m app.scripts.run_migrations --verify
if ($LASTEXITCODE -ne 0) {
    throw "Migration verification failed."
}
$indexCount = [int](docker compose exec -T db psql -U fairprice -d fairprice -tAc "SELECT COUNT(*) FROM pg_indexes WHERE indexname IN ('ix_prediction_logs_market_filters', 'ix_shadow_logs_market_filters');")
if ($LASTEXITCODE -ne 0) {
    throw "Market Insight index verification failed."
}

$allInsights = @($overall, $compound, $area, $propertyType, $history, $empty, $afterBackendRestart, $afterPostgresRestart)
$result = [ordered]@{
    workspace_id = $workspace.id
    mivida_apartment_property_id = $mividaApartment.id
    mivida_villa_property_id = $mividaVilla.id
    cairo_apartment_property_id = $cairoApartment.id
    mivida_apartment_valuation_id = $mividaApartmentValuation.valuation_id
    mivida_villa_valuation_id = $mividaVillaValuation.valuation_id
    cairo_apartment_valuation_id = $cairoApartmentValuation.valuation_id
    h3_res9 = $h3Res9
    overall_valuation_volume = $overall.valuation_volume
    overall_prediction_log_count = $overall.evidence_summary.source_record_counts.prediction_logs
    overall_shadow_log_count = $overall.evidence_summary.source_record_counts.shadow_logs
    overall_snapshot_count = $overall.evidence_summary.source_record_counts.valuation_snapshots
    overall_confidence_count = $overall.confidence_distribution.valuation_count
    overall_comparable_density = $overall.comparable_density.density_level
    most_active_compound = $overall.active_compounds[0].name
    most_active_compound_volume = $overall.active_compounds[0].valuation_count
    active_area_count = @($overall.active_areas).Count
    compound_filter_volume = $compound.valuation_volume
    h3_filter_volume = $area.valuation_volume
    property_type_filter_volume = $propertyType.valuation_volume
    history_30d_volume = $history.valuation_volume
    empty_filter_volume = $empty.valuation_volume
    empty_filter_density = $empty.comparable_density.density_level
    required_sources_used = (@("valuation_snapshots", "prediction_logs", "shadow_logs") | Where-Object {
        $_ -notin @($overall.data_sources_used)
    }).Count -eq 0
    all_statements_traceable = @($allInsights | Where-Object { -not (Test-StatementsTraceable -Insight $_) }).Count -eq 0
    forbidden_metric_fields = @($allInsights | Where-Object { Test-ForbiddenMarketField -Value $_ }).Count
    forbidden_summary_language = @($allInsights | Where-Object { $_.market_summary -match "(?i)(forecast|future|predict|appreciation|expected return|trend)" }).Count
    audit_filters_persisted = ($overallAudit.payload.request.filters_used.workspace_id -eq $workspace.id)
    audit_sources_persisted = (@("valuation_snapshots", "prediction_logs", "shadow_logs") | Where-Object {
        $_ -notin @($overallAudit.payload.request.data_sources_used)
    }).Count -eq 0
    market_events_before_restart = @($eventsBeforeRestart | Where-Object { $_.tool_name -eq "market_insight" }).Count
    market_events_after_postgres_restart = @($eventsAfterPostgresRestart | Where-Object { $_.tool_name -eq "market_insight" }).Count
    backend_restart_volume = $afterBackendRestart.valuation_volume
    postgres_restart_volume = $afterPostgresRestart.valuation_volume
    tenant_isolation_status = $tenantIsolationStatus
    analytics_index_count = $indexCount
}

if (
    $result.overall_valuation_volume -ne 3 -or
    $result.overall_prediction_log_count -ne 3 -or
    $result.overall_shadow_log_count -ne 3 -or
    $result.overall_snapshot_count -ne 3 -or
    $result.overall_confidence_count -ne 3 -or
    $result.most_active_compound -ne "Mivida" -or
    $result.most_active_compound_volume -ne 2 -or
    $result.active_area_count -ne 2 -or
    $result.compound_filter_volume -ne 2 -or
    $result.h3_filter_volume -ne 2 -or
    $result.property_type_filter_volume -ne 1 -or
    $result.history_30d_volume -ne 3 -or
    $result.empty_filter_volume -ne 0 -or
    $result.empty_filter_density -ne "Insufficient Evidence" -or
    -not $result.required_sources_used -or
    -not $result.all_statements_traceable -or
    $result.forbidden_metric_fields -ne 0 -or
    $result.forbidden_summary_language -ne 0 -or
    -not $result.audit_filters_persisted -or
    -not $result.audit_sources_persisted -or
    $result.market_events_before_restart -ne 6 -or
    $result.market_events_after_postgres_restart -lt 8 -or
    $result.backend_restart_volume -ne 3 -or
    $result.postgres_restart_volume -ne 3 -or
    $result.tenant_isolation_status -ne 404 -or
    $result.analytics_index_count -ne 2
) {
    $result | ConvertTo-Json -Depth 20
    throw "Copilot Market Insight Docker validation failed."
}

$result | ConvertTo-Json -Depth 20
