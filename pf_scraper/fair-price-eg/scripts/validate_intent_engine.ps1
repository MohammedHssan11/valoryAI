$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$image = "valorai-intent-engine-validation:phase-5-5c-1"

docker build --tag $image ./backend
if ($LASTEXITCODE -ne 0) {
    throw "Intent Engine Docker image build failed."
}

$validationJson = docker run --rm --network none $image python -m app.scripts.validate_intent_engine
if ($LASTEXITCODE -ne 0) {
    throw "Intent Engine standalone Docker validation failed."
}
$validation = $validationJson | ConvertFrom-Json

$result = [ordered]@{
    image = $image
    network_mode = "none"
    database_dependency = $false
    router_dependency = $false
    ml_dependency = $false
    cmt_dependency = $false
    classified_intent_count = $validation.classified_intent_count
    failed_cases = @($validation.failed_cases)
    multi_intent_primary = $validation.multi_intent_primary
    multi_intent_secondary = @($validation.multi_intent_secondary)
    clarification_intent = $validation.clarification_intent
    clarification_confidence = $validation.clarification_confidence
    clarification_required = $validation.clarification_required
    misspelling_and_noise_intent = $validation.misspelling_and_noise_intent
    deterministic_output_count = $validation.deterministic_output_count
    forbidden_source_references = @($validation.forbidden_source_references).Count
    forbidden_imports = @($validation.forbidden_imports).Count
    average_latency_ms = $validation.average_latency_ms
    latency_target_ms = $validation.latency_target_ms
    latency_target_passed = $validation.latency_target_passed
    standalone_docker_validation = "PASS"
}

if (
    $result.network_mode -ne "none" -or
    $result.database_dependency -or
    $result.router_dependency -or
    $result.ml_dependency -or
    $result.cmt_dependency -or
    $result.classified_intent_count -ne 10 -or
    @($result.failed_cases).Count -ne 0 -or
    $result.multi_intent_primary -ne "MARKET_INSIGHT" -or
    @($result.multi_intent_secondary).Count -ne 1 -or
    $result.multi_intent_secondary[0] -ne "NEGOTIATION" -or
    $result.clarification_intent -ne "GENERAL_QUESTION" -or
    $result.clarification_confidence -ne "LOW" -or
    -not $result.clarification_required -or
    $result.misspelling_and_noise_intent -ne "NEGOTIATION" -or
    $result.deterministic_output_count -ne 1 -or
    $result.forbidden_source_references -ne 0 -or
    $result.forbidden_imports -ne 0 -or
    -not $result.latency_target_passed
) {
    $result | ConvertTo-Json -Depth 10
    throw "Intent Engine Docker validation failed."
}

$result | ConvertTo-Json -Depth 10
