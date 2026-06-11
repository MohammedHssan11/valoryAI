# ValorAI Execution Plan Matrix

Report date: 2026-06-01  
Scope: Phase 5.5C.2 deterministic Tool Planner

## Direct Intent Matrix

| Intent | Selected Tools | Strategy | Reason |
| --- | --- | --- | --- |
| `VALUATION` | `VALUATION_TOOL` | `SEQUENTIAL` | Direct approved Tool 1 mapping |
| `EXPLAINABILITY` | `EXPLAINABILITY_TOOL` | `SEQUENTIAL` | Direct approved Tool 2 mapping |
| `COMPARABLES` | `COMPARABLES_TOOL` | `SEQUENTIAL` | Direct approved Tool 3 mapping |
| `FAIRNESS` | `FAIRNESS_TOOL` | `SEQUENTIAL` | Direct approved Tool 4 mapping |
| `WHAT_IF` | `WHAT_IF_TOOL` | `SEQUENTIAL` | Tool 5 already performs its governed evidence orchestration |
| `NEGOTIATION` | `NEGOTIATION_TOOL` | `SEQUENTIAL` | Tool 6 already orchestrates required evidence |
| `INVESTMENT` | `INVESTMENT_TOOL` | `SEQUENTIAL` | Tool 7 already orchestrates its required evidence chain |
| `MARKET_INSIGHT` | `MARKET_INSIGHT_TOOL` | `SEQUENTIAL` | Direct approved Tool 8 mapping |

## Property Comparison Matrix

| Intent | Selected Tools | Parallel Groups | Strategy | Reason |
| --- | --- | --- | --- | --- |
| `PROPERTY_COMPARISON` | `VALUATION_TOOL:PROPERTY_A`, `VALUATION_TOOL:PROPERTY_B` | `[PROPERTY_A, PROPERTY_B]` | `PARALLEL` | Invoke Tool 1 twice; future Response Composer calculates deltas |

No Tool 9 exists. `PROPERTY_A` and `PROPERTY_B` are invocation slots for the
existing Valuation Tool.

## Multi-Intent Matrix

| Primary Intent | Secondary Intents | Selected Tools | Parallel Groups | Strategy |
| --- | --- | --- | --- | --- |
| `MARKET_INSIGHT` | `NEGOTIATION` | `MARKET_INSIGHT_TOOL`, `NEGOTIATION_TOOL` | `[MARKET_INSIGHT_TOOL, NEGOTIATION_TOOL]` | `PARALLEL` |
| `VALUATION` | `MARKET_INSIGHT` | `VALUATION_TOOL`, `MARKET_INSIGHT_TOOL` | `[VALUATION_TOOL, MARKET_INSIGHT_TOOL]` | `PARALLEL` |
| `PROPERTY_COMPARISON` | `MARKET_INSIGHT` | `VALUATION_TOOL:PROPERTY_A`, `VALUATION_TOOL:PROPERTY_B`, `MARKET_INSIGHT_TOOL` | `[VALUATION_TOOL:PROPERTY_A, VALUATION_TOOL:PROPERTY_B, MARKET_INSIGHT_TOOL]` | `PARALLEL` |

All top-level calls selected for a multi-intent plan are independent. Tool
dependencies internal to Tools 5, 6, and 7 remain encapsulated by those Tools.

## Clarification Matrix

| Condition | Selected Tools | Strategy | Requires clarification |
| --- | --- | --- | --- |
| `requires_clarification = true` | None | `CLARIFICATION_REQUIRED` | `true` |
| `confidence = LOW` | None | `CLARIFICATION_REQUIRED` | `true` |
| `GENERAL_QUESTION` | None | `CLARIFICATION_REQUIRED` | `true` |

## Audit Matrix

| Field | Purpose |
| --- | --- |
| `plan_id` | Stable SHA-256-derived plan identifier for identical `IntentResult` input |
| `reason` | Human-readable deterministic planning decision |
| `selected_tools` | Auditable selected Tool calls |
| `selection_source` | Approved mapping or clarification policy source |
| `intent_source` | Upstream governed classifier source: `INTENT_ENGINE_V1` |
