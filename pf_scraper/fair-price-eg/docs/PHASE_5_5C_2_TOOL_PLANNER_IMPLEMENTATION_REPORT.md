# ValorAI Phase 5.5C.2 Tool Planner Implementation Report

Report date: 2026-06-01  
Scope: Tool Planner only  
Decision: **GO**

## Executive Result

Implemented only:

```text
IntentResult
  -> deterministic Tool Planner
  -> ExecutionPlan
```

The Tool Planner creates plans. It does not execute, call, import, or inspect
Tools 1-8. It has no network, database, Router, CMT, ML, HTTP-client, or LLM
dependency.

## Scope Boundary

Implemented:

```text
Approved intent-to-Tool mapping
Deterministic plan IDs
Sequential plans
Parallel plans
Clarification-required plans
Property comparison planning through two Tool 1 invocation slots
Multi-intent planning
Auditable selection metadata
```

Not implemented:

```text
Tool Executor
Tool invocation
Response Composer
Property comparison arithmetic
Memory Integration
LLM Integration
Frontend Integration
API route wiring
```

## Contract

`ExecutionPlan` returns:

```text
plan_id
primary_intent
secondary_intents
tools
parallel_groups
execution_strategy
requires_clarification
reason
selected_tools
selection_source
intent_source
```

Strategies:

```text
SEQUENTIAL
PARALLEL
CLARIFICATION_REQUIRED
```

`plan_id` is derived from a canonical serialization of the complete
`IntentResult` using SHA-256. No random ID generator is used.

## Approved Tool Mapping

```text
VALUATION       -> VALUATION_TOOL
EXPLAINABILITY  -> EXPLAINABILITY_TOOL
COMPARABLES     -> COMPARABLES_TOOL
FAIRNESS        -> FAIRNESS_TOOL
WHAT_IF         -> WHAT_IF_TOOL
NEGOTIATION     -> NEGOTIATION_TOOL
INVESTMENT      -> INVESTMENT_TOOL
MARKET_INSIGHT  -> MARKET_INSIGHT_TOOL
```

`NEGOTIATION` selects only Tool 6 because Tool 6 already orchestrates its
required evidence. `INVESTMENT` selects only Tool 7 for the same reason.

## Property Comparison

No Tool 9 exists or was added.

```text
PROPERTY_COMPARISON
  -> VALUATION_TOOL:PROPERTY_A
  -> VALUATION_TOOL:PROPERTY_B
  -> PARALLEL
```

The two values are explicit Tool 1 invocation slots. The future Response
Composer remains responsible for deterministic comparison arithmetic.

## Multi-Intent Planning

Input:

```text
What is happening in Mivida and should I negotiate?
```

Plan:

```text
primary_intent:      MARKET_INSIGHT
secondary_intents:  [NEGOTIATION]
tools:              [MARKET_INSIGHT_TOOL, NEGOTIATION_TOOL]
parallel_groups:    [[MARKET_INSIGHT_TOOL, NEGOTIATION_TOOL]]
strategy:           PARALLEL
```

## Clarification Planning

Low-confidence or clarification-requested input returns:

```text
tools:                  []
parallel_groups:        []
execution_strategy:     CLARIFICATION_REQUIRED
requires_clarification: true
```

`GENERAL_QUESTION` also produces a clarification plan because it has no
approved Tool mapping.

## Auditability

Every plan records:

```text
reason
selected_tools
selection_source
intent_source
```

Selection sources:

```text
APPROVED_TOOL_MAP
APPROVED_TOOL_MAP+APPROVED_PROPERTY_COMPARISON_PATTERN
CLARIFICATION_POLICY
```

## Files Created

```text
backend/app/copilot/orchestrator/planner/__init__.py
backend/app/copilot/orchestrator/planner/contracts.py
backend/app/copilot/orchestrator/planner/planner.py
backend/app/tests/test_tool_planner.py
backend/app/scripts/validate_tool_planner.py
scripts/validate_tool_planner.ps1
PHASE_5_5C_2_TOOL_PLANNER_IMPLEMENTATION_REPORT.md
TOOL_PLANNER_DOCKER_VALIDATION_REPORT.md
TOOL_PLANNER_ARCHITECTURE_DIAGRAM.md
EXECUTION_PLAN_MATRIX.md
```

Updated:

```text
../../PROJECT_MASTER_STATE_V2.md
```

## Local Validation

Focused planner suite:

```text
python -m pytest -p no:cacheprovider app/tests/test_tool_planner.py -q
20 passed
```

Intent Engine plus planner regression:

```text
python -m pytest -p no:cacheprovider \
  app/tests/test_intent_engine.py \
  app/tests/test_tool_planner.py -q
49 passed
```

Standalone local validator:

```text
python -m app.scripts.validate_tool_planner
direct_intent_count:           8
failed_direct_cases:           []
property_comparison_strategy:  PARALLEL
multi_intent_strategy:         PARALLEL
clarification_strategy:        CLARIFICATION_REQUIRED
deterministic_output_count:    1
forbidden_source_references:   []
forbidden_imports:             []
average_latency_ms:            0.010778
latency_target_passed:         true
```

Compilation:

```text
python -m compileall -q app
PASS
```

## Docker Evidence

Dedicated validator:

```powershell
.\scripts\validate_tool_planner.ps1
```

The validator builds the real backend image and executes:

```text
docker run --rm --network none
```

Key result:

```text
network_mode:                 none
database_dependency:         false
postgis_dependency:          false
tool_layer_dependency:       false
router_dependency:           false
ml_dependency:               false
cmt_dependency:              false
llm_dependency:              false
direct_intent_count:         8
failed_direct_cases:         []
property_comparison_strategy: PARALLEL
multi_intent_strategy:       PARALLEL
clarification_strategy:      CLARIFICATION_REQUIRED
deterministic_output_count:  1
forbidden_source_references: 0
forbidden_imports:           0
average_latency_ms:          0.009094
latency_target_ms:           1
latency_target_passed:       true
```

Detailed report:

```text
TOOL_PLANNER_DOCKER_VALIDATION_REPORT.md
```

## GO / NO-GO

**GO for Phase 5.5C.2 Tool Planner.**

The planner is deterministic, auditable, executor-free, infrastructure-free,
property-comparison capable, multi-intent capable, clarification-aware, and
comfortably below the `< 1 ms` average latency target.
