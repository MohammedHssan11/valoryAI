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
        name = "Docker Memory Integration Validation"
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

function Invoke-MemoryValidation {
    param([string]$Mode)

    $replayArguments = @()
    if ($Mode -eq "replay") {
        $replayArguments = @("--expected-memory-id", $initial.memory_id)
    }
    $json = docker compose exec -T backend python -m app.scripts.validate_memory_integration `
        --mode $Mode `
        --subject $subject `
        --other-subject $otherSubject `
        --workspace-id $workspace.id `
        --empty-workspace-id $emptyWorkspace.id `
        --scenario-id $scenario.id `
        --property-a-id $propertyA.id `
        --property-b-id $propertyB.id `
        --broker-session-id $brokerSessionId `
        --replay-path "/tmp/memory_integration_context.json" `
        @replayArguments
    if ($LASTEXITCODE -ne 0) {
        throw "Memory Integration in-container $Mode validation failed."
    }
    return $json | ConvertFrom-Json
}

docker compose up -d --build db db-bootstrap backend
if ($LASTEXITCODE -ne 0) {
    throw "Docker stack build failed."
}
Wait-Backend

$baseUrl = "$backendUrl/v1/copilot"
$subject = "memory-integration-$([guid]::NewGuid())"
$otherSubject = "memory-integration-other-$([guid]::NewGuid())"
$headers = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject $subject)" }
$otherHeaders = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject $otherSubject)" }
Invoke-JsonRequest -Method GET -Uri "$baseUrl/users/me" -Headers $headers | Out-Null
Invoke-JsonRequest -Method GET -Uri "$baseUrl/users/me" -Headers $otherHeaders | Out-Null
$workspace = Invoke-JsonRequest -Method POST -Uri "$baseUrl/workspaces" -Headers $headers -Body @{
    name = "Docker Memory Integration Workspace"
}
$emptyWorkspace = Invoke-JsonRequest -Method POST -Uri "$baseUrl/workspaces" -Headers $headers -Body @{
    name = "Docker Memory Integration Empty Workspace"
}
$propertyA = Invoke-JsonRequest -Method POST -Uri "$baseUrl/properties" -Headers $headers -Body @{
    workspace_id = $workspace.id
    label = "Memory Property A"
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
    label = "Memory Property B"
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
$scenario = Invoke-JsonRequest -Method POST -Uri "$baseUrl/scenarios" -Headers $headers -Body @{
    property_state_id = $propertyA.id
    name = "Memory Integration Scenario"
    modifications = @{ parking = $true }
}
Invoke-JsonRequest -Method POST -Uri "$baseUrl/assumptions" -Headers $headers -Body @{
    property_state_id = $propertyA.id
    scenario_state_id = $scenario.id
    key = "parking"
    value = $true
    status = "confirmed"
    source = "docker-validation"
} | Out-Null
$chat = Invoke-JsonRequest -Method POST -Uri "$baseUrl/chats" -Headers $headers -Body @{
    workspace_id = $workspace.id
    title = "Memory Integration History"
}
for ($index = 0; $index -lt 15; $index++) {
    Invoke-JsonRequest -Method POST -Uri "$baseUrl/messages" -Headers $headers -Body @{
        chat_id = $chat.id
        role = "user"
        content = "Memory integration message $index"
    } | Out-Null
    Invoke-JsonRequest -Method POST -Uri "$baseUrl/tool-events" -Headers $headers -Body @{
        workspace_id = $workspace.id
        property_state_id = $propertyA.id
        scenario_state_id = $scenario.id
        tool_name = "validation-event"
        event_type = "executed"
        payload = @{
            response = @{
                valuation_id = "validation_val_$index"
                comparable_ids = @("validation_comp_$index")
            }
        }
    } | Out-Null
}
$brokerSessionId = "memory-docker-$([guid]::NewGuid().ToString('N').Substring(0, 10))"
Invoke-JsonRequest -Method POST -Uri "$backendUrl/v1/broker/chat" -Headers $headers -Body @{
    session_id = $brokerSessionId
    workspace_id = $workspace.id
    scenario_id = $scenario.id
    message = "Preserve this memory context through Docker recovery."
} | Out-Null

$initial = Invoke-MemoryValidation -Mode "initial"

docker compose restart backend
if ($LASTEXITCODE -ne 0) {
    throw "Backend restart failed."
}
Wait-Backend
$afterBackendRestart = Invoke-MemoryValidation -Mode "replay"

docker compose restart db backend
if ($LASTEXITCODE -ne 0) {
    throw "PostgreSQL restart failed."
}
Wait-Backend
$afterPostgresRestart = Invoke-MemoryValidation -Mode "replay"

docker compose up -d --force-recreate backend
if ($LASTEXITCODE -ne 0) {
    throw "Backend container recreation failed."
}
Wait-Backend
$afterContainerRecreate = Invoke-MemoryValidation -Mode "replay"

Push-Location "backend"
try {
    $env:RUN_POSTGIS_INTEGRATION = "1"
    python -m pytest -p no:cacheprovider `
        app/tests/test_memory_integration_postgis_integration.py `
        app/tests/test_response_composer_postgis_integration.py `
        app/tests/test_tool_executor_postgis_integration.py -q
    if ($LASTEXITCODE -ne 0) {
        throw "Memory Integration live PostGIS regression sweep failed."
    }
}
finally {
    Remove-Item Env:RUN_POSTGIS_INTEGRATION -ErrorAction SilentlyContinue
    Pop-Location
}

