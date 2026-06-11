# ValorAI Tool Planner Architecture Diagram

Report date: 2026-06-01  
Scope: Phase 5.5C.2 only

## Runtime Diagram

```mermaid
flowchart TD
    A["IntentResult"] --> B["Deterministic Tool Planner"]
    B --> C{"Clarification required or LOW confidence?"}
    C -- "Yes" --> D["No Tools selected"]
    D --> E["CLARIFICATION_REQUIRED"]
    C -- "No" --> F["Approved intent-to-Tool map"]
    F --> G{"PROPERTY_COMPARISON?"}
    G -- "Yes" --> H["VALUATION_TOOL:PROPERTY_A"]
    G -- "Yes" --> I["VALUATION_TOOL:PROPERTY_B"]
    G -- "No" --> J["Mapped top-level Tool call"]
    H --> K["PARALLEL group"]
    I --> K
    J --> L{"Multiple independent Tool calls?"}
    L -- "No" --> M["SEQUENTIAL"]
    L -- "Yes" --> K
    E --> N["ExecutionPlan"]
    K --> N
    M --> N
```

## Approved Tool Map

```mermaid
flowchart LR
    V["VALUATION"] --> T1["Tool 1"]
    E["EXPLAINABILITY"] --> T2["Tool 2"]
    C["COMPARABLES"] --> T3["Tool 3"]
    F["FAIRNESS"] --> T4["Tool 4"]
    W["WHAT_IF"] --> T5["Tool 5"]
    N["NEGOTIATION"] --> T6["Tool 6"]
    I["INVESTMENT"] --> T7["Tool 7"]
    M["MARKET_INSIGHT"] --> T8["Tool 8"]
```

## Property Comparison Boundary

```mermaid
flowchart LR
    A["PROPERTY_COMPARISON"] --> B["Tool 1 invocation: PROPERTY_A"]
    A --> C["Tool 1 invocation: PROPERTY_B"]
    B --> D["Future Tool Executor"]
    C --> D
    D -. "Future Phase 5.5C.4" .-> E["Response Composer computes deltas"]
```

There is no Tool 9. The Tool Planner does not compute deltas.

## Phase Boundary

```mermaid
flowchart LR
    A["Phase 5.5C.1 Intent Engine"] --> B["IntentResult"]
    B --> C["Phase 5.5C.2 Tool Planner"]
    C --> D["ExecutionPlan"]
    D -. "Future Phase 5.5C.3" .-> E["Tool Executor"]
    E -. "Future Phase 5.5C.4" .-> F["Response Composer"]
    F -. "Future Phase 5.5C.5" .-> G["Memory Integration"]
    G -. "Future Phase 5.5C.6" .-> H["LLM Integration"]
```

Only the solid-line path through `ExecutionPlan` is implemented in Phase
5.5C.2.

## Governance Boundary

The Tool Planner has no dependency on:

```text
Network
Database
PostGIS
Tool Layer execution
Router
CMT
ML
HTTP clients
LLM providers
```
