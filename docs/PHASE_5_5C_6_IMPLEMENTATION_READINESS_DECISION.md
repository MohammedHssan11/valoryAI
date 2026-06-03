# Phase 5.5C.6X Final Governance Remediation

Decision date: 2026-06-02  
Decision scope: Phase 5.5C.6 implementation readiness  
Reference authority: `PROJECT_MASTER_STATE_V2.md`  
Decision mode: Governance remediation only  

# Executive Decision

Phase 5.5C.6 is not ready for implementation.

The architecture boundaries are now resolved without creating new
architecture. The remaining blockers are smaller than the previously open
review set, but they are real:

1. Required Prompt Assembly and Provider Adapter operational values are not
   documented.
2. No concrete provider profile is documented or approved.
3. Conflicting activatable legacy and unauthorized LLM paths remain present
   in source and must be retired before the modern path is implemented.

This decision closes architecture discovery, architecture review, governance
review, and forensic review. No additional review cycle is authorized.

# Missing Information

The following information is not present in `PROJECT_MASTER_STATE_V2.md` and
is not resolved by any existing repository artifact:

1. Exact maximum serialized provider-request size.
2. Exact maximum provider-response size.
3. Exact maximum provider-output token count.
4. Exact maximum candidate-narration character count.
5. Exact maximum candidate citation-reference count.
6. Approved tokenizer identifier and version.
7. Approved serializer identifier and version.
8. Approved fixed-overhead and response-reserve accounting values.
9. Exact stable within-class optional-context eviction ordering and tie-break
   rules, if optional-context eviction is implemented.
10. One approved provider profile covering vendor, endpoint, model or model
    family, data-processing location, retention posture, logging posture,
    training-use posture, statelessness behavior, structured-output
    capability, timeout ceiling, request ceiling, response ceiling,
    observability metadata, credential handling, and contractual controls.

The repository contains partial legacy settings, including
`BROKER_MAX_CONTEXT_TOKENS = 4000` and `BROKER_LLM_TIMEOUT_SECONDS = 12.0`.
Those values are incomplete and belong to rejected legacy or unauthorized
runtime shapes. They are not silently promoted into modern governance
approvals.

# Blocker 1: Master State Synchronization

## Resolution

RESOLVED BY THIS DECISION

`PROJECT_MASTER_STATE_V2.md` remains the baseline authority. This required
Phase 5.5C.6X decision is the final phase-specific remediation addendum for
items documented after the last master-state update. It does not alter
completed pre-LLM phases.

## Final Authoritative Status

| Item | Final status | Resolution |
| --- | --- | --- |
| Phase 5.5C.6A unauthorized attempted LLM implementation | `REJECTED` | Must not be extended, activated, or reused as the modern path. |
| Phase 5.5C.6B canonical narration-only target | `ACCEPTED` | Keep the approved sequence after Memory Integration and before Delivery. |
| Phase 5.5C.6D Narration Contracts | `ACCEPTED` | Keep nine default-off intent-specific contracts and exact pass-through authority only. |
| Phase 5.5C.6F Narration Admission Gate | `ACCEPTED` | Keep the deterministic no-I/O fail-closed pre-provider firewall. |
| Phase 5.5C.6G Provider Adapter architecture | `ACCEPTED` | Keep the stateless minimized transport-only boundary. No concrete provider profile is approved. |
| Phase 5.5C.6E Prompt Assembly architecture | `ACCEPTED WITH REJECTED OPERATIONAL INPUTS` | Keep the representation-only boundary. Implementation remains blocked by missing exact values listed in this decision. |
| Candidate Parser architecture | `ACCEPTED` | Keep the parsing-only boundary defined below. |
| Phase 5.5C.6H target Grounding architecture | `ACCEPTED` | Keep the deterministic no-I/O decision-only target. Existing grounding-related runtime paths are rejected. |
| Existing legacy broker LLM runtime | `REJECTED` | Final disposition: `RETIRE`. |
| Existing unauthorized modern LLM package | `REJECTED` | Keep non-canonical, non-activatable, and unavailable for reuse. Retire from the implementation path. |
| Provider integration | `REJECTED` | No concrete approved provider profile exists. |
| Runtime activation | `REJECTED` | No Phase 5.5C.6 runtime activation is allowed before implementation conformance work completes. |
| Production promotion | `REJECTED` | Phase 5.5C.6 does not alter existing production-promotion blockers. |

