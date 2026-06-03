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
if (-not $env:BACKEND_PORT) {
    $env:BACKEND_PORT = "58002"
}
$backendUrl = "http://localhost:$($env:BACKEND_PORT)"

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
        name = "Docker Response Composer Validation"
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
            Invoke-RestMethod -Method GET -Uri "$backendUrl/health/ready" | Out-Null
            return
        }
        catch {
            Start-Sleep -Seconds 2
        }
    }
    throw "Backend did not become ready within 120 seconds."
}

function Invoke-ComposerValidation {
    param([string]$Mode)

    $json = docker compose exec -T backend python -m app.scripts.validate_response_composer `
        --mode $Mode `
        --subject $subject `
        --workspace-id $workspace.id `
        --empty-workspace-id $emptyWorkspace.id `
        --property-a-id $propertyA.id `
        --property-b-id $propertyB.id `
        --other-property-id $otherProperty.id `
        --replay-path "/tmp/response_composer_execution_result.json"
    if ($LASTEXITCODE -ne 0) {
        throw "Response Composer in-container $Mode validation failed."
    }
    return $json | ConvertFrom-Json
}

docker compose up -d --build db db-bootstrap backend
if ($LASTEXITCODE -ne 0) {
    throw "Docker stack build failed."
}
Wait-Backend

