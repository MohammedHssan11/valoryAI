# ValorAI Tool Planner Docker Validation Report

Report date: 2026-06-01  
Validator: `scripts/validate_tool_planner.ps1`  
Decision: **GO**

## Validation Scope

Executed against:

```text
Real backend Docker image
Docker network disabled
Real Intent Engine results
Real approved Tool mapping
Real ExecutionPlan contract
Real deterministic plan ID generation
Real property comparison plan
Real multi-intent plan
Real clarification plan
Real source-boundary scan
Real latency loop
```

Explicitly absent:

```text
PostgreSQL
PostGIS
Tool Layer execution
Router
CMT
ML
OpenAI
Gemini
Anthropic
HTTP clients
External services
```

## Command

```powershell
.\scripts\validate_tool_planner.ps1
```

The script executes:

```text
docker build --tag valorai-tool-planner-validation:phase-5-5c-2 ./backend
docker run --rm --network none \
  valorai-tool-planner-validation:phase-5-5c-2 \
  python -m app.scripts.validate_tool_planner
```

## Result

```text
image:                       valorai-tool-planner-validation:phase-5-5c-2
network_mode:                none
database_dependency:        false
postgis_dependency:         false
tool_layer_dependency:      false
router_dependency:          false
ml_dependency:              false
cmt_dependency:             false
llm_dependency:             false
direct_intent_count:        8
failed_direct_cases:        []
property_comparison_tools:  [VALUATION_TOOL:PROPERTY_A, VALUATION_TOOL:PROPERTY_B]
property_comparison_strategy: PARALLEL
multi_intent_tools:         [MARKET_INSIGHT_TOOL, NEGOTIATION_TOOL]
multi_intent_strategy:      PARALLEL
clarification_tools:        []
clarification_strategy:     CLARIFICATION_REQUIRED
clarification_required:     true
deterministic_output_count: 1
forbidden_references:       0
forbidden_imports:          0
average_latency_ms:         0.009094
latency_target_ms:          1
latency_target_passed:      true
standalone_validation:      PASS
```

## Direct Intent Coverage

The Docker validator plans one real Intent Engine result for every direct
approved mapping:

```text
VALUATION
EXPLAINABILITY
COMPARABLES
FAIRNESS
WHAT_IF
NEGOTIATION
INVESTMENT
MARKET_INSIGHT
```

## Property Comparison Evidence

Input:

```text
Compare these two properties.
```

Result:

```text
tools:     [VALUATION_TOOL:PROPERTY_A, VALUATION_TOOL:PROPERTY_B]
strategy:  PARALLEL
Tool 9:    absent
```

## Multi-Intent Evidence

Input:

```text
What is happening in Mivida and should I negotiate?
```

Result:

```text
primary:    MARKET_INSIGHT
secondary:  NEGOTIATION
tools:      [MARKET_INSIGHT_TOOL, NEGOTIATION_TOOL]
strategy:   PARALLEL
```

## Clarification Evidence

Input:

```text
Tell me more
```

Result:

```text
tools:                  []
strategy:               CLARIFICATION_REQUIRED
requires_clarification: true
```

## Negative Boundary Evidence

The validator parses every Python file in:

```text
backend/app/copilot/orchestrator/planner
```

Only standard-library imports and the local Intent/Planner contracts are
permitted. The scan rejects external provider, network-client, database,
framework, and model-library references.

Result:

```text
forbidden_source_references: 0
forbidden_imports:           0
```

## Latency Evidence

The container runs `20,000` plans for a real multi-intent `IntentResult`.

Measured average:

```text
0.009094 ms
```

Target:

```text
< 1 ms average
```

Result:

```text
PASS
```

## Environment Independence

The Docker run uses:

```text
--network none
```

No Compose services are started. No database container, PostGIS extension,
Tool Layer service, Router request, model file, or external endpoint is
required.

## Remaining Risks

1. The future Tool Executor must interpret comparison invocation slots without
   adding a Tool 9.
2. The future Response Composer must calculate property-comparison deltas; the
   planner intentionally does not compare values.
3. API route wiring remains intentionally deferred.

## GO / NO-GO

**GO for Tool Planner Docker validation.**

The Tool Planner functions inside Docker with no network and no
infrastructure dependencies while meeting its determinism, isolation, and
latency requirements.
