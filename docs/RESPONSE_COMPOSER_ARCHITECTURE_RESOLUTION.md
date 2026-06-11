# ValorAI Phase 5.5C.4A Response Composer Architecture Resolution

Resolution date: 2026-06-01  
Scope: Architecture resolution only  
Decision: **APPROVED FOR PHASE 5.5C.4B IMPLEMENTATION REVIEW**

## Decision

Phase 5.5C.4A resolves the Response Composer architecture. It does not
authorize implementation.

The approved pipeline is:

```text
Intent Engine
  -> Tool Planner
  -> Tool Executor
  -> ExecutionResult
  -> Response Composer
  -> ComposedResponse
```

The Response Composer is a pure deterministic transformation boundary. It
accepts one `ExecutionResult` and emits one `ComposedResponse`.

The Composer may:

```text
normalize received Tool payloads
preserve received citation identifiers
calculate approved arithmetic
calculate Property Comparison V1 price deltas
aggregate evidence statistics
compress the future narration-safe context channel
preserve complete frontend-safe evidence in a separate structured channel
normalize failures and sparse-evidence disclosures
```

The Composer must not:

```text
execute Tools
receive ExecutionPlan
classify intents
plan Tool calls
query PostgreSQL or PostGIS
call Router, CMT, or ML
call HTTP services
call LLM providers
generate prompts
generate narrative language
stream events
write frontend integration code
persist ComposedResponse artifacts
```

## Resolved Architecture

### ExecutionResult Extension

`ExecutionResult` must be extended in Phase 5.5C.4B with:

```text
primary_intent
secondary_intents
```

The executor already receives `ExecutionPlan`. It must copy the approved
intent metadata into `ExecutionResult` without reinterpretation.

`ExecutionPlan` is not a Composer input.

### Property Comparison V1

Property Comparison V1 is intentionally narrow:

```text
price_delta
price_percentage_delta
confidence_level_label
```

The Composer uses only the two received Tool 1 payloads:

```text
VALUATION_TOOL:PROPERTY_A
VALUATION_TOOL:PROPERTY_B
```

The following metrics are prohibited in V1:

```text
sqm_delta
feature_delta
numeric_confidence_delta
winner
recommendation
```

### Citation Policy

Approved citation types:

| Citation | Policy |
| --- | --- |
| `valuation_id` | Canonical valuation citation. |
| `tool_event_id` | Optional pass-through citation when received. |
| `comparable_id` | Optional pass-through citation when received. |
| `audit_id` | Deferred. |
| `evidence_id` | Deferred. |

The Composer must not query a database, fabricate IDs, or introduce a new
citation system.

### Frontend Channel

`frontend_payload` is a pure structured data object.

It is not:

```text
an SSE event
a WebSocket message
a streaming wrapper
a chat response
```

Frontend transport and integration are deferred.

### Compression Comparator

Comparable Top-N selection uses:

```text
Primary sort: distance_km ASC
Tie-break:    comparable_id ASC
Limit:        3
```

Rows without a usable `distance_km` or canonical comparable identifier remain
available in the frontend evidence channel but are ineligible for compressed
Top-N selection.

### Composer Statuses

The complete V1 status taxonomy is:

```text
SUCCESS
PARTIAL_SUCCESS
FAILED
SPARSE_EVIDENCE
CLARIFICATION_REQUIRED
```

Detailed precedence is defined in:

```text
COMPOSER_FAILURE_SEMANTICS.md
```

### Restart Recovery

The Composer is stateless. Restart recovery means deterministic recomposition
from a supplied `ExecutionResult`, including the same content-derived
`response_id`.

Phase 5.5C.4 does not introduce Composer persistence, database reads, or
recovery storage.

## Resolution Matrix

| Blocker | Approved resolution |
| --- | --- |
| Missing intents in `ExecutionResult` | Extend `ExecutionResult` with primary and secondary intents. |
| Unavailable comparison fields | Reduce Property Comparison V1 to price deltas and confidence labels. |
| Unavailable citations | Preserve only received canonical and optional identifiers. Defer audit and evidence IDs. |
| LLM responsibility conflict | Remove all LLM, narration, prompt, and streaming responsibilities from Phase 5.5C.4. |
| Frontend contract ambiguity | Emit a structured `frontend_payload` object only. |
| Top-N ordering ambiguity | Sort by `distance_km ASC`, then `comparable_id ASC`. |
| Failure semantics ambiguity | Use the approved five-status taxonomy and deterministic precedence. |

## Reason

The resolved design protects the mathematical-authority boundary without
expanding the Tool Layer or allowing the Composer to recover missing data from
infrastructure. It makes the future narrator a consumer of locked structured
context, not a calculator or evidence retriever.

## Alternatives Rejected

Rejected:

```text
passing ExecutionPlan into the Composer
extending Tool 1 for Property Comparison V1
creating Tool 9
querying persisted snapshots or Tool events from the Composer
inventing audit IDs or evidence IDs
adding LLM orchestration to the Composer
adding SSE or WebSocket wrappers
sorting comparables by an unexposed relevance score
persisting Composer output in Phase 5.5C.4
```

## Risks

| Risk | Impact |
| --- | --- |
| V1 comparison is intentionally limited | Users cannot receive size, feature, or numeric confidence deltas from this phase. |
| Optional citation coverage may be incomplete | Tool events and comparable IDs may be absent from some received payloads. |
| Compression can hide lower-ranked evidence from future narration | The frontend channel must retain full safe evidence. |
| Content-derived response IDs depend on canonical serialization | Phase 5.5C.4B must define one stable serialization before hashing. |

## Mitigations

```text
disclose unavailable comparison metrics explicitly
preserve full frontend-safe evidence independently of compressed context
surface optional citation availability metadata
apply one governed Top-N comparator
preserve structured failures and sparse-evidence markers
keep Phase 5.5C.4B implementation isolated from infrastructure dependencies
```

## Governance Impact

This resolution supersedes conflicting Phase 5.5C draft language that assigned
LLM prompt assembly, LLM invocation, narration, SSE citation events, or final
Broker response assembly to the Composer.

Those responsibilities remain deferred to later phases, including Phase
5.5C.6 for LLM integration.

## Authorization Boundary

Phase 5.5C.4A is complete when the six resolution documents are approved.

Do not implement Response Composer production code, tests, Docker validators,
or runtime wiring until Phase 5.5C.4B receives explicit approval.
