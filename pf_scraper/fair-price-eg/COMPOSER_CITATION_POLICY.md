# Response Composer Citation Policy

Phase: 5.5C.4A Response Composer Architecture Resolution  
Status: Architecture specification only

## Decision

The Composer preserves citation identifiers received through
`ExecutionResult` payloads. It does not create a new citation system.

Approved V1 citation types:

| Citation type | Status | Meaning |
| --- | --- | --- |
| `valuation_id` | Canonical | Canonical valuation citation. |
| `tool_event_id` | Optional | Preserve only when received. |
| `comparable_id` | Optional | Preserve only when received. |
| `audit_id` | Deferred | Not emitted in V1. |
| `evidence_id` | Deferred | Not emitted in V1. |

## Citation Package

```json
{
  "valuation_ids": ["val_<uuid>"],
  "tool_event_ids": [],
  "comparable_ids": ["listing_<id>"],
  "unavailable_optional_citation_types": ["tool_event_id"]
}
```

The arrays contain stable first-seen unique identifiers. De-duplication is
allowed only to avoid repeating an identical received identifier. It must not
rewrite identifiers.

## Approved Structured Extraction Paths

### Valuation Citations

The Composer may preserve structured values from:

```text
valuation_id
valuation_ids[]
base_valuation_id
scenario_valuation_id
fairness_valuation_id
```

All of these contribute canonical valuation citations.

### Tool-Event Citations

The Composer may preserve structured values from:

```text
tool_event_id
tool_event_ids[]
```

These are optional because current Tool payloads may not expose them.

### Comparable Citations

The Composer may preserve structured values from:

```text
comparable_id
comparable_ids[]
comparable_ids_used[]
```

For the existing Explainability Tool schema only, the Composer may normalize:

```text
comparable_evidence[].property_id
```

as a comparable identifier because that field is the structured identifier
for a received comparable evidence row. This narrow mapping must not be
applied to arbitrary `property_id` fields elsewhere.

## Prohibited Citation Behavior

The Composer must not:

```text
query Tool events
query valuation snapshots
query any database table
parse opaque narrative text to recover identifiers
invent snapshot IDs
invent Tool-event IDs
create audit IDs
create evidence IDs
hash payloads into replacement citations
reinterpret arbitrary database identifiers as citations
```

## Optional Citation Disclosure

Missing optional citation types are not failures.

The Composer records unavailable optional types:

```json
{
  "unavailable_optional_citation_types": [
    "tool_event_id",
    "comparable_id"
  ]
}
```

`comparable_id` is unavailable only when no received payload contains a
structured comparable identifier.

## Frontend Delivery

The same `citation_package` is included as structured data in:

```text
ComposedResponse.citation_package
ComposedResponse.frontend_payload.citations
```

No SSE citation event, WebSocket message, or streaming wrapper is created in
Phase 5.5C.4.

## Reason

Citation integrity requires a pass-through boundary. A Composer that queries
or fabricates citation IDs would violate tenant isolation and blur the
separation between execution and composition.

## Alternatives Rejected

Rejected:

```text
database lookup of persisted Tool events
treating valuation_id and an invented snapshot_id as separate citations
introducing audit_id
introducing evidence_id
parsing IDs out of narrative text
emitting citation SSE events
```

## Risks

| Risk | Impact |
| --- | --- |
| Tool-event citations are often absent | Frontend consumers must handle optional coverage. |
| Comparable identifiers use different source field names | Extraction must be path-specific and strictly governed. |
| Over-broad identifier extraction could leak internal IDs | Only approved structured paths may contribute citations. |

## Mitigations

```text
use an explicit extraction allowlist
de-duplicate without rewriting IDs
record unavailable optional citation types
keep deferred citation categories absent
never query infrastructure
```

## Governance Impact

`valuation_id` is the canonical valuation citation for Phase 5.5C.4. Citation
coverage is honest and bounded by received evidence. Optional absence is
disclosed instead of repaired.