No `CONDITIONAL` architecture status remains. An item is accepted, rejected,
or blocked by specifically missing operational information.

# Blocker 2: Candidate Parser

## Final Decision

KEEP

## Exact Ownership

The Candidate Parser owns parsing of one original unmodified provider
response into one minimal untrusted candidate representation.

## Exact Responsibilities

1. Receive the original unmodified provider response from the Provider
   Adapter.
2. Preserve linkage to the original response.
3. Enforce the approved response-size and candidate-size ceilings once those
   missing values are supplied.
4. Parse exactly one bounded candidate narration text field.
5. Parse one bounded citation-reference list when citations are referenced.
6. Reject malformed responses.
7. Reject unknown or additional fields.
8. Return the original parsed candidate to Grounding without semantic
   mutation.

## Exact Forbidden Responsibilities

The Candidate Parser must never:

1. Repair, rewrite, shorten, sanitize, summarize, enrich, or complete
   narration.
2. Overwrite, normalize, round, convert, or replace values.
3. Create, alias, normalize, resolve, repair, enrich, or attach citations.
4. Create evidence or synthetic comparable wrappers.
5. Ground or approve narration.
6. Retrieve Memory, database rows, Tool payloads, files, or external data.
7. Persist content.
8. Deliver content.
9. Retry a provider call or request failover.
10. Read provider-side memory, threads, sessions, or continuity metadata.

## Reason

Grounding can validate only an original candidate. Parser repair would create
hidden narration authority and destroy original-output integrity.

# Blocker 3: Prompt Assembly

## Final Governance Decision

PROMPT_ASSEMBLY_ARCHITECTURE: ACCEPTED  
PROMPT_ASSEMBLY_IMPLEMENTATION_READINESS: REJECTED  

Prompt Assembly remains a deterministic representation-only boundary after
`ADMIT_NARRATION`. It may serialize approved data, execute an approved
optional-context policy, count against approved hard limits, and reject. It
must not retrieve, infer, calculate, repair, persist, deliver, invoke a
provider, or ground output.

## Approval Matrix

