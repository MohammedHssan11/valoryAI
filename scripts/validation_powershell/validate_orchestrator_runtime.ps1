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
        name = "Docker Orchestrator Runtime Validation"
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
        $params.Body = ($Body | ConvertTo-Json -Depth 40)
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

function Invoke-Orchestrator {
    param(
        [string]$Message,
        [hashtable]$ToolInputs
    )
    return Invoke-JsonRequest -Method POST -Uri "$baseUrl/orchestrator/respond" -Headers $headers -Body @{
        workspace_id = $workspace.id
        message = $Message
        tool_inputs = $ToolInputs
    }
}

function Get-RuntimeFingerprint {
    param($Response)

    $outputs = @($Response.response.tool_outputs)
    return [ordered]@{
        intent = $Response.intent
        status = $Response.status
        delivery_mode = $Response.delivery_mode
        composition_status = $Response.audit.composition_status
        memory_status = $Response.audit.memory_status
        tool_names = @($outputs | ForEach-Object { $_.tool_name })
        tool_sources = @($outputs | ForEach-Object { $_.payload.source })
        fair_prices = @($outputs | Where-Object { $null -ne $_.payload.fair_price } | ForEach-Object { $_.payload.fair_price })
        failed_tool_count = @($Response.response.failed_tools).Count
    }
}

function Invoke-RuntimeSuite {
    $valuation = Invoke-Orchestrator -Message "What is the fair price for this property?" -ToolInputs @{
        VALUATION_TOOL = @{
            workspace_id = $workspace.id
            property_id = $propertyA.id
        }
    }
    $comparison = Invoke-Orchestrator -Message "Compare these two properties." -ToolInputs @{
        "VALUATION_TOOL:PROPERTY_A" = @{
            workspace_id = $workspace.id
            property_id = $propertyA.id
        }
        "VALUATION_TOOL:PROPERTY_B" = @{
            workspace_id = $workspace.id
            property_id = $propertyB.id
        }
    }
    $negotiation = Invoke-Orchestrator -Message "Should I negotiate this overpriced listing?" -ToolInputs @{
        NEGOTIATION_TOOL = @{
            workspace_id = $workspace.id
            property_id = $propertyA.id
            asking_price_egp = $askingPrice
        }
    }
    $investment = Invoke-Orchestrator -Message "Is this a good investment?" -ToolInputs @{
        INVESTMENT_TOOL = @{
            workspace_id = $workspace.id
            property_id = $propertyA.id
            asking_price_egp = $askingPrice
        }
    }
    $marketInsight = Invoke-Orchestrator -Message "What is happening in Mivida?" -ToolInputs @{
        MARKET_INSIGHT_TOOL = @{
            workspace_id = $workspace.id
            compound_name = "Mivida"
        }
    }
    $clarification = Invoke-Orchestrator -Message "Tell me more" -ToolInputs @{}
    return [ordered]@{
        valuation = Get-RuntimeFingerprint $valuation
        property_comparison = Get-RuntimeFingerprint $comparison
        negotiation = Get-RuntimeFingerprint $negotiation
        investment = Get-RuntimeFingerprint $investment
        market_insight = Get-RuntimeFingerprint $marketInsight
        clarification = Get-RuntimeFingerprint $clarification
    }
}

function Test-SuiteEqual {
    param($First, $Second)
    return (
        ($First | ConvertTo-Json -Depth 30 -Compress) -eq
        ($Second | ConvertTo-Json -Depth 30 -Compress)
    )
}

docker compose up -d --build db db-bootstrap backend
if ($LASTEXITCODE -ne 0) {
    throw "Docker stack build failed."
}
Wait-Backend

