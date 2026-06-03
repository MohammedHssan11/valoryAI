# Execution Result Contract

Phase: 5.5C.3 Tool Executor, extended in Phase 5.5C.4B  
Contract: `ExecutionPlan -> ExecutionResult`

## ExecutionResult

```json
{
  "execution_id": "exec_<uuid>",
  "plan_id": "plan_<digest>",
  "primary_intent": "VALUATION",
  "secondary_intents": [],
  "status": "SUCCESS | PARTIAL_SUCCESS | FAILED | CLARIFICATION_REQUIRED",
  "tool_results": [],
  "failed_tools": [],
  "execution_time_ms": 0.0,
  "partial_success": false,
  "audit_metadata": {
    "executed_tools": [],
    "successful_tools": [],
    "failed_tools": [],
    "execution_strategy": "SEQUENTIAL | PARALLEL | CLARIFICATION_REQUIRED",
    "timeout_seconds": 30.0
  }
}
```

`primary_intent` and `secondary_intents` are copied from `ExecutionPlan` into
`ExecutionResult`. This gives the Response Composer its governed intent
context without passing `ExecutionPlan` across the Composer boundary.

## Successful Tool Envelope

Each `tool_results` item is:

```json
{
  "planned_tool": "VALUATION_TOOL",
  "tool_name": "valuation",
  "payload": {
    "tool_name": "valuation",
    "valuation_id": "val_<uuid>",
    "source": "TruthLayer"
  },
  "execution_time_ms": 0.0,
  "ordering_metadata": {
    "order_index": 0,
    "parallel_group_index": null
  }
}
```

`payload` is the raw Tool Layer response. The executor does not alter,
truncate, summarize, compress, compare, or interpret that object.

## Failed Tool Envelope

Each `failed_tools` item is:

```json
{
  "planned_tool": "VALUATION_TOOL:PROPERTY_B",
  "tool_name": "valuation",
  "error_type": "ToolResourceNotFound",
  "error_message": "Property not found",
  "execution_time_ms": 0.0,
  "ordering_metadata": {
    "order_index": 1,
    "parallel_group_index": 0
  }
}
```

Timeout example:

```json
{
  "planned_tool": "MARKET_INSIGHT_TOOL",
  "tool_name": "market_insight",
  "error_type": "ToolTimeoutError",
  "error_message": "MARKET_INSIGHT_TOOL exceeded the configured timeout",
  "execution_time_ms": 0.0,
  "ordering_metadata": {
    "order_index": 0,
    "parallel_group_index": null
  }
}
```

## Status Semantics

| Status | Meaning |
| --- | --- |
| `SUCCESS` | Every planned Tool slot completed successfully. |
| `PARTIAL_SUCCESS` | At least one planned Tool slot succeeded and at least one failed. |
| `FAILED` | Planned Tool execution produced no successful payload. |
| `CLARIFICATION_REQUIRED` | Planner requested clarification. No Tool executes. |

`partial_success` is `true` whenever any planned Tool slot fails. It marks the
returned payload as incomplete, including total failures such as a timeout.

## Audit Metadata

`audit_metadata` records:

```text
executed_tools
successful_tools
failed_tools
execution_strategy
timeout_seconds
```

Each successful and failed envelope also retains:

```text
order_index
parallel_group_index
```

This keeps property-comparison payloads distinguishable without comparing
their contents.

## Clarification Result

```json
{
  "execution_id": "exec_<uuid>",
  "plan_id": "plan_<digest>",
  "primary_intent": "CLARIFICATION_REQUIRED",
  "secondary_intents": [],
  "status": "CLARIFICATION_REQUIRED",
  "tool_results": [],
  "failed_tools": [],
  "execution_time_ms": 0.0,
  "partial_success": false,
  "audit_metadata": {
    "executed_tools": [],
    "successful_tools": [],
    "failed_tools": [],
    "execution_strategy": "CLARIFICATION_REQUIRED",
    "timeout_seconds": 30.0
  }
}
```

## Governance

The contract deliberately excludes:

```text
property deltas
winners
averages
summaries
compressed payloads
narratives
LLM prompts
execution plans at the Composer boundary
```

Those remain Response Composer or later-phase responsibilities.