$result = [ordered]@{
    workspace_id = $workspace.id
    empty_workspace_id = $emptyWorkspace.id
    scenario_id = $scenario.id
    memory_id = $initial.memory_id
    status = $initial.status
    memory_only = $initial.memory_only
    idempotent_memory_equal = $initial.idempotent_memory_equal
    remembered_decision_count = $initial.remembered_decision_count
    deterministic_memory_id_count = $initial.deterministic_memory_id_count
    empty_workspace_status = $initial.empty_workspace_status
    tenant_isolation_status = $initial.tenant_isolation_status
    broker_session_recovered = $initial.broker_session_recovered
    active_comparison_recovered = $initial.active_comparison_recovered
    citation_valuation_count = $initial.citation_valuation_count
    citation_tool_event_count = $initial.citation_tool_event_count
    recent_tool_history_count = $initial.recent_tool_history_count
    recent_decision_count = $initial.recent_decision_count
    recent_valuation_count = $initial.recent_valuation_count
    recent_conversation_metadata_count = $initial.recent_conversation_metadata_count
    tool_history_compressed = $initial.tool_history_compressed
    conversation_metadata_compressed = $initial.conversation_metadata_compressed
    average_overhead_ms_excluding_database = $initial.average_overhead_ms_excluding_database
    latency_target_ms = $initial.latency_target_ms
    latency_target_passed = $initial.latency_target_passed
    backend_restart_replay_equal = $afterBackendRestart.replay_equal
    postgres_restart_replay_equal = $afterPostgresRestart.replay_equal
    container_recreate_replay_equal = $afterContainerRecreate.replay_equal
    forbidden_source_references = @($initial.forbidden_source_references).Count
    forbidden_imports = @($initial.forbidden_imports).Count
    live_postgis_integration_tests = "PASS"
    docker_validation = "PASS"
}

if (
    $result.status -ne "SUCCESS" -or
    -not $result.memory_only -or
    -not $result.idempotent_memory_equal -or
    $result.remembered_decision_count -ne 1 -or
    $result.deterministic_memory_id_count -ne 1 -or
    $result.empty_workspace_status -ne "EMPTY_CONTEXT" -or
    $result.tenant_isolation_status -ne "ACCESS_DENIED" -or
    -not $result.broker_session_recovered -or
    -not $result.active_comparison_recovered -or
    $result.citation_valuation_count -lt 2 -or
    $result.citation_tool_event_count -lt 1 -or
    -not $result.tool_history_compressed -or
    -not $result.conversation_metadata_compressed -or
    -not $result.latency_target_passed -or
    -not $result.backend_restart_replay_equal -or
    -not $result.postgres_restart_replay_equal -or
    -not $result.container_recreate_replay_equal -or
    $result.forbidden_source_references -ne 0 -or
    $result.forbidden_imports -ne 0
) {
    $result | ConvertTo-Json -Depth 20
    throw "Memory Integration Docker validation failed."
}

$result | ConvertTo-Json -Depth 20