| Unresolved item | Decision | Final governance position |
| --- | --- | --- |
| Representation-only deterministic boundary | `APPROVED` | Prompt Assembly packages approved representation only. |
| Exactly one admitted scoped envelope as input | `APPROVED` | Hidden side inputs are forbidden. |
| Internal envelope versus external projection separation | `APPROVED` | Internal attestations must not become provider-visible content. |
| Provider-visible allowlist | `APPROVED` | Only bounded current-turn content, minimized Composer projection, explicitly allowlisted redacted bounded Memory-summary classes, necessary exact citation tokens, and approved single-contract policy markers are eligible. |
| Provider-visible denylist | `APPROVED` | Raw plans, execution results, Tool payloads, database rows, ORM objects, raw Memory context, raw Composer context, frontend payloads, full transcripts, identifiers, credentials, secrets, logs, snapshots, provider memory, retrieval, files, embeddings, and unknown fields are forbidden. |
| Protected-context list | `APPROVED` | Admission attestation, single-intent contract marker, narration-policy marker, required bounded current-turn content, core Composer projection, exact deterministic values, required limitations, required citations, and serialization-policy identifiers are non-evictable. |
| Optional-context classes | `APPROVED` | Only explicitly allowlisted Memory-summary segments, supplemental Composer segments, and supplemental evidence with now-unused citations are eligible for eviction. Unclassified segments are never optional. |
| Stable class-level eviction order | `APPROVED` | Optional Memory summaries first, optional Composer supplemental segments second, optional evidence and now-unused citations third, otherwise reject. |
| Exact within-class eviction order and tie-break rules | `REJECTED` | Not documented. If optional eviction is implemented, exact ordering must be supplied before implementation. |
| Tokenizer identifier and version | `REJECTED` | Not documented. |
| Serializer identifier and version | `REJECTED` | Not documented. |
| Fixed-overhead and response-reserve accounting | `REJECTED` | Exact values are not documented. |
| Exact request, response, output-token, character, citation-count, and timeout limits | `REJECTED` | Exact values are not documented. |
| Citation-token presentation form | `APPROVED` | Only `[citation:<exact-received-id>]` is allowed. The wrapper is presentation syntax only. |
| Citation-token representability rule | `APPROVED` | Preserve exact identity or reject. Unsafe or ambiguous exact representation must fail closed. |
| Opaque citation-token posture | `APPROVED` | Citation tokens are references only, never retrieval handles. |
| Opaque internal binding attestations | `APPROVED` | Internal, request-bound, non-semantic, and never provider-visible. |
| Assembly logging posture | `APPROVED` | Bounded redacted non-content metadata only. Prompt content and response content logging are forbidden by default. |
| Single-contract enforcement | `APPROVED` | Exactly one active approved narration contract per candidate. |
| Deterministic-only excluded flows | `APPROVED` | General-question, clarification, unsupported, generic catch-all, disabled narration, and multi-intent flows do not invoke a provider. |
| Repair, retry, failover, second-pass assembly, or provider-feedback loop | `REJECTED` | None is allowed. |
| Legacy broker bypass | `REJECTED` | Legacy path must be retired. |

## Prompt Assembly Blocker

The Prompt Assembly boundary is final, but implementation is blocked until
the missing exact operational values and policy versions are supplied. They
cannot be invented by implementation.

# Blocker 4: Provider Adapter

## Final Governance Decision

PROVIDER_ADAPTER_ARCHITECTURE: ACCEPTED  
PROVIDER_INTEGRATION: REJECTED  

## Provider Authority

The provider is an untrusted external narrator. It has no truth, planning,
execution, calculation, Memory, citation, scope, persistence, Grounding,
Delivery, Tool, retrieval, browsing, file, or recommendation authority.

## Transport Authority

The Provider Adapter owns only:

1. One configuration-bound invocation of one explicitly approved provider
   profile.
2. Out-of-band provider authentication.
3. Hard timeout enforcement.
4. Request-size and response-size enforcement.
5. Preservation of the original unmodified provider response.
6. Uniform unavailable, timeout, and transport-error outcomes.
7. Bounded redacted transport metadata.

The adapter does not select providers dynamically and does not construct
prompts, parse candidates, ground output, persist text, or deliver text.

## Retention Rules

1. Provider-side threads, sessions, assistants, conversation continuity, and
   memory are forbidden.
2. Prompt or provider-response content retention is not approved by this
   architecture.
3. A provider profile without an explicit approved retention posture is
   unavailable.
4. Accepted narration persistence, when separately implemented, belongs only
   to Memory Integration after Grounding acceptance.

## Logging Rules

Allowed adapter logs are bounded redacted operational metadata only:

1. Opaque request correlation identifier.
2. Approved provider-profile identifier.
3. Approved model-profile identifier.
4. Policy versions.
5. Start and finish timestamps.
6. Duration.
7. Request-size and response-size metadata.
8. Outcome, timeout, attempt-count, and transport-error categories.

Prompt content, provider-response content, tenant identifiers, workspace
identifiers, scenario identifiers, broker-session identifiers, chat
identifiers, JWT claims, credentials, raw citations, raw Memory context, and
raw Composer context must not be logged by default.

## Statelessness Rules

