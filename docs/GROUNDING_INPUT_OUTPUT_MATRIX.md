# ValorAI Grounding Input and Output Matrix

Review date: 2026-06-02  
Phase: 5.5C.6H Grounding Architecture Review  
Status: Architecture only  

## Input Matrix

| Proposed input | Decision | Justification |
| --- | --- | --- |
| Original provider response | `CONDITIONAL` | Candidate Parser owns parsing. Grounding may receive a preserved-response linkage attestation and the original parsed candidate. |
| Original parsed candidate narration | `ALLOWED` | This is the only narration content Grounding may judge. It must remain unmodified. |
| Candidate citation-reference list | `ALLOWED` | Required when citations are referenced; exact scoped token validation only. |
| Prompt Assembly metadata | `CONDITIONAL` | Bounded redacted correlation metadata only: policy versions, segment identifiers, budget result, and opaque binding attestation. |
| Internal grounding manifest | `ALLOWED` | Required authoritative validation surface. It is produced upstream and bound to the admitted request. |
| Immutable citation package | `ALLOWED` | Required for exact scoped citation membership validation. |
| Narration-contract identifier and approved version | `ALLOWED` | Exactly one contract must apply. |
| Prohibited-claims policy identifier and approved version | `ALLOWED` | Required for deterministic policy enforcement. |
| Opaque binding attestations | `CONDITIONAL` | Allowed only when non-semantic, request-bound, and internal. |
| Provider transport metadata | `CONDITIONAL` | Bounded outcome and response-size metadata may support integrity correlation. It must not become evidence. |
| `MemoryContext` | `FORBIDDEN` | Raw Memory context exceeds Grounding's validation boundary. Allowed facts must arrive through the manifest only. |
| `ComposedResponse` | `FORBIDDEN` | Raw Composer output is broader than the Grounding validation surface. Allowed facts must arrive through the manifest only. |
| `ExecutionResult` | `FORBIDDEN` | Raw executor output stops upstream. |
| `ExecutionPlan` | `FORBIDDEN` | Planning state has no Grounding role. |
| Raw Tool payloads | `FORBIDDEN` | Grounding may not bypass Composer normalization. |
| Database rows | `FORBIDDEN` | Grounding is no-I/O and retrieval-free. |
| ORM entities | `FORBIDDEN` | ORM access creates persistence and scope leakage risk. |
| JWT claims | `FORBIDDEN` | Authentication and authorization remain upstream. |
| Tenant identifiers | `FORBIDDEN` | Raw identifiers must not enter Grounding. Opaque binding attestations are the maximum permitted substitute. |
| Workspace identifiers | `FORBIDDEN` | Raw identifiers remain upstream. |
| Scenario identifiers | `FORBIDDEN` | Raw identifiers remain upstream. |
| Broker-session identifiers | `FORBIDDEN` | Raw identifiers remain upstream. |
| Chat identifiers | `FORBIDDEN` | Grounding must not select or persist conversations. |
| Raw frontend payload | `FORBIDDEN` | Delivery data is not a Grounding input. |
| Raw prompt text | `FORBIDDEN` | Grounding validates candidate narration, not prompt quality. |
| Provider credentials | `FORBIDDEN` | Provider authentication remains out-of-band. |
| Hidden retrieval output | `FORBIDDEN` | No hidden retrieval is approved. |
| Provider-side memory or thread metadata | `FORBIDDEN` | Provider-side continuity is prohibited. |

## Output Matrix

| Grounding output | Decision | Meaning |
| --- | --- | --- |
| `ACCEPT_NARRATION` | `ALLOWED` | Original candidate is fully grounded and may proceed under downstream policy. |
| `REJECT_NARRATION` | `ALLOWED` | Candidate is suppressed; authorized deterministic fallback may remain available. |
| `ACCESS_DENIED` | `ALLOWED` | Cross-scope or untrusted binding detected; no scoped disclosure is permitted. |
| `UNGROUNDED` | `CONDITIONAL` | Allowed only as a bounded reason category under `REJECT_NARRATION`. |
| `POLICY_VIOLATION` | `CONDITIONAL` | Allowed only as a bounded reason category under `REJECT_NARRATION`. |
| Checked policy versions | `ALLOWED` | Bounded redacted decision metadata. |
| Checked citation tokens | `CONDITIONAL` | Bounded internal decision metadata only; do not create a broad content log. |
| Repaired narration | `FORBIDDEN` | Grounding never edits candidate text. |
| Sanitized narration | `FORBIDDEN` | Partial repair creates hidden narration ownership. |
| Replacement value | `FORBIDDEN` | Composer and Tools own values. |
| New citation | `FORBIDDEN` | Citation creation remains upstream. |
| Persistence operation | `FORBIDDEN` | Memory owns accepted-memory commits. |
| Delivery instruction | `FORBIDDEN` | Delivery owns transport behavior. |
| Retry or failover instruction | `FORBIDDEN` | Grounding rejection ends narration attempt. |

## Output Principle

Grounding outputs a decision, not content.