$baseUrl = "$backendUrl/v1/copilot"
$subject = "response-composer-$([guid]::NewGuid())"
$otherSubject = "response-composer-other-$([guid]::NewGuid())"
$headers = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject $subject)" }
$otherHeaders = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject $otherSubject)" }
$workspace = Invoke-JsonRequest -Method POST -Uri "$baseUrl/workspaces" -Headers $headers -Body @{
    name = "Docker Response Composer Workspace"
}
$emptyWorkspace = Invoke-JsonRequest -Method POST -Uri "$baseUrl/workspaces" -Headers $headers -Body @{
    name = "Docker Response Composer Empty Workspace"
}
$propertyA = Invoke-JsonRequest -Method POST -Uri "$baseUrl/properties" -Headers $headers -Body @{
    workspace_id = $workspace.id
    label = "Composer Property A"
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
$propertyB = Invoke-JsonRequest -Method POST -Uri "$baseUrl/properties" -Headers $headers -Body @{
    workspace_id = $workspace.id
    label = "Composer Property B"
    location = "Mivida"
    area = 230
    bedrooms = 4
    bathrooms = 3
    amenities = @{ codes = @("BA", "SE") }
    valuation_inputs = @{
        lat = 30.00575065612793
        lng = 31.533998489379883
        compound_name = "Mivida"
    }
}
$otherWorkspace = Invoke-JsonRequest -Method POST -Uri "$baseUrl/workspaces" -Headers $otherHeaders -Body @{
    name = "Docker Response Composer Other Workspace"
}
$otherProperty = Invoke-JsonRequest -Method POST -Uri "$baseUrl/properties" -Headers $otherHeaders -Body @{
    workspace_id = $otherWorkspace.id
    label = "Other Tenant Property"
    location = "Mivida"
    area = 240
    bedrooms = 4
    bathrooms = 3
    amenities = @{ codes = @("BA", "SE") }
    valuation_inputs = @{
        lat = 30.00575065612793
        lng = 31.533998489379883
        compound_name = "Mivida"
    }
}

$initial = Invoke-ComposerValidation -Mode "initial"

docker compose restart backend
if ($LASTEXITCODE -ne 0) {
    throw "Backend restart failed."
}
Wait-Backend
$afterBackendRestart = Invoke-ComposerValidation -Mode "replay"

docker compose restart db backend
if ($LASTEXITCODE -ne 0) {
    throw "PostgreSQL restart failed."
}
Wait-Backend
$afterPostgresRestart = Invoke-ComposerValidation -Mode "replay"

Push-Location "backend"
try {
    $env:RUN_POSTGIS_INTEGRATION = "1"
    python -m pytest -p no:cacheprovider `
        app/tests/test_response_composer_postgis_integration.py `
        app/tests/test_tool_executor_postgis_integration.py -q
    if ($LASTEXITCODE -ne 0) {
        throw "Response Composer live PostGIS integration sweep failed."
    }
}
finally {
    Remove-Item Env:RUN_POSTGIS_INTEGRATION -ErrorAction SilentlyContinue
    Pop-Location
}

$result = [ordered]@{
    workspace_id = $workspace.id
    empty_workspace_id = $emptyWorkspace.id
    property_a_id = $propertyA.id
    property_b_id = $propertyB.id
    composer_only = $initial.composer_only
    execution_result_primary_intent = $initial.execution_result_primary_intent
    execution_result_secondary_intents = $initial.execution_result_secondary_intents
    comparison_status = $initial.comparison_status
    comparison_price_delta = $initial.comparison_price_delta
    comparison_percentage_delta = $initial.comparison_percentage_delta
    comparison_arithmetic_valid = $initial.comparison_arithmetic_valid
    comparison_prohibited_fields = @($initial.comparison_prohibited_fields).Count
    deterministic_output_count = $initial.deterministic_output_count
    deterministic_response_id = $initial.deterministic_response_id
    citation_valuation_count = $initial.citation_valuation_count
    citation_comparable_count = $initial.citation_comparable_count
    compressed_top_comparable_count = $initial.compressed_top_comparable_count
    frontend_comparable_count = $initial.frontend_comparable_count
    dual_channel_delivery = $initial.dual_channel_delivery
    negotiation_status = $initial.negotiation_status
    investment_status = $initial.investment_status
    market_status = $initial.market_status
    multi_intent_status = $initial.multi_intent_status
    sparse_status = $initial.sparse_status
    partial_status = $initial.partial_status
    failed_status = $initial.failed_status
    clarification_status = $initial.clarification_status
    average_latency_ms = $initial.average_latency_ms
    latency_target_ms = $initial.latency_target_ms
    latency_target_passed = $initial.latency_target_passed
    backend_restart_replay_equal = $afterBackendRestart.replay_equal
    postgres_restart_replay_equal = $afterPostgresRestart.replay_equal
    backend_restart_response_id = $afterBackendRestart.response_id
    postgres_restart_response_id = $afterPostgresRestart.response_id
    forbidden_source_references = @($initial.forbidden_source_references).Count
    forbidden_imports = @($initial.forbidden_imports).Count
    direct_queries_found = $initial.direct_queries_found
    live_postgis_integration_tests = "PASS"
    docker_validation = "PASS"
}

if (
    -not $result.composer_only -or
    $result.execution_result_primary_intent -ne "PROPERTY_COMPARISON" -or
    @($result.execution_result_secondary_intents).Count -ne 1 -or
    $result.execution_result_secondary_intents -ne "NEGOTIATION" -or
    $result.comparison_status -ne "SUCCESS" -or
    -not $result.comparison_arithmetic_valid -or
    $result.comparison_prohibited_fields -ne 0 -or
    $result.deterministic_output_count -ne 1 -or
    $result.citation_valuation_count -lt 1 -or
    $result.citation_comparable_count -lt 1 -or
    $result.compressed_top_comparable_count -gt 3 -or
    $result.frontend_comparable_count -lt $result.compressed_top_comparable_count -or
    -not $result.dual_channel_delivery -or
    $result.negotiation_status -ne "SUCCESS" -or
    $result.investment_status -ne "SUCCESS" -or
    $result.sparse_status -ne "SPARSE_EVIDENCE" -or
    $result.partial_status -ne "PARTIAL_SUCCESS" -or
    $result.failed_status -ne "FAILED" -or
    $result.clarification_status -ne "CLARIFICATION_REQUIRED" -or
    -not $result.latency_target_passed -or
    -not $result.backend_restart_replay_equal -or
    -not $result.postgres_restart_replay_equal -or
    $result.backend_restart_response_id -ne $result.deterministic_response_id -or
    $result.postgres_restart_response_id -ne $result.deterministic_response_id -or
    $result.forbidden_source_references -ne 0 -or
    $result.forbidden_imports -ne 0 -or
    $result.direct_queries_found
) {
    $result | ConvertTo-Json -Depth 20
    throw "Response Composer Docker validation failed."
}

$result | ConvertTo-Json -Depth 20
