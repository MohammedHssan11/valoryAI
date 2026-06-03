$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$image = "valorai-tool-planner-validation:phase-5-5c-2"

docker build --tag $image ./backend
if ($LASTEXITCODE -ne 0) {
    throw "Tool Planner Docker image build failed."
}

$validationJson = docker run --rm --network none $image python -m app.scripts.validate_tool_planner
if ($LASTEXITCODE -ne 0) {
    throw "Tool Planner standalone Docker validation failed."
}
$validation = $validationJson | ConvertFrom-Json

$result = [ordered]@{
    image = $image
    network_mode = "none"
    database_dependency = $false
    postgis_dependency = $false
    tool_layer_dependency = $false
    router_dependency = $false
    ml_dependency = $false
    cmt_dependency = $false
    llm_dependency = $false
    direct_intent_count = $validation.direct_intent_count
    failed_direct_cases = @($validation.failed_direct_cases)
    property_comparison_tools = @($validation.property_comparison_tools)
    property_comparison_parallel_groups = @($validation.property_comparison_parallel_groups)
    property_comparison_strategy = $validation.property_comparison_strategy
    multi_intent_primary = $validation.multi_intent_primary
    multi_intent_secondary = @($validation.multi_intent_secondary)
    multi_intent_tools = @($validation.multi_intent_tools)
    multi_intent_strategy = $validation.multi_intent_strategy
    clarification_primary = $validation.clarification_primary
    clarification_tools = @($validation.clarification_tools)
    clarification_strategy = $validation.clarification_strategy
    clarification_required = $validation.clarification_required
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
    $result.postgis_dependency -or
    $result.tool_layer_dependency -or
    $result.router_dependency -or
    $result.ml_dependency -or
    $result.cmt_dependency -or
    $result.llm_dependency -or
    $result.direct_intent_count -ne 8 -or
    @($result.failed_direct_cases).Count -ne 0 -or
    @($result.property_comparison_tools).Count -ne 2 -or
    $result.property_comparison_tools[0] -ne "VALUATION_TOOL:PROPERTY_A" -or
    $result.property_comparison_tools[1] -ne "VALUATION_TOOL:PROPERTY_B" -or
    $result.property_comparison_strategy -ne "PARALLEL" -or
    $result.multi_intent_primary -ne "MARKET_INSIGHT" -or
    @($result.multi_intent_secondary).Count -ne 1 -or
    $result.multi_intent_secondary[0] -ne "NEGOTIATION" -or
    @($result.multi_intent_tools).Count -ne 2 -or
    $result.multi_intent_tools[0] -ne "MARKET_INSIGHT_TOOL" -or
    $result.multi_intent_tools[1] -ne "NEGOTIATION_TOOL" -or
    $result.multi_intent_strategy -ne "PARALLEL" -or
    @($result.clarification_tools).Count -ne 0 -or
    $result.clarification_strategy -ne "CLARIFICATION_REQUIRED" -or
    -not $result.clarification_required -or
    $result.deterministic_output_count -ne 1 -or
    $result.forbidden_source_references -ne 0 -or
    $result.forbidden_imports -ne 0 -or
    -not $result.latency_target_passed
) {
    $result | ConvertTo-Json -Depth 10
    throw "Tool Planner Docker validation failed."
}

$result | ConvertTo-Json -Depth 10
