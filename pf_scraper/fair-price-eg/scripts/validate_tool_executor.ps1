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
    $env:BACKEND_PORT = "58003"
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
        name = "Docker Tool Executor Validation"
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

function Invoke-ExecutorValidation {
    $json = docker compose exec -T backend python -m app.scripts.validate_tool_executor `
        --subject $subject `
        --other-subject $otherSubject `
        --workspace-id $workspace.id `
        --property-a-id $propertyA.id `
        --property-b-id $propertyB.id `
        --other-property-id $otherProperty.id
    if ($LASTEXITCODE -ne 0) {
        throw "Tool Executor in-container validation failed."
    }
    return $json | ConvertFrom-Json
}

docker compose up -d --build db db-bootstrap backend
if ($LASTEXITCODE -ne 0) {
    throw "Docker stack build failed."
}
Wait-Backend

$baseUrl = "$backendUrl/v1/copilot"
$subject = "tool-executor-$([guid]::NewGuid())"
$otherSubject = "tool-executor-other-$([guid]::NewGuid())"
$headers = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject $subject)" }
$otherHeaders = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject $otherSubject)" }
$workspace = Invoke-JsonRequest -Method POST -Uri "$baseUrl/workspaces" -Headers $headers -Body @{
    name = "Docker Tool Executor Workspace"
}
$propertyA = Invoke-JsonRequest -Method POST -Uri "$baseUrl/properties" -Headers $headers -Body @{
    workspace_id = $workspace.id
    label = "Executor Property A"
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
    label = "Executor Property B"
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
    name = "Docker Tool Executor Other Workspace"
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

$beforeRestart = Invoke-ExecutorValidation

docker compose restart backend
if ($LASTEXITCODE -ne 0) {
    throw "Backend restart failed."
}
Wait-Backend
$afterBackendRestart = Invoke-ExecutorValidation

docker compose restart db backend
if ($LASTEXITCODE -ne 0) {
    throw "PostgreSQL restart failed."
}
Wait-Backend
$afterPostgresRestart = Invoke-ExecutorValidation

$result = [ordered]@{
    workspace_id = $workspace.id
    property_a_id = $propertyA.id
    property_b_id = $propertyB.id
    executor_only = $beforeRestart.executor_only
    sequential_status = $beforeRestart.sequential_status
    sequential_raw_payload_source = $beforeRestart.sequential_raw_payload_source
    parallel_status = $beforeRestart.parallel_status
    parallel_concurrency_proven = $beforeRestart.parallel_concurrency_proven
    parallel_execution_time_ms = $beforeRestart.parallel_execution_time_ms
    parallel_runtime_total_ms = $beforeRestart.parallel_runtime_total_ms
    sequential_overhead_ms = $beforeRestart.sequential_overhead_ms
    parallel_overhead_ms = $beforeRestart.parallel_overhead_ms
    overhead_target_ms = $beforeRestart.overhead_target_ms
    multi_intent_status = $beforeRestart.multi_intent_status
    property_comparison_payload_count = $beforeRestart.property_comparison_payload_count
    property_comparison_raw_payloads_preserved = $beforeRestart.property_comparison_raw_payloads_preserved
    clarification_status = $beforeRestart.clarification_status
    timeout_status = $beforeRestart.timeout_status
    timeout_partial_success = $beforeRestart.timeout_partial_success
    timeout_error_type = $beforeRestart.timeout_error_type
    partial_failure_status = $beforeRestart.partial_failure_status
    partial_success = $beforeRestart.partial_success
    partial_error_type = $beforeRestart.partial_error_type
    tenant_isolation_status = $beforeRestart.tenant_isolation_status
    tenant_isolation_error_type = $beforeRestart.tenant_isolation_error_type
    audit_execution_id_present = $beforeRestart.audit_execution_id_present
    audit_plan_id_matches = $beforeRestart.audit_plan_id_matches
    tool_event_count_before_restart = $beforeRestart.tool_event_count
    backend_restart_status = $afterBackendRestart.sequential_status
    tool_event_count_after_backend_restart = $afterBackendRestart.tool_event_count
    postgres_restart_status = $afterPostgresRestart.sequential_status
    tool_event_count_after_postgres_restart = $afterPostgresRestart.tool_event_count
    forbidden_source_references = @($beforeRestart.forbidden_source_references).Count
    forbidden_imports = @($beforeRestart.forbidden_imports).Count
    direct_queries_found = $beforeRestart.direct_queries_found
    docker_validation = "PASS"
}

if (
    -not $result.executor_only -or
    $result.sequential_status -ne "SUCCESS" -or
    $result.sequential_raw_payload_source -ne "TruthLayer" -or
    $result.parallel_status -ne "SUCCESS" -or
    -not $result.parallel_concurrency_proven -or
    $result.sequential_overhead_ms -ge $result.overhead_target_ms -or
    $result.parallel_overhead_ms -ge $result.overhead_target_ms -or
    $result.multi_intent_status -ne "SUCCESS" -or
    $result.property_comparison_payload_count -ne 2 -or
    -not $result.property_comparison_raw_payloads_preserved -or
    $result.clarification_status -ne "CLARIFICATION_REQUIRED" -or
    $result.timeout_status -ne "FAILED" -or
    -not $result.timeout_partial_success -or
    $result.timeout_error_type -ne "ToolTimeoutError" -or
    $result.partial_failure_status -ne "PARTIAL_SUCCESS" -or
    -not $result.partial_success -or
    $result.partial_error_type -ne "ToolResourceNotFound" -or
    $result.tenant_isolation_status -ne "FAILED" -or
    $result.tenant_isolation_error_type -ne "ToolResourceNotFound" -or
    -not $result.audit_execution_id_present -or
    -not $result.audit_plan_id_matches -or
    $result.backend_restart_status -ne "SUCCESS" -or
    $result.postgres_restart_status -ne "SUCCESS" -or
    $result.tool_event_count_after_backend_restart -le $result.tool_event_count_before_restart -or
    $result.tool_event_count_after_postgres_restart -le $result.tool_event_count_after_backend_restart -or
    $result.forbidden_source_references -ne 0 -or
    $result.forbidden_imports -ne 0 -or
    $result.direct_queries_found
) {
    $result | ConvertTo-Json -Depth 20
    throw "Tool Executor Docker validation failed."
}

$result | ConvertTo-Json -Depth 20
