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
    $env:BACKEND_PORT = "58001"
}
$backendUrl = "http://localhost:$($env:BACKEND_PORT)"

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

function Invoke-LLMValidation {
    $json = docker compose exec -T backend python -m app.scripts.validate_llm_integration
    if ($LASTEXITCODE -ne 0) {
        throw "LLM Integration in-container validation failed."
    }
    return $json | ConvertFrom-Json
}

docker compose up -d --build db db-bootstrap backend
if ($LASTEXITCODE -ne 0) {
    throw "Docker stack build failed."
}
Wait-Backend

$initial = Invoke-LLMValidation

docker compose restart backend
if ($LASTEXITCODE -ne 0) {
    throw "Backend restart failed."
}
Wait-Backend
$afterBackendRestart = Invoke-LLMValidation

docker compose restart db
if ($LASTEXITCODE -ne 0) {
    throw "PostgreSQL restart failed."
}
Wait-Backend
$afterDatabaseRestart = Invoke-LLMValidation

$result = [ordered]@{
    authorized_runtime = $initial.authorized_runtime
    target_runtime_count = $initial.target_runtime_count
    legacy_python_file_count = $initial.legacy_python_file_count
    accepted_status = $initial.accepted_status
    citations_verified = $initial.citations_verified
    grounding_status = $initial.grounding_status
    citation_rejection_status = $initial.citation_rejection_status
    fake_value_rejection_status = $initial.fake_value_rejection_status
    fake_prediction_rejection_status = $initial.fake_prediction_rejection_status
    tenant_isolation_status = $initial.tenant_isolation_status
    tenant_isolation_provider_calls = $initial.tenant_isolation_provider_calls
    fail_closed_transport_status = $initial.fail_closed_transport_status
    fail_closed_transport_calls = $initial.fail_closed_transport_calls
    deterministic_assembly = $initial.deterministic_assembly
    prompt_assembly_overhead_ms = $initial.prompt_assembly_overhead_ms
    backend_restart_fingerprint_stable = ($initial.assembly_fingerprint -eq $afterBackendRestart.assembly_fingerprint)
    database_restart_fingerprint_stable = ($initial.assembly_fingerprint -eq $afterDatabaseRestart.assembly_fingerprint)
    docker_validation = "PASS"
}

if (
    $result.target_runtime_count -ne 1 -or
    $result.legacy_python_file_count -ne 0 -or
    $result.accepted_status -ne "ACCEPT_NARRATION" -or
    -not $result.citations_verified -or
    $result.grounding_status -ne "ACCEPT_NARRATION" -or
    $result.citation_rejection_status -ne "REJECT_NARRATION" -or
    $result.fake_value_rejection_status -ne "REJECT_NARRATION" -or
    $result.fake_prediction_rejection_status -ne "REJECT_NARRATION" -or
    $result.tenant_isolation_status -ne "ACCESS_DENIED" -or
    $result.tenant_isolation_provider_calls -ne 0 -or
    $result.fail_closed_transport_status -ne "REJECT_NARRATION" -or
    $result.fail_closed_transport_calls -ne 1 -or
    -not $result.deterministic_assembly -or
    -not $result.backend_restart_fingerprint_stable -or
    -not $result.database_restart_fingerprint_stable
) {
    $result | ConvertTo-Json -Depth 20
    throw "LLM Integration Docker validation failed."
}

$result | ConvertTo-Json -Depth 20
