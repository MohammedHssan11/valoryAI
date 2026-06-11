# Response Composer Docker Validation Report

Report date: 2026-06-01  
Phase: 5.5C.4B Response Composer  
Decision: **PASS**

## Runtime

Validation command:

```powershell
.\scripts\validate_response_composer.ps1
```

The validator:

1. Builds the real backend image.
2. Starts the real PostgreSQL/PostGIS stack and migration bootstrap.
3. Creates JWT-scoped users, workspaces, and properties through authenticated
   Copilot APIs.
4. Runs the real Tool Layer and Tool Executor inside the backend container.
5. Composes real property comparison, comparable, negotiation, investment,
   market insight, multi-intent, sparse, partial-failure, full-failure, and
   clarification results.
6. Replays a serialized `ExecutionResult` after backend restart.
7. Replays the same result after PostgreSQL and backend restart.
8. Runs live PostGIS integration tests from the host against the Docker
   database. The lean backend image intentionally does not ship with `pytest`.

## Result

```text
docker_validation:                    PASS
composer_only:                        true
comparison_status:                    SUCCESS
comparison_arithmetic_valid:          true
comparison_prohibited_fields:         0
deterministic_output_count:           1
citation_valuation_count:             1
citation_comparable_count:            5
compressed_top_comparable_count:      3
frontend_comparable_count:            5
dual_channel_delivery:                true
negotiation_status:                   SUCCESS
investment_status:                    SUCCESS
market_status:                        SUCCESS
multi_intent_status:                  SUCCESS
sparse_status:                        SPARSE_EVIDENCE
partial_status:                       PARTIAL_SUCCESS
failed_status:                        FAILED
clarification_status:                 CLARIFICATION_REQUIRED
average_latency_ms:                   0.053627
latency_target_ms:                    15
latency_target_passed:                true
backend_restart_replay_equal:         true
postgres_restart_replay_equal:        true
forbidden_source_references:          0
forbidden_imports:                    0
direct_queries_found:                 false
live_postgis_integration_tests:       PASS
```

The real Docker comparison happened to produce equal Tool 1 fair prices, so
its approved arithmetic was:

```text
price_delta:            0
price_percentage_delta: 0.0
```

The deterministic unit contract also validates a non-zero case:

```text
price_delta:            250000
price_percentage_delta: 25.0
```

## Restart Determinism

The same serialized `ExecutionResult` emitted the same complete
`ComposedResponse` and the same content-derived response identifier after both
restart paths:

```text
response_c2bbe2d553192917ac845ac611eaf2f4be5af45adc9eea8d145e0b9d7e89fb44
```

## Live PostGIS Evidence

Composer plus Executor integration suite in the Docker harness:

```text
4 passed
```

Adjacent Tools 3-8, Executor, and Composer sweep:

```text
13 passed
```

Existing Tool Executor Docker regression validator:

```text
PASS
```

## Boundary Scan

The Composer package contains:

```text
No database access
No direct query
No Tool execution
No Router invocation
No CMT invocation
No ML invocation
No OpenAI import
No Gemini import
No Anthropic import
No LLM SDK
No embedding dependency
No narration
No prompt building
No SSE wrapper
No WebSocket wrapper
```

## Final Result

**PASS.**

The real Docker/PostGIS flow proves deterministic structured composition while
preserving the locked phase boundary.
