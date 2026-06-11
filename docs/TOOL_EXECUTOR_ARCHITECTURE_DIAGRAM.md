# Tool Executor Architecture Diagram

Phase: 5.5C.3  
Scope: Tool Executor only

## Main Flow

```text
IntentResult
  -> Deterministic Tool Planner
  -> ExecutionPlan
       plan_id
       tools
       parallel_groups
       execution_strategy
  -> Deterministic Tool Executor
       if CLARIFICATION_REQUIRED
         -> execute nothing
       else
         -> validate invocation-slot inputs
         -> run sequentially or concurrently
         -> isolate failures and timeouts
         -> preserve raw Tool responses
  -> ExecutionResult
       execution_id
       plan_id
       status
       tool_results
       failed_tools
       execution_time_ms
       partial_success
       audit_metadata
  -> Response Composer (future)
```

## Approved Dispatch

```text
Deterministic Tool Executor
  -> CopilotToolInvoker
       -> isolated database session per invocation
       -> existing CopilotToolsService
            -> Tool 1 Valuation
            -> Tool 2 Explainability
            -> Tool 3 Comparable
            -> Tool 4 Fairness
            -> Tool 5 What-if
            -> Tool 6 Negotiation
            -> Tool 7 Investment
            -> Tool 8 Market Insight
```

## Property Comparison

```text
ExecutionPlan: PARALLEL
  -> VALUATION_TOOL:PROPERTY_A
       -> Tool 1
       -> raw valuation payload A
  -> VALUATION_TOOL:PROPERTY_B
       -> Tool 1
       -> raw valuation payload B

ExecutionResult
  -> raw valuation payload A
  -> raw valuation payload B

No comparison arithmetic occurs in the executor.
```

## Parallel Multi-Intent

```text
ExecutionPlan: PARALLEL
  -> MARKET_INSIGHT_TOOL
       -> Tool 8
  -> NEGOTIATION_TOOL
       -> Tool 6

ExecutionResult
  -> raw Tool 8 payload
  -> raw Tool 6 payload
```

## Failure Isolation

```text
Parallel group
  -> Tool A succeeds
       -> raw payload retained
  -> Tool B fails or times out
       -> structured failure retained

ExecutionResult
  -> status = PARTIAL_SUCCESS
  -> partial_success = true
```

## Boundary

```text
Allowed:
  execute approved plans
  invoke approved Tools 1-8
  preserve raw payloads
  collect timing and ordering metadata
  isolate errors and timeouts

Forbidden:
  compare property values
  calculate real-estate metrics
  summarize evidence
  compress payloads
  generate narratives
  call LLMs
```
