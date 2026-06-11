# ValorAI Intent Engine V1 Architecture Diagram

Report date: 2026-06-01  
Scope: Phase 5.5C.1 only

## Runtime Diagram

```mermaid
flowchart TD
    A["User Message"] --> B["Intent Engine V1"]
    B --> C["Unicode NFKC normalization"]
    C --> D["Case folding and whitespace collapse"]
    D --> E["Whole-keyword deterministic rule matching"]
    E --> F["Per-intent evidence aggregation"]
    F --> G["Deterministic ranking"]
    G --> H["Primary Intent"]
    G --> I["Safe Secondary Intents"]
    H --> J["IntentResult"]
    I --> J
    J --> K["intent"]
    J --> L["confidence"]
    J --> M["matched_rules"]
    J --> N["matched_keywords"]
    J --> O["requires_clarification"]
    J --> P["reason"]
    J --> Q["secondary_intents"]
```

## Clarification Branch

```mermaid
flowchart LR
    A["Normalized message"] --> B{"Governed rule matched?"}
    B -- "Yes" --> C["Return deterministic intent result"]
    B -- "No" --> D["GENERAL_QUESTION"]
    D --> E["confidence = LOW"]
    E --> F["requires_clarification = true"]
```

## Scope Boundary

```mermaid
flowchart LR
    A["User Message"] --> B["Phase 5.5C.1 Intent Engine"]
    B --> C["IntentResult"]
    C -. "Future Phase 5.5C.2" .-> D["Tool Planner"]
    D -. "Future Phase 5.5C.3" .-> E["Tool Executor"]
    E -. "Future Phase 5.5C.4" .-> F["Response Composer"]
    F -. "Future Phase 5.5C.5" .-> G["Memory Integration"]
    G -. "Future Phase 5.5C.6" .-> H["LLM Integration"]
```

Only the solid-line path is implemented in Phase 5.5C.1.

## Governance Boundary

The Intent Engine has no dependency on:

```text
Network
Database
Router
CMT
ML
Embeddings
Vector database
Tool Layer
LLM providers
```
