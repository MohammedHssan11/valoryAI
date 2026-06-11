# Tool Executor Docker Validation Report

Report date: 2026-06-01  
Phase: 5.5C.3 Tool Executor  
Decision: **PASS**

## Runtime

Validation command:

```powershell
.\scripts\validate_tool_executor.ps1
```

The validator:

1. Builds the real backend image.
2. Starts the real PostgreSQL/PostGIS stack and migration bootstrap.
3. Creates JWT-scoped users, workspaces, and properties through authenticated
   Copilot APIs.
4. Runs the Tool Executor inside the backend container against the real Tool
   Layer.
5. Restarts the backend and reruns executor validation.
6. Restarts PostgreSQL and the backend and reruns executor validation.

## Result

```text
docker_validation:                         PASS
executor_only:                             true
sequential_status:                         SUCCESS
sequential_raw_payload_source:             TruthLayer
parallel_status:                           SUCCESS
parallel_concurrency_proven:               true
parallel_execution_time_ms:                378.997
parallel_runtime_total_ms:                 672.039
sequential_overhead_ms:                    1.427
parallel_overhead_ms:                      2.190
overhead_target_ms:                        10
multi_intent_status:                       SUCCESS
property_comparison_payload_count:         2
property_comparison_raw_payloads_preserved:true
clarification_status:                      CLARIFICATION_REQUIRED
timeout_status:                            FAILED
timeout_partial_success:                   true
timeout_error_type:                        ToolTimeoutError
partial_failure_status:                    PARTIAL_SUCCESS
partial_success:                           true
partial_error_type:                        ToolResourceNotFound
tenant_isolation_status:                   FAILED
tenant_isolation_error_type:               ToolResourceNotFound
audit_execution_id_present:                true
audit_plan_id_matches:                     true
tool_event_count_before_restart:           11
backend_restart_status:                    SUCCESS
tool_event_count_after_backend_restart:    22
postgres_restart_status:                   SUCCESS
tool_event_count_after_postgres_restart:   33
forbidden_source_references:               0
forbidden_imports:                         0
direct_queries_found:                      false
```

## Validated Behavior

Passed:

```text
Sequential Tool 1 execution
Parallel Tool 1 property-comparison execution
Parallel Tool 8 plus Tool 6 multi-intent execution
Raw Tool payload preservation
Planner ordering metadata preservation
Configurable timeout failure
Partial failure isolation
JWT-created tenant state
Cross-tenant concealment through existing Tool Layer checks
Execution ID and plan ID auditability
Backend restart recovery
PostgreSQL restart recovery
Executor source boundary scan
< 10 ms executor overhead target
```

## Live PostGIS Pytest Evidence

Dedicated executor suite:

```text
2 passed
```

Adjacent Tools 3-8 plus executor sweep:

```text
11 passed
```

The local pytest environment executed against the running Docker
PostgreSQL/PostGIS service. The production-style backend image does not ship
with `pytest`; the standalone validator itself ran inside that image.

## Boundary Scan

The executor package contains:

```text
No OpenAI import
No Gemini import
No Anthropic import
No embedding import
No ML import
No Response Composer logic
No property comparison arithmetic
No evidence summarization
No payload truncation or compression
No direct database query
```

## Final Result

**PASS.**

Planner decides. Executor runs. Composer remains a future phase.
