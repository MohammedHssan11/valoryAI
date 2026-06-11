# MemoryContext Contract

Phase: 5.5C.5 Memory Integration  
Schema version: `1.0`

## Contract

```text
MemoryContext
  memory_id: string
  status: MemoryStatus
  workspace_context: object
  scenario_context: object | null
  broker_session_context: object | null
  recent_tool_history: object[]
  recent_decisions: object[]
  recent_valuations: object[]
  active_assumptions: object[]
  active_comparison_context: object | null
  recent_conversation_metadata: object[]
  citation_package: object
  memory_metadata: object
```

## Memory ID

`memory_id` is:

```text
memory_<sha256(canonical JSON context)>
```

Canonical JSON uses sorted keys, stable persisted ordering, and no retrieval
timestamp. Identical persisted state rebuilds the same `memory_id`.

## Status

| Status | Meaning |
| --- | --- |
| `SUCCESS` | Owned bounded context rebuilt successfully. |
| `PARTIAL_SUCCESS` | Context rebuilt, but the latest remembered composition was partial or failed. |
| `FAILED` | Runtime mismatch or persistence failure. |
| `EMPTY_CONTEXT` | Owned active workspace exists but has no material memory context. |
| `ACCESS_DENIED` | Requested workspace, scenario, or broker-session scope is unavailable or mismatched. |

`FAILED` and `ACCESS_DENIED` return empty fail-closed payloads.

## Governed Limits

| Context slice | Limit | Ordering |
| --- | ---: | --- |
| Recent Tool history | 10 | `tool_events.id DESC` |
| Recent decisions | 10 | `decision_history.id DESC` |
| Recent valuations | 5 | `created_at DESC`, `valuation_id DESC` |
| Active assumptions | 20 | `assumptions.id DESC` |
| Recent conversation metadata | 10 | `messages.created_at DESC`, `messages.id DESC` |
| Scenario lineage | 10 | Current scenario ancestry |

## Citation Package

```text
workspace_id
scenario_id
valuation_ids
tool_event_ids
comparable_ids
```

Only persisted or received identifiers are preserved. The Memory Layer does
not fabricate citations.

## Remember Hook

```text
remember(
  user_id,
  workspace_id,
  scenario_id?,
  broker_session_id?,
  execution_result,
  composed_response
) -> MemoryContext
```

The hook validates the Composer and Executor identifiers, writes one
idempotent bounded `decision_history` summary, then rebuilds `MemoryContext`.

## Load Hook

```text
load_context(
  user_id,
  workspace_id,
  scenario_id?,
  broker_session_id?
) -> MemoryContext
```

The load hook reconstructs context from existing persistence only.

## Layer Ownership

```text
Intent Engine        owns IntentResult
Tool Planner         owns ExecutionPlan
Tool Executor        owns ExecutionResult
Response Composer    owns ComposedResponse
Memory Integration  owns MemoryContext
```

`MemoryContext` is downstream structured context. It does not replace,
mutate, or reinterpret the upstream contracts.
