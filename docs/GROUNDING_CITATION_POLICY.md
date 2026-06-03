# ValorAI Grounding Citation Policy

Review date: 2026-06-02  
Phase: 5.5C.6H Grounding Architecture Review  
Status: Architecture only  

## Citation Ownership

| Citation responsibility | Owner |
| --- | --- |
| Preserve received citation package | Response Composer and Memory Integration |
| Bind package to request before provider egress | Narration Admission Gate |
| Serialize approved provider-visible token without mutation | Prompt Assembly |
| Reference token in candidate narration | Provider, untrusted |
| Validate returned references | Grounding |
| Attach deterministic delivery citations | Delivery using immutable upstream package |

Grounding is a citation validator only. It is not a citation creator,
resolver, retrieval layer, or repair layer.

## Allowed Citation Categories

| Citation category | Decision | Notes |
| --- | --- | --- |
| `valuation_id` | `ALLOWED` | Canonical valuation citation when present in the immutable scoped package. |
| `tool_event_id` | `CONDITIONAL` | Optional pass-through citation when present in the immutable scoped package. |
| `comparable_id` | `CONDITIONAL` | Optional pass-through citation when present in the immutable scoped package. |
| `audit_id` | `FORBIDDEN` | Deferred and not approved. |
| `evidence_id` | `FORBIDDEN` | Deferred and not approved. |
| Citation alias | `FORBIDDEN` | Aliases create a second evidence system. |
| Fallback citation | `FORBIDDEN` | Missing citations must remain missing. |

## Validation Rules

Grounding must validate:

1. Every referenced token matches an immutable scoped token exactly.
2. Inline references and any candidate citation-reference list agree.
3. Every evidence-dependent statement carries required legal references under
   its contract.
4. No token is added, removed, renamed, normalized, repaired, enriched, or
   rebound.
5. Property-comparison references remain bound to the correct property.
6. Optional absence remains an honest limitation, not a repair opportunity.
7. Citation tokens are treated as references only, never retrieval handles.

## Rejection Matrix

| Citation condition | Required outcome |
| --- | --- |
| Fabricated citation | `REJECT_NARRATION` |
| Citation alias | `REJECT_NARRATION` |
| Fallback evidence ID | `REJECT_NARRATION` |
| Modified token | `REJECT_NARRATION` |
| Missing required citation | `REJECT_NARRATION` |
| Extra unsupported citation | `REJECT_NARRATION` |
| Unsupported citation category | `REJECT_NARRATION` |
| Citation bound to wrong compared property | `REJECT_NARRATION` |
| Foreign-tenant citation | `ACCESS_DENIED` |
| Cross-workspace citation | `ACCESS_DENIED` |
| Untrusted citation-package binding | `ACCESS_DENIED` |
| Unsafe exact token representation | `REJECT_NARRATION` |

## Prohibited Grounding Behavior

Grounding must never:

1. Query a database for a citation.
2. Resolve a token into evidence.
3. Hash a value into a replacement citation.
4. Infer a missing citation.
5. Create `comp.<id>` aliases.
6. Create `valuation.authoritative`.
7. Create `explainability.truth_layer`.
8. Create placeholder comparable records.
9. Accept zero-price synthetic comparable wrappers.
10. Treat citation absence as permission to proceed with an evidence claim.

## Forensic Finding

The observed unauthorized adapter synthesizes citation aliases and
replacement comparable wrappers. That behavior is `NO_GO`.