Every provider call must be one stateless request-response operation. Provider
threads, provider memory, provider sessions, function calling, Tool calling,
browsing, retrieval, file upload, embeddings, arbitrary endpoints, and
pre-Grounding client streaming are forbidden.

## Retry Rules

Automatic retry is `REJECTED`.

The legacy setting `BROKER_LLM_MAX_RETRIES = 1` is not approved for the modern
path. A timeout, transport error, malformed response, parser rejection,
Grounding rejection, or policy rejection ends the narration attempt and uses
authorized deterministic fallback when authorization remains valid.

## Failover Rules

Transparent failover is `REJECTED`.

The adapter must not send the same tenant-scoped request to another provider.
Provider unavailability suppresses narration and uses authorized
deterministic fallback when authorization remains valid.

## Provider Adapter Blocker

No concrete provider profile is documented or approved. An unapproved
profile is unavailable. Provider integration cannot be implemented until the
missing profile information and exact hard limits are supplied.

# Blocker 5: Legacy LLM Path

## Findings

| Question | Decision | Evidence |
| --- | --- | --- |
| Does the legacy path exist? | `YES` | `backend/app/broker/llm/runtime/narration.py` and `backend/app/broker/orchestrator/core.py` remain present. |
| Is the legacy path activatable? | `YES` | `BROKER_LLM_ENABLED` can enable provider construction; the broker orchestrator receives the legacy narration singleton. |
| Does it conflict with the modern narration-only architecture? | `YES` | It builds legacy prompts, accepts the legacy broad response schema, overwrites authoritative values, permits pre-Grounding progress flow, and participates in fallback revalidation. |

## Final Decision

RETIRE

## Required Effect

The legacy broker LLM path must be removed from any activatable Phase 5.5C.6
runtime path before modern implementation begins. Deterministic pre-LLM broker
behavior may remain, but the legacy provider, prompt, parser, and Grounding
path must not define, bypass, or coexist as an alternative to the modern
canonical narration-only pipeline.

The unauthorized modern package under
`backend/app/copilot/orchestrator/llm/` is also rejected for reuse. Its
existing tests or scripts do not convert it into an approved runtime.

# Blocker 6: Grounding Forensic Findings

## Finding Resolution Matrix

| Finding | Confirmation | Decision | Evidence and reason |
| --- | --- | --- | --- |
| Value mutation before validation | `CONFIRMED` | `FIX_REQUIRED` | Both observed LLM paths overwrite parsed `authoritative_values` before Grounding can judge the original candidate. |
| Citation fabrication | `CONFIRMED` | `FIX_REQUIRED` | The unauthorized integration creates fallback evidence IDs including `valuation.authoritative` and `explainability.truth_layer`. |
| Citation aliasing | `CONFIRMED` | `FIX_REQUIRED` | Comparable IDs are transformed into `comp.<id>` aliases. |
| Synthetic comparable wrappers | `CONFIRMED` | `FIX_REQUIRED` | The unauthorized integration creates comparable wrappers with `price_egp = 0`. |
| Raw Memory coupling | `CONFIRMED` | `FIX_REQUIRED` | The unauthorized prompt path consumes raw `MemoryContext` slices and citation-package content. |
| Hidden retrieval | `CONFIRMED` | `FIX_REQUIRED` | The unauthorized integration queries the latest workspace chat directly. |
| Persistence outside Memory ownership | `CONFIRMED` | `FIX_REQUIRED` | The unauthorized integration creates assistant message persistence directly after legacy Grounding success. |
| Fallback revalidation | `CONFIRMED` | `FIX_REQUIRED` | Legacy broker finalization generates deterministic fallback content and revalidates it as Grounding output. |
| Incomplete prohibited-claims enforcement | `CONFIRMED` | `FIX_REQUIRED` | The legacy validator checks a narrow authoritative-values and evidence-ID surface, not the nine narration contracts and full prohibited-claims matrix. |
| Competing LLM paths | `CONFIRMED` | `FIX_REQUIRED` | The live legacy broker runtime and unauthorized modern package coexist. |

