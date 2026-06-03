# Memory Architecture Diagram

Phase: 5.5C.5 Memory Integration  
Status: Implemented

## Runtime Flow

```mermaid
flowchart TD
    COMPOSER["ComposedResponse"] --> REMEMBER["Deterministic Memory Integration"]
    EXECUTION["ExecutionResult"] --> REMEMBER
    SCOPE["JWT-owned workspace<br/>optional scenario<br/>optional broker session"] --> REMEMBER
    REMEMBER --> AUDIT["Existing decision_history<br/>idempotent bounded summary"]
    AUDIT --> LOAD["Deterministic context rebuild"]
    SQL["Existing PostgreSQL persistence<br/>workspaces / chats / messages<br/>property_states / scenario_states<br/>assumptions / decision_history<br/>tool_events / broker_sessions<br/>valuation_snapshots"] --> LOAD
    LOAD --> CONTEXT["MemoryContext<br/>restart-stable memory_id"]
    CONTEXT --> FUTURE["Future LLM Layer"]
```

## Orchestrator Placement

```mermaid
flowchart LR
    USER["User message"] --> INTENT["Intent Engine<br/>IntentResult"]
    INTENT --> PLANNER["Tool Planner<br/>ExecutionPlan"]
    PLANNER --> EXECUTOR["Tool Executor<br/>ExecutionResult"]
    EXECUTOR --> COMPOSER["Response Composer<br/>ComposedResponse"]
    COMPOSER --> MEMORY["Memory Integration<br/>MemoryContext"]
    MEMORY --> FUTURE["Future LLM narration"]
```

The direction is forward-only. Memory Integration does not classify intent,
plan work, execute Tools, or compute response arithmetic.

## Scoped Retrieval

```mermaid
flowchart LR
    JWT["Authenticated user_id"] --> WS["Active owned workspace"]
    WS --> SCENARIO["Optional active owned scenario"]
    SCENARIO --> PROPERTY["Scenario property"]
    SCENARIO --> BROKER["Optional matching broker session"]
    WS --> BOUNDED["Bounded recent persistence slices"]
    PROPERTY --> BOUNDED
    BROKER --> BOUNDED
    BOUNDED --> MEMORY["MemoryContext"]
    DENY["Foreign / deleted / mismatched scope"] -. fail closed .-> EMPTY["ACCESS_DENIED<br/>empty disclosure"]
```

## Boundary

```text
Planner decides.
Executor executes.
Composer computes.
Memory remembers.
Future LLM narrates.
```

Memory does not call Tools, Router, CMT, ML, model providers, vector stores,
prompt builders, narration, streaming, or frontend transport.