$baseUrl = "$backendUrl/v1/copilot"
$subject = "orchestrator-runtime-$([guid]::NewGuid())"
$headers = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject $subject)" }
$otherHeaders = @{ "Authorization" = "Bearer $(New-ValidationJwt -Subject "other-$subject")" }
Invoke-JsonRequest -Method GET -Uri "$baseUrl/users/me" -Headers $headers | Out-Null
Invoke-JsonRequest -Method GET -Uri "$baseUrl/users/me" -Headers $otherHeaders | Out-Null
$workspace = Invoke-JsonRequest -Method POST -Uri "$baseUrl/workspaces" -Headers $headers -Body @{
    name = "Docker Orchestrator Runtime Workspace"
}
$propertyA = Invoke-JsonRequest -Method POST -Uri "$baseUrl/properties" -Headers $headers -Body @{
    workspace_id = $workspace.id
    label = "Orchestrator Property A"
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
    label = "Orchestrator Property B"
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
$seedValuation = Invoke-JsonRequest -Method POST -Uri "$baseUrl/tools/valuation" -Headers $headers -Body @{
    workspace_id = $workspace.id
    property_id = $propertyA.id
}
$askingPrice = [int]$seedValuation.price_range.high + 1

$initial = Invoke-RuntimeSuite

$denied = Invoke-JsonRequest -Method POST -Uri "$baseUrl/orchestrator/respond" -Headers $otherHeaders -Body @{
    workspace_id = $workspace.id
    message = "Tell me more"
    tool_inputs = @{}
}

$llmJson = docker compose exec -T backend python -m app.scripts.validate_llm_integration
if ($LASTEXITCODE -ne 0) {
    throw "Grounding rejection validation failed."
}
$llm = $llmJson | ConvertFrom-Json

docker compose restart backend
if ($LASTEXITCODE -ne 0) {
    throw "Backend restart failed."
}
Wait-Backend
$afterBackendRestart = Invoke-RuntimeSuite

docker compose restart db backend
if ($LASTEXITCODE -ne 0) {
    throw "PostgreSQL restart failed."
}
Wait-Backend
$afterPostgresRestart = Invoke-RuntimeSuite

$result = [ordered]@{
    endpoint = "/v1/copilot/orchestrator/respond"
    runtime_id = "COPILOT_ORCHESTRATOR_LLM_V1"
    workspace_id = $workspace.id
    property_a_id = $propertyA.id
    property_b_id = $propertyB.id
    initial = $initial
    access_denied_status = $denied.status
    access_denied_delivery_mode = $denied.delivery_mode
    access_denied_response_redacted = ($null -eq $denied.response)
    citation_rejection_status = $llm.citation_rejection_status
    fake_value_rejection_status = $llm.fake_value_rejection_status
    fake_prediction_rejection_status = $llm.fake_prediction_rejection_status
    backend_restart_replay_equal = (Test-SuiteEqual $initial $afterBackendRestart)
    postgres_restart_replay_equal = (Test-SuiteEqual $initial $afterPostgresRestart)
    docker_validation = "PASS"
}

if (
    $result.initial.valuation.intent -ne "VALUATION" -or
    $result.initial.property_comparison.intent -ne "PROPERTY_COMPARISON" -or
    $result.initial.negotiation.intent -ne "NEGOTIATION" -or
    $result.initial.investment.intent -ne "INVESTMENT" -or
    $result.initial.market_insight.intent -ne "MARKET_INSIGHT" -or
    $result.initial.clarification.intent -ne "GENERAL_QUESTION" -or
    $result.initial.clarification.composition_status -ne "CLARIFICATION_REQUIRED" -or
    @($result.initial.property_comparison.tool_names).Count -ne 2 -or
    $result.initial.negotiation.tool_names[0] -ne "negotiation" -or
    $result.initial.investment.tool_names[0] -ne "investment" -or
    $result.initial.market_insight.tool_names[0] -ne "market_insight" -or
    $result.access_denied_status -ne "ACCESS_DENIED" -or
    $result.access_denied_delivery_mode -ne "ACCESS_DENIED" -or
    -not $result.access_denied_response_redacted -or
    $result.citation_rejection_status -ne "REJECT_NARRATION" -or
    $result.fake_value_rejection_status -ne "REJECT_NARRATION" -or
    $result.fake_prediction_rejection_status -ne "REJECT_NARRATION" -or
    -not $result.backend_restart_replay_equal -or
    -not $result.postgres_restart_replay_equal
) {
    $result | ConvertTo-Json -Depth 40
    throw "Copilot Orchestrator runtime Docker validation failed."
}

$result | ConvertTo-Json -Depth 40
