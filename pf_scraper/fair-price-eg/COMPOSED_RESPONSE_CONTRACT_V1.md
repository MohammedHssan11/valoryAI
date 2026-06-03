# ComposedResponse Contract V1

Phase: 5.5C.4A Response Composer Architecture Resolution  
Contract: `ExecutionResult -> ComposedResponse`  
Status: Architecture specification only

## Decision

The Composer accepts exactly one extended `ExecutionResult` and emits exactly
one `ComposedResponse`.

`ExecutionPlan` is not a Composer input.

## Input Contract

Phase 5.5C.4B must extend `ExecutionResult` with intent metadata copied from
the approved plan:

```json
{
  "execution_id": "exec_<uuid>",
  "plan_id": "plan_<digest>",
  "primary_intent": "PROPERTY_COMPARISON",
  "secondary_intents": [],
  "status": "SUCCESS | PARTIAL_SUCCESS | FAILED | CLARIFICATION_REQUIRED",
  "tool_results": [],
  "failed_tools": [],
  "execution_time_ms": 0.0,
  "partial_success": false,
  "audit_metadata": {}
}
```

The Composer must not receive the source `ExecutionPlan`, authenticated user
context, database sessions, or infrastructure clients.

## Output Contract

```json
{
  "response_id": "response_<digest>",
  "execution_id": "exec_<uuid>",
  "plan_id": "plan_<digest>",
  "primary_intent": "PROPERTY_COMPARISON",
  "secondary_intents": [],
  "status": "SUCCESS | PARTIAL_SUCCESS | FAILED | SPARSE_EVIDENCE | CLARIFICATION_REQUIRED",
  "evidence_summary": {
    "tool_summaries": [],
    "property_comparison": null,
    "sparse_evidence": [],
    "evidence_conflicts": [],
    "failed_tools": []
  },
  "citation_package": {
    "valuation_ids": [],
    "tool_event_ids": [],
    "comparable_ids": [],
    "unavailable_optional_citation_types": []
  },
  "compressed_context": {
    "schema_version": "1.0",
    "composition_status": "SUCCESS",
    "intent": {
      "primary": "PROPERTY_COMPARISON",
      "secondary": []
    },
    "evidence": {},
    "failures": [],
    "compression_disclosures": []
  },
  "frontend_payload": {
    "schema_version": "1.0",
    "composition_status": "SUCCESS",
    "tool_outputs": [],
    "failed_tools": [],
    "full_evidence": {},
    "citations": {}
  },
  "composer_metadata": {
    "schema_version": "1.0",
    "composer_mode": "DETERMINISTIC_ONLY",
    "source_execution_status": "SUCCESS",
    "arithmetic_authority": "RESPONSE_COMPOSER",
    "composition_time_ms": 0.0,
    "warnings": []
  }
}
```

## Required Top-Level Fields

| Field | Meaning |
| --- | --- |
| `response_id` | Content-derived Composer trace identifier. |
| `execution_id` | Source executor trace identifier. |
| `plan_id` | Source plan trace identifier copied through `ExecutionResult`. |
| `primary_intent` | Source primary intent copied through `ExecutionResult`. |
| `secondary_intents` | Source secondary intents copied through `ExecutionResult`. |
| `status` | Composer status from the approved five-value taxonomy. |
| `evidence_summary` | Deterministic structured summary of received evidence. |
| `citation_package` | Received canonical and optional citation IDs only. |
| `compressed_context` | Bounded structured context for a future narrator phase. |
| `frontend_payload` | Full frontend-safe structured evidence channel. |
| `composer_metadata` | Composition provenance, timing, and governance markers. |

## Evidence Summary Contract

### Tool Summary

Each successful Tool envelope produces one normalized summary:

```json
{
  "planned_tool": "COMPARABLES_TOOL",
  "tool_name": "comparable",
  "status": "SUCCESS",
  "summary": {}
}
```

`summary` is Tool-specific and may contain received authoritative values plus
Composer-calculated approved statistics.

### Comparable Statistics

When a received evidence array contains usable comparable prices, the Composer
may calculate:

```json
{
  "comparable_count": 3,
  "average_price": 1100000.0,
  "minimum_price": 1000000,
  "maximum_price": 1200000
}
```

Rules:

```text
count = number of usable received comparable price rows
average_price = sum(received prices) / count
minimum_price = minimum received price
maximum_price = maximum received price
average_price is rounded to 4 decimal places
zero usable rows produce count = 0 and null statistics
```

### Property Comparison

When both comparison slots succeed:

```json
{
  "status": "AVAILABLE",
  "property_a": {
    "valuation_id": "val_a",
    "fair_price": 1000000,
    "confidence_level_label": "High"
  },
  "property_b": {
    "valuation_id": "val_b",
    "fair_price": 1200000,
    "confidence_level_label": "Medium"
  },
  "price_delta": 200000,
  "price_percentage_delta": 20.0,
  "confidence_level_label": {
    "property_a": "High",
    "property_b": "Medium"
  }
}
```

When one or both slots fail:

```json
{
  "status": "UNAVAILABLE",
  "unavailable_reason_code": "PROPERTY_COMPARISON_REQUIRES_TWO_SUCCESSFUL_VALUATIONS"
}
```

The V1 comparison object must not contain:

```text
sqm_delta
feature_delta
numeric_confidence_delta
winner
recommendation
```

## Citation Package Contract

```json
{
  "valuation_ids": ["val_<uuid>"],
  "tool_event_ids": [],
  "comparable_ids": ["listing_<id>"],
  "unavailable_optional_citation_types": ["tool_event_id"]
}
```

Rules are defined in:

```text
COMPOSER_CITATION_POLICY.md
```

`audit_id` and `evidence_id` are deferred and must not appear in V1.

## Channel Separation

`compressed_context`:

```text
bounded
Top-N compressed
arithmetic already calculated
structured data only
no prompt text
no transport wrapper
```

`frontend_payload`:

```text
complete frontend-safe normalized evidence
not Top-N truncated
structured data only
no SSE wrapper
no WebSocket wrapper
```

## Response ID And Replay

`response_id` is derived from the SHA-256 digest of one canonical serialization
of the supplied `ExecutionResult`.

Rules:

```text
prefix = response_
digest algorithm = SHA-256
digest input = canonical serialization of the complete supplied ExecutionResult
Composer runtime timing is not included
random ID generation is prohibited
```

Recomposition of the same supplied `ExecutionResult` after restart must emit
the same `response_id`, `execution_id`, and `plan_id`.

The Composer does not persist responses in V1.

## Reason

This contract gives later phases one bounded mathematical-authority object
without passing planning state or infrastructure access into the Composer.

## Alternatives Rejected

Rejected:

```text
passing ExecutionPlan to the Composer
returning raw Tool arrays as future narration context
adding LLM prompt strings
adding generated prose
adding transport wrappers
adding audit_id or evidence_id before their contracts exist
```

## Risks

| Risk | Impact |
| --- | --- |
| Generic Tool summaries can drift if not validated per Tool | Phase 5.5C.4B must use strict known-schema normalizers. |
| Frontend payload can grow large | It must remain frontend-safe and separate from compressed context. |
| Optional citations can be absent | Availability must be disclosed explicitly. |

## Mitigations

```text
normalize known Tools 1-8 only
reject malformed successful envelopes as composition failures
apply bounded compressed-context policies
keep complete safe evidence in frontend_payload
preserve source execution trace IDs
```

## Governance Impact

`ComposedResponse` becomes the sole approved output of Phase 5.5C.4. Future
narration may consume `compressed_context`, but it must not receive raw
arithmetic tasks or replace the Composer as mathematical authority.
