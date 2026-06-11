# Response Composer Failure Semantics

Phase: 5.5C.4A Response Composer Architecture Resolution  
Status: Architecture specification only

## Decision

The Response Composer uses exactly five top-level statuses:

```text
SUCCESS
PARTIAL_SUCCESS
FAILED
SPARSE_EVIDENCE
CLARIFICATION_REQUIRED
```

## Status Precedence

Apply the first matching rule:

| Priority | Status | Rule |
| --- | --- | --- |
| 1 | `CLARIFICATION_REQUIRED` | Source `ExecutionResult.status` is `CLARIFICATION_REQUIRED`. |
| 2 | `FAILED` | No successful Tool envelope remains after normalization. |
| 3 | `PARTIAL_SUCCESS` | At least one Tool slot failed, at least one successful Tool envelope remains, or a material evidence conflict prevents a complete compressed summary. |
| 4 | `SPARSE_EVIDENCE` | Execution otherwise succeeded and an applicable V1 sparse-evidence rule matches. |
| 5 | `SUCCESS` | Execution succeeded and no preceding rule matches. |

Sparse-evidence markers must still be preserved inside `evidence_summary` when
a higher-priority `PARTIAL_SUCCESS` status applies.

## Normalized Failure Shape

```json
{
  "planned_tool": "VALUATION_TOOL:PROPERTY_B",
  "tool_name": "valuation",
  "error_type": "ToolResourceNotFound",
  "failure_category": "TOOL_FAILURE",
  "ordering_metadata": {
    "order_index": 1,
    "parallel_group_index": 0
  }
}
```

The Composer preserves structured failure facts. It must not generate prose
or expose arbitrary internal exception text in `compressed_context`.

Approved failure categories:

```text
TOOL_FAILURE
TOOL_TIMEOUT
MISSING_TOOL_INPUT
COMPOSER_NORMALIZATION_FAILURE
```

## Sparse Evidence Rules

The Composer does not invent new business thresholds. It uses received
zero-evidence counts and Tool-owned sparse markers only.

| Tool payload | Sparse-evidence condition |
| --- | --- |
| Comparable Tool | `comparable_count == 0` |
| What-if Tool | `comparables.comparable_count == 0` |
| Negotiation Tool | `comparable_summary.comparable_count == 0` |
| Investment Tool | `comparable_summary.comparable_count == 0` |
| Market Insight Tool | `valuation_volume == 0` |
| Market Insight Tool | `comparable_density.density_level` is `Sparse` or `Insufficient Evidence` |

The following do not independently promote the whole response to
`SPARSE_EVIDENCE`:

```text
an absent optional tool_event_id
an absent optional comparable_id
Investment Tool optional what_if_summary.status = Insufficient Evidence
an empty Explainability Tool comparable_evidence array on an ML-backed result
```

Those conditions remain structured disclosures.

## Missing Evidence

If a successful Tool envelope lacks fields required by its V1 normalizer:

```text
record COMPOSER_NORMALIZATION_FAILURE
exclude the malformed envelope from approved arithmetic
preserve safe failure metadata
derive the final status using the standard precedence
```

The Composer must not guess missing fields, query infrastructure, or call a
Tool to repair the payload.

## Conflicting Evidence

The Composer is not a business-logic adjudicator.

V1 may flag a material conflict only when received payloads attach different
authoritative scalar values to the same canonical `valuation_id` and field.

Example:

```json
{
  "valuation_id": "val_123",
  "field": "fair_price",
  "received_values": [1000000, 1200000],
  "resolution": "UNRESOLVED"
}
```

Rules:

```text
preserve both received values in frontend_payload
do not choose a winner
do not average conflicting values
do not use the conflicted field for compressed arithmetic
record the conflict in evidence_summary.evidence_conflicts
emit PARTIAL_SUCCESS if the conflict affects compressed output
```

## Property Comparison Failure

| Slot result | Composition behavior |
| --- | --- |
| Both Tool 1 slots succeed | Calculate approved Property Comparison V1 fields. |
| One slot succeeds | Return unavailable comparison metadata and `PARTIAL_SUCCESS`. |
| Neither slot succeeds | Return unavailable comparison metadata and `FAILED`. |

## Timeout Handling

Executor timeout failures remain failures. The Composer:

```text
preserves planned Tool and ordering metadata
maps ToolTimeoutError to TOOL_TIMEOUT
does not retry
does not execute a fallback Tool
does not generate a replacement value
```

## Restart Recovery

The Composer is stateless.

Recovery validation means:

```text
supply an ExecutionResult after process restart
recompose a valid ComposedResponse
preserve execution_id and plan_id
derive the same response_id from the same supplied ExecutionResult
```

No Composer persistence table, cache, or database read is approved.

## Reason

The status model must preserve partial truth without converting failures,
sparse evidence, or conflicts into fabricated certainty.

## Alternatives Rejected

Rejected:

```text
catch-all SUCCESS responses
silent evidence omission
Composer retries
Composer Tool execution
database-backed repair
averaging conflicting authoritative values
new sparse-evidence business thresholds
Composer persistence in V1
```

## Risks

| Risk | Impact |
| --- | --- |
| Conservative failure handling can reduce apparent answer coverage | Truthful degradation is preferred to invented evidence. |
| Tool payload drift can cause normalization failures | Known Tool contracts must be validated strictly. |
| Sparse and partial conditions can coexist | Precedence plus structured disclosures must be tested in Phase 5.5C.4B. |

## Mitigations

```text
use explicit reason codes
retain safe frontend evidence
keep sparse markers even under PARTIAL_SUCCESS
make malformed envelopes fail closed
validate restart recomposition without adding persistence
```

## Governance Impact

Failure composition is deterministic and non-generative. The Composer may
report received failure facts and approved reason codes only. It may not
repair, reinterpret, or narrate failures.