## Grounding Target Decision

The target Grounding boundary is accepted exactly as already documented:

1. Deterministic.
2. No-I/O.
3. Original-candidate-only.
4. Manifest-bound.
5. Immutable-citation-bound.
6. Single-contract-bound.
7. Prohibited-claims-enforcing.
8. Decision-only.
9. No repair.
10. No retry.
11. No failover.
12. No self-healing.
13. No inference.
14. No persistence.
15. No delivery.

The observed legacy validator and unauthorized integration are not acceptable
implementations of this target and must not be reused.

# Grounding Readiness Decision

GROUNDING_NOT_READY_FOR_IMPLEMENTATION

The Grounding target boundary is final and accepted, but implementation is
not ready to start while conflicting activatable paths remain in source.
Those paths mutate original candidates, synthesize citations, consume raw
Memory context, retrieve and persist outside approved owners, revalidate
fallback narration, and apply incomplete prohibited-claims enforcement.

Grounding becomes implementation-ready when the legacy and unauthorized LLM
paths are retired from the modern implementation path. No new architecture,
governance review, or forensic review is required.

# Implementation Readiness

## READY NOW

The following decisions are final and require no further architecture or
governance work:

1. Keep the canonical narration-only sequence after Memory Integration and
   before Delivery.
2. Keep the nine default-off exact-pass-through Narration Contracts.
3. Keep deterministic-only handling for general-question, clarification,
   unsupported, generic catch-all, disabled narration, and multi-intent flows.
4. Keep the deterministic no-I/O fail-closed Narration Admission Gate.
5. Keep the representation-only Prompt Assembly boundary.
6. Keep the stateless minimized transport-only Provider Adapter boundary.
7. Keep the parsing-only Candidate Parser boundary.
8. Keep the deterministic no-I/O original-candidate-only Grounding boundary.
9. Retire the legacy broker LLM path and reject reuse of the unauthorized
   modern package.

No Phase 5.5C.6 runtime implementation may begin until the blockers below are
fixed.

## MUST BE FIXED BEFORE IMPLEMENTATION

1. Supply the missing exact Prompt Assembly and Provider Adapter operational
   limits and versions:
   maximum serialized request size, maximum response size, maximum output
   tokens, maximum candidate characters, maximum citation references,
   tokenizer version, serializer version, fixed-overhead accounting,
   response-reserve accounting, and exact optional-context within-class
   ordering if optional eviction is implemented.
2. Supply one concrete approved provider profile with the documented vendor,
   endpoint, model, processing-location, retention, logging, training-use,
   statelessness, structured-output, timeout, request-ceiling,
   response-ceiling, observability, credential-handling, and contractual
   fields.
3. Retire the conflicting legacy broker LLM path and unauthorized modern LLM
   package from any activatable or reusable modern implementation path.

These are the smallest remaining blockers. The confirmed Grounding findings
are resolved by blocker 3: the observed paths are rejected and retired rather
than reused.

## OPTIONAL

None.

IMPLEMENTATION_READY_ITEMS

* Canonical narration-only sequence: accepted.
* Nine default-off Narration Contracts: accepted.
* Narration Admission Gate boundary: accepted.
* Prompt Assembly representation-only boundary: accepted.
* Provider Adapter transport-only boundary: accepted.
* Candidate Parser parsing-only boundary: accepted.
* Grounding decision-only target boundary: accepted.
* Legacy path disposition: `RETIRE`.

BLOCKING_ITEMS

* Supply exact Prompt Assembly and Provider Adapter operational limits and policy versions.
* Supply one concrete approved provider profile.
* Retire conflicting legacy and unauthorized LLM paths from any activatable or reusable modern implementation path.

OPTIONAL_ITEMS

* None.

GROUNDING_STATUS:
NOT_READY

FINAL_DECISION:
NO_GO

NEXT_STEP:
FIX_BLOCKERS_FIRST
