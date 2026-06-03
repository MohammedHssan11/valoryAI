# Response Composer Architecture Diagram

Phase: 5.5C.4B Response Composer  
Status: Implemented

## Runtime Flow

```mermaid
flowchart TD
    PLAN["ExecutionPlan"] --> EXEC["Tool Executor"]
    TOOLS["Existing Tools 1-8"] --> EXEC
    EXEC --> RESULT["Extended ExecutionResult<br/>primary_intent<br/>secondary_intents<br/>raw Tool envelopes<br/>structured failures"]
    RESULT --> COMPOSER["Deterministic Response Composer"]
    COMPOSER --> NORMALIZE["Strict known-schema normalization"]
    NORMALIZE --> MATH["Approved arithmetic only<br/>comparison deltas<br/>comparable count / average / min / max"]
    NORMALIZE --> CITE["Received citation ID preservation<br/>and de-duplication"]
    NORMALIZE --> COMPRESS["Bounded compression<br/>Top 3 by distance_km ASC<br/>then comparable_id ASC"]
    MATH --> RESPONSE["ComposedResponse"]
    CITE --> RESPONSE
    COMPRESS --> RESPONSE
    RESPONSE --> CONTEXT["compressed_context<br/>bounded structured data"]
    RESPONSE --> FRONTEND["frontend_payload<br/>complete frontend-safe structured data"]
```

## Boundary

```mermaid
flowchart LR
    ALLOWED["Allowed input<br/>ExecutionResult only"] --> COMPOSER["Response Composer"]
    COMPOSER --> OUTPUT["Allowed output<br/>ComposedResponse only"]
    FORBIDDEN["Forbidden<br/>ExecutionPlan<br/>database<br/>Tool execution<br/>Router / CMT / ML<br/>LLM SDKs<br/>narration<br/>prompt building<br/>SSE / WebSockets"] -. blocked .-> COMPOSER
```

## Governed Responsibilities

| Layer | Responsibility |
| --- | --- |
| Intent Engine | Classifies approved intent vocabulary. |
| Tool Planner | Selects approved Tool slots and execution strategy. |
| Tool Executor | Executes approved Tools and returns raw envelopes. |
| Response Composer | Normalizes, computes approved math, preserves citations, compresses, and emits structured channels. |
| Future Phase 5.5C.6 | May narrate precomputed structured evidence. |

## Locked Rule

```text
Planner decides.
Executor executes.
Composer computes.
Future LLM narrates.
```
