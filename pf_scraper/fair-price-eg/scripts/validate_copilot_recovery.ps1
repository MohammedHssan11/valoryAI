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
        name = "Docker Recovery Validation"
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
        $params.Body = ($Body | ConvertTo-Json -Depth 10)
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

docker compose up -d --build db db-bootstrap backend
Wait-Backend

$baseUrl = "http://localhost:8000/v1/copilot"
$subject = "recovery-$([guid]::NewGuid())"
$headers = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject $subject)" }
$user = Invoke-JsonRequest -Method GET -Uri "$baseUrl/users/me" -Headers $headers
$workspace = Invoke-JsonRequest -Method POST -Uri "$baseUrl/workspaces" -Headers $headers -Body @{
    name = "Docker Recovery Workspace"
}
$property = Invoke-JsonRequest -Method POST -Uri "$baseUrl/properties" -Headers $headers -Body @{
    workspace_id = $workspace.id
    label = "Property A"
    location = "New Cairo"
    area = 150
    bedrooms = 3
    bathrooms = 2
    amenities = @{}
}
$scenario = Invoke-JsonRequest -Method POST -Uri "$baseUrl/scenarios" -Headers $headers -Body @{
    property_state_id = $property.id
    name = "Recovery Scenario"
    modifications = @{ parking = "unknown" }
}
$brokerSessionId = "docker-broker-$([guid]::NewGuid().ToString('N').Substring(0, 10))"
$broker = Invoke-JsonRequest -Method POST -Uri "http://localhost:8000/v1/broker/chat" -Headers $headers -Body @{
    session_id = $brokerSessionId
    workspace_id = $workspace.id
    scenario_id = $scenario.id
    message = "Preserve this broker session through Docker recovery."
}

docker compose restart backend
Wait-Backend
$afterBackendRestart = Invoke-JsonRequest -Method GET -Uri "$baseUrl/scenarios/$($scenario.id)" -Headers $headers
$brokerAfterBackendRestart = Invoke-JsonRequest -Method GET -Uri "http://localhost:8000/v1/broker/session/$brokerSessionId" -Headers $headers

docker compose restart db backend
Wait-Backend
$afterDockerRestart = Invoke-JsonRequest -Method GET -Uri "$baseUrl/scenarios/$($scenario.id)" -Headers $headers
$brokerAfterDockerRestart = Invoke-JsonRequest -Method GET -Uri "http://localhost:8000/v1/broker/session/$brokerSessionId" -Headers $headers

docker compose up -d --force-recreate backend
Wait-Backend
$afterContainerRecreate = Invoke-JsonRequest -Method GET -Uri "$baseUrl/scenarios/$($scenario.id)" -Headers $headers
$brokerAfterContainerRecreate = Invoke-JsonRequest -Method GET -Uri "http://localhost:8000/v1/broker/session/$brokerSessionId" -Headers $headers

[ordered]@{
    user_id = $user.id
    workspace_id = $workspace.id
    property_id = $property.id
    scenario_id = $scenario.id
    broker_session_id = $brokerSessionId
    backend_restart_retrieved = ($afterBackendRestart.id -eq $scenario.id)
    docker_restart_retrieved = ($afterDockerRestart.id -eq $scenario.id)
    container_recreate_retrieved = ($afterContainerRecreate.id -eq $scenario.id)
    broker_backend_restart_retrieved = ($brokerAfterBackendRestart.data.scenario_id -eq $scenario.id)
    broker_postgres_restart_retrieved = ($brokerAfterDockerRestart.data.scenario_id -eq $scenario.id)
    broker_container_recreate_retrieved = ($brokerAfterContainerRecreate.data.scenario_id -eq $scenario.id)
} | ConvertTo-Json
