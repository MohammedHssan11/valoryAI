# ValorAI Grounding Security Review

Review date: 2026-06-02  
Phase: 5.5C.6H Grounding Architecture Review  
Status: Architecture only  

## Security Posture

Grounding assumes:

1. Providers are untrusted.
2. Provider output is untrusted.
3. Tenant-derived prompt content may be adversarial.
4. Citation tokens may be poisoned.
5. Memory summaries may contain stored injection content.
6. Every boundary can leak data.

## Threat Matrix

| Threat | Risk | Required Grounding posture |
| --- | --- | --- |
| Prompt injection | Candidate may follow tenant instructions instead of policy. | Validate original candidate only against manifest, contract, citations, and prohibited claims. Reject unsupported content. |
| Cross-tenant leakage | Candidate or citation may reflect foreign context. | Return `ACCESS_DENIED` for foreign or cross-scope binding. Permit no scoped fallback. |
| Citation poisoning | Token may be fabricated, altered, rebound, or used as a retrieval handle. | Exact immutable membership validation only. No lookup or repair. |
| Memory poisoning | Stored summaries may contain instructions or unsupported claims. | Treat candidate output as untrusted regardless of prompt source. Grounding does not trust Memory text as instructions. |
| Provider manipulation | Provider may return extra fields, follow-up requests, or authority claims. | Reject unknown fields and unsupported claims. |
| Contract bypass | Candidate may rely on a generic or wrong intent surface. | Require exactly one approved contract version and reject ambiguity. |
| Grounding bypass | Delivery path may skip Grounding. | Require Grounding acceptance before narrative persistence or Delivery. |
| Shadow context | Hidden retrieval or side input may influence narration. | Grounding trusts only one bound manifest and immutable package. Unknown content is unsupported. |
| Hidden retrieval | Provider or Grounding may retrieve external facts. | Provider retrieval and Grounding retrieval are forbidden. |
| Provider-side memory | Provider continuity may introduce unreviewed history. | Provider threads, sessions, and memory remain forbidden. |
| Grounding repair | Validator may sanitize content and conceal drift. | Reject original candidate without repair. |
| Grounding retry | Rejection may cause duplicate egress. | No retry, failover, or second provider call from Grounding. |
| Grounding self-healing | Fallback content may be regenerated and treated as grounded narration. | Grounding outputs no content. Deterministic fallback stays outside candidate narration. |
| Audit leakage | Decision records may become a transcript store. | Record bounded redacted reason metadata only. |

## Required Isolation

Grounding must have no:

1. Database access.
2. ORM access.
3. Cache access.
4. Memory retrieval.
5. Tool access.
6. Router, CMT, or ML access.
7. Provider invocation.
8. Prompt assembly access.
9. File access.
10. Browsing or external retrieval.
11. Embedding or vector-memory access.
12. Persistence ownership.
13. Delivery ownership.

## Forensic Security Findings

The observed unauthorized and legacy paths violate the target posture:

1. Candidate values are overwritten before validation.
2. Citation aliases and synthetic comparable wrappers are created.
3. Raw Memory context enters prompt assembly.
4. Latest-chat retrieval and persistence occur inside the adapter.
5. Legacy fallback content is created and revalidated after failure.
6. Modern intent-specific prohibited claims are incompletely enforced.

These findings require `NO_GO`.

