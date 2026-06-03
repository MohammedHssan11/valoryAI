# ValorAI Phase 5.5C.6E Prompt Assembly Architecture Review

Review date: 2026-06-02  
Review scope: Prompt Assembly Architecture  
Review mode: Architecture only  
Implementation status: Prohibited  

## Authoritative Sources

This review is based only on the following authoritative sources, each read
completely:

1. `PROJECT_MASTER_STATE_V2.md`
2. `NARRATION_CONTRACT_ARCHITECTURE.md`
3. `NARRATION_ACTIVATION_POLICY.md`
4. `NARRATION_PROHIBITED_CLAIMS_MATRIX.md`
5. `VALUATION_NARRATION_CONTRACT.md`
6. `EXPLAINABILITY_NARRATION_CONTRACT.md`
7. `COMPARABLES_NARRATION_CONTRACT.md`
8. `FAIRNESS_NARRATION_CONTRACT.md`
9. `WHAT_IF_NARRATION_CONTRACT.md`
10. `NEGOTIATION_NARRATION_CONTRACT.md`
11. `INVESTMENT_NARRATION_CONTRACT.md`
12. `MARKET_INSIGHT_NARRATION_CONTRACT.md`
13. `PROPERTY_COMPARISON_NARRATION_CONTRACT.md`
14. `NARRATION_APPROVAL_DECISION.md`
15. `PHASE_5_5C_6B_FORMAL_ARCHITECTURE_REVIEW.md`
16. `PHASE_5_5C_6B_RUNTIME_DECISION.md`
17. `PHASE_5_5C_6B_BOUNDARY_OWNERSHIP_MATRIX.md`
18. `PHASE_5_5C_6B_CANONICAL_RUNTIME_PATH.md`
19. `PHASE_5_5C_6B_APPROVAL_REQUIREMENTS.md`
20. `PHASE_5_5C_6FG_ARCHITECTURE_REVIEW.md`

The sources provide sufficient information for an architecture review. No
implementation assumption is required.

## Locked Rule

```text
Planner decides.
Executor executes.
Composer computes.
Memory remembers.
LLM narrates.
```

Prompt Assembly exists only to preserve this rule. It is not a reasoning,
retrieval, memory, evidence, authorization, provider-selection, grounding, or
delivery layer.

# Section 1: Architecture Overview

## 1.1 Purpose

Prompt Assembly is the deterministic bounded transformation between an
`ADMIT_NARRATION` decision and the Provider Adapter.

Its purpose is narrow:

1. Consume exactly one validated scoped narration envelope emitted after the
   Narration Admission Gate approves narration.
2. Use only the envelope's already-approved provider-safe projection as
   external request content.
3. Apply one approved deterministic serialization policy.
4. Apply one approved deterministic optional-context eviction policy when
   needed.
5. Perform the final exact hard-budget decision.
6. Emit one bounded provider request artifact or reject narration before any
   provider invocation.

Prompt Assembly is packaging, not authorship.

## 1.2 Ownership

Prompt Assembly owns:

1. Deterministic serialization of already-approved provider-safe projection
   segments.
2. Deterministic ordering of approved projection segments.
3. Final exact request-budget accounting under an approved tokenizer,
   serializer, provider profile, and policy version.
4. Execution of a pre-approved optional-context eviction order.
5. Rejection when protected context cannot fit.
6. Emission of bounded redacted assembly metadata for downstream audit and
   grounding correlation.

Prompt Assembly does not own:

1. Narration eligibility.
2. Provider-safe projection construction.
3. Scope validation.
4. Semantic content selection outside the pre-approved eviction policy.
5. Provider selection or invocation.
6. Candidate parsing.
7. Grounding acceptance.

## 1.3 Inputs

Prompt Assembly receives exactly one validated scoped narration envelope from
the Narration Admission Gate.

The only external-request content it may use is the envelope's provider-safe
projection. Internal binding attestations may accompany the envelope for
integrity correlation, but they must never become provider-visible content.

## 1.4 Outputs

Prompt Assembly emits exactly one of:

1. One bounded provider request artifact plus bounded redacted assembly
   metadata.
2. A fail-closed narration rejection outcome.

The provider request artifact is not an authoritative response. It grants no
new authority to the provider.

## 1.5 Responsibilities

Prompt Assembly must:

1. Require upstream `ADMIT_NARRATION`.
2. Reject every other admission state.
3. Consume no hidden side input.
4. Preserve the distinction between internal envelope metadata and external
   provider-visible projection content.
5. Preserve exact deterministic values without rounding, conversion,
   recombination, enrichment, or inference.
6. Preserve immutable citation tokens without aliasing, normalization,
   repair, or replacement.
7. Keep tenant-derived content structurally treated as untrusted data.
8. Apply final exact request-size and token-budget enforcement.
9. Fail closed before provider invocation.

## 1.6 Non-Responsibilities

Prompt Assembly must never:

1. Parse JWTs or execute authentication or authorization policy.
2. Resolve tenant, workspace, scenario, broker-session, chat, property, or
   citation scope.
3. Retrieve memory.
4. Read databases, ORM entities, caches, logs, transcripts, or Tool payloads.
5. Classify intent.
6. Select or execute Tools.
7. Compute values.
8. Summarize, compress, redact, repair, or infer facts dynamically.
9. Select providers.
10. Invoke providers.
11. Parse or repair provider responses.
12. Approve grounding.
13. Persist content.
14. Deliver content.

## 1.7 Runtime Placement

The approved placement is:

```text
Authenticated scoped request
  -> Intent Engine
  -> Tool Planner
  -> Tool Executor
  -> Response Composer
  -> Memory Integration Pre-Generation
  -> Narration Admission Gate
  -> Prompt Assembly
  -> Provider Adapter
  -> Candidate Parser
  -> Deterministic Grounding and Governance
  -> Memory Integration Post-Generation, when separately approved
  -> Delivery
```

Prompt Assembly must not be bypassable by routes, feature flags, retries,
failover, legacy broker configuration, direct provider calls, or provider
capabilities.

## 1.8 Failure Behavior

Prompt Assembly is fail-closed:

1. Any missing required artifact rejects narration.
2. Any admission state other than `ADMIT_NARRATION` blocks assembly.
3. Any unknown projection segment rejects narration.
4. Any protected-content overflow rejects narration.
5. Any serialization ambiguity rejects narration.
6. Any unsafe citation representation rejects narration.
7. Any policy-version mismatch rejects narration.
8. No rejected assembly may contact a provider.

When authorization remains valid, the authorized Composer-owned deterministic
fallback remains available. Prompt Assembly must never weaken
`ACCESS_DENIED`.

## 1.9 Deterministic Behavior

Given the same admitted envelope, approved policy versions, tokenizer,
serializer, provider profile, and hard limits, Prompt Assembly must produce
the same result:

1. The same included projection segments.
2. The same evicted optional segments.
3. The same provider request artifact.
4. The same budget accounting.
5. The same bounded redacted assembly metadata.
6. The same rejection outcome when assembly cannot proceed.

No model, random choice, provider feedback, dynamic retrieval, or runtime
heuristic may influence assembly.

## 1.10 Relationships

| Layer | Relationship to Prompt Assembly |
| --- | --- |
| Narration Admission Gate | Exclusive upstream owner of narration admission, scope binding, minimization, provider-safe projection construction, preflight budget eligibility, and grounding eligibility. |
| Provider Adapter | Exclusive downstream owner of approved-profile transport invocation. It may receive only the bounded provider request artifact. |
| Grounding | Separate downstream authority that validates original candidate narration. Prompt Assembly cannot ground or pre-approve provider output. |
| Memory Integration | Exclusive memory retrieval and persistence owner. Prompt Assembly may use only gate-approved redacted bounded Memory-summary projection segments. |
| Response Composer | Exclusive arithmetic and deterministic response-composition owner. Prompt Assembly may package only minimized approved Composer projection segments. |
| Narration Contracts | Normative limits on what provider-visible context may support and what future candidate narration may restate exactly. Prompt Assembly cannot merge, widen, or substitute contracts. |

# Section 2: Boundary Ownership Review

## 2.1 What Prompt Assembly Owns

Prompt Assembly owns only:

1. Verification that an upstream `ADMIT_NARRATION` decision is present and
   bound to the envelope.
2. Verification that the referenced approved assembly-policy versions are
   present and internally consistent.
3. Deterministic serialization of allowlisted provider-safe projection
   segments.
4. Deterministic omission of explicitly optional segments under a
   pre-approved eviction order.
5. Final exact hard-budget enforcement.
6. Bounded redacted assembly metadata.

## 2.2 What Prompt Assembly Does Not Own

Prompt Assembly does not own:

1. Admission-state classification.
2. Authentication, authorization, or tenancy decisions.
3. Provider egress allowlist definition.
4. Redaction decisions.
5. Composer compression.
6. Memory summarization.
7. Citation creation, resolution, lookup, or validation ownership.
8. Grounding-eligibility definition.
9. Provider profile approval.
10. Provider selection.
11. Provider retry or failover.
12. Candidate schema decisions.
13. Delivery or persistence.

## 2.3 What Prompt Assembly May Read

Prompt Assembly may read only:

1. One admitted scoped narration envelope.
2. The envelope's provider-safe projection.
3. An opaque internal envelope-binding attestation.
4. Approved assembly-policy identifiers and versions.
5. Approved serializer and tokenizer identifiers and versions.
6. Approved provider-profile hard-limit metadata required for exact budget
   accounting.
7. Explicit per-segment protected or optional classification already decided
   by governance policy.

## 2.4 What Prompt Assembly May Never Read

Prompt Assembly may never read:

1. Raw JWTs, claims, tokens, credentials, or secrets.
2. `ExecutionPlan`.
3. Raw `ExecutionResult`.
4. Raw Tool 1-8 payloads.
5. Raw `ComposedResponse`.
6. Raw `MemoryContext`.
7. Raw `frontend_payload`.
8. Database rows, ORM entities, direct query results, caches, or
   unrestricted logs.
9. Full transcripts or unrestricted messages.
10. Foreign, deleted, failed, access-denied, unbound, or cross-scope data.
11. Provider responses.
12. Grounding decisions from previous attempts.
13. Provider-side memory, retrieval results, or external knowledge.

## 2.5 What Prompt Assembly May Transform

Prompt Assembly may transform only representation:

1. Place already-approved projection segments into the approved deterministic
   serialized form.
2. Order segments according to approved deterministic policy.
3. Omit only segments already classified as optional and evictable.
4. Attach bounded non-content assembly metadata outside provider-visible
   content.

## 2.6 What Prompt Assembly May Never Transform

Prompt Assembly may never:

1. Change a deterministic fact.
2. Change, round, convert, recombine, aggregate, or calculate a numeric value.
3. Rewrite a limitation into stronger certainty.
4. Add an assumption.
5. Repair missing evidence.
6. Create or rename a citation.
7. Re-summarize Composer context.
8. Re-summarize Memory content.
9. Merge tenant scopes.
10. Merge contracts.
11. Infer a missing field.
12. Add provider-specific hidden context.

# Section 3: Input Review

| Proposed input | Decision | Justification |
| --- | --- | --- |
| `MemoryContext` | `CONDITIONAL` | Raw `MemoryContext` is forbidden. Only Admission-Gate-approved redacted bounded Memory-summary projection segments may enter Prompt Assembly inside the admitted envelope. |
| `ComposedResponse` | `CONDITIONAL` | Raw `ComposedResponse` is forbidden. Only minimized approved Composer projection segments, deterministic status markers, limitation disclosures, and immutable citation tokens may enter inside the admitted envelope. |
| `ExecutionResult` | `FORBIDDEN` | Raw execution output stops at Response Composer. |
| `ExecutionPlan` | `FORBIDDEN` | Planning authority remains upstream and has no narration-packaging purpose. |
| Raw Tool payloads | `FORBIDDEN` | Tool output must cross the Composer normalization and compression boundary first. |
| Database rows | `FORBIDDEN` | Prompt Assembly is not a retrieval or persistence boundary. |
| ORM entities | `FORBIDDEN` | ORM entities expose uncontrolled persistence structure and fields. |
| JWT claims | `FORBIDDEN` | Authentication and authorization remain upstream; claims create leakage risk and no narration value. |
| Tenant identifiers | `FORBIDDEN` | Raw tenant identifiers must never enter provider-visible content or Prompt Assembly inputs. An opaque non-semantic binding attestation may accompany the envelope only for integrity correlation. |
| Workspace identifiers | `FORBIDDEN` | Raw workspace identifiers remain internal to upstream binding. An opaque non-semantic binding attestation is the maximum conditional exception. |
| Scenario identifiers | `FORBIDDEN` | Raw scenario identifiers remain internal to upstream binding. Approved scenario facts may be projected without exposing the identifier. |
| Broker-session identifiers | `FORBIDDEN` | Raw broker-session identifiers remain internal. Provider-side continuity is prohibited. |

Additional input decisions:

| Proposed input | Decision | Justification |
| --- | --- | --- |
| Bounded current-turn content | `CONDITIONAL` | Allowed only inside the admitted provider-safe projection, marked as untrusted user data, size-limited, and structurally isolated from governed policy material. |
| Approved intent marker | `ALLOWED` | Required to preserve the one-contract boundary. |
| Approved contract and policy markers | `ALLOWED` | Required only in bounded governed form. They do not grant new authority. |
| Exact immutable citation tokens | `CONDITIONAL` | Allowed only when scoped, safely representable, provider-necessary, and passed through unchanged. |
| Internal grounding manifest | `FORBIDDEN` | Grounding receives its internal manifest through a separate internal path. Prompt Assembly may receive only an opaque binding attestation when required for correlation. |
| Provider credentials | `FORBIDDEN` | Provider authentication is out-of-band and owned by the Provider Adapter. |

# Section 4: Context Eligibility Matrix

| Context category | Decision | Protected or evictable | Reason |
| --- | --- | --- | --- |
| Upstream `ADMIT_NARRATION` attestation | `ALLOWED` | Protected, internal only | Assembly must prove admission occurred. |
| Approved single-intent marker | `ALLOWED` | Protected | Prompt Assembly may package one approved intent contract only. |
| Approved contract-version marker | `ALLOWED` | Protected | Contract substitution or ambiguity must fail closed. |
| Approved narration-policy marker | `ALLOWED` | Protected | Required bounded governance context. |
| Bounded current-turn content | `CONDITIONAL` | Protected when admitted | It is untrusted user data, never authority. If it cannot fit its hard limit, reject narration. |
| Minimized Composer compressed-context projection | `ALLOWED` | Protected core; optional supplemental segments only when pre-classified | Composer is the only arithmetic and deterministic composition owner. |
| Composer deterministic status | `ALLOWED` | Protected | Status and limitations must not be weakened. |
| Composer arithmetic fields | `CONDITIONAL` | Protected when exposed | Exact pass-through only. No reformatting that changes value meaning. |
| Composer `frontend_payload` | `FORBIDDEN` | Not applicable | Frontend-safe does not imply provider-safe or provider-necessary. |
| Approved redacted bounded Memory-summary classes | `CONDITIONAL` | Optional by default unless policy explicitly protects a class | Memory Integration owns retrieval and summarization. Assembly cannot widen memory use. |
| Raw `MemoryContext` | `FORBIDDEN` | Not applicable | Only minimized redacted summary projection segments may enter. |
| Evidence-limitation disclosures | `ALLOWED` | Protected | Sparse, insufficient, partial, and unavailable disclosures must survive packaging. |
| Exact immutable citation tokens | `CONDITIONAL` | Protected when required by included evidence segment | Citation identity must remain unchanged and scoped. |
| Raw citation package metadata | `FORBIDDEN` | Not applicable | Internal provenance and scope metadata are not provider content. |
| Opaque internal envelope-binding attestation | `CONDITIONAL` | Protected, internal only | It may support correlation but must never become provider-visible content. |
| Raw tenant, user, workspace, scenario, broker-session, chat, or property identifiers | `FORBIDDEN` | Not applicable | Identity and scope remain internal. |
| Full transcript or unrestricted message history | `FORBIDDEN` | Not applicable | Only bounded approved Memory summaries may support continuity. |
| Raw logs, snapshots, prediction logs, shadow logs, or Tool events | `FORBIDDEN` | Not applicable | Composer and Memory must create the governed summaries. |
| External retrieval, provider memory, hidden model knowledge, browsing, files, embeddings, or Tool capability markers | `FORBIDDEN` | Not applicable | Providers are untrusted stateless narrators only. |
| Unknown or unclassified projection segment | `FORBIDDEN` | Not applicable | Denied by default. |

# Section 5: Memory Policy

## 5.1 Memory Content That May Enter Prompt Assembly

Only the following Memory-derived content may enter:

1. Approved redacted bounded Memory-summary projection segments selected by
   Memory Integration and minimized by the Admission Gate.
2. Approved evidence-limitation disclosures.
3. Exact immutable scoped citation tokens when required for narration.
4. Opaque internal binding attestation needed for integrity correlation.

Each Memory-summary class must be explicitly allowlisted, versioned,
intent-compatible, bounded, redacted, tenant-scoped, and provider-safe before
Prompt Assembly receives it.

## 5.2 Memory Content That May Never Enter Prompt Assembly

Prompt Assembly must never receive:

1. Raw `MemoryContext`.
2. Raw conversation messages.
3. Full transcript history.
4. Unrestricted decision history.
5. Raw Tool events.
6. Raw valuation snapshots.
7. Raw assumptions, scenario lineage, prediction logs, or shadow logs.
8. Database rows or ORM entities.
9. Foreign, deleted, failed, `ACCESS_DENIED`, or unbound Memory content.
10. Hidden retrieval output.
11. Provider-side memory identifiers.

## 5.3 Redaction

Before Prompt Assembly, Memory-derived projection segments must remove:

1. Tenant, user, workspace, scenario, broker-session, chat, and property
   identifiers unless a future separate approval proves a field necessary.
2. Tokens, secrets, credentials, connection strings, and infrastructure
   details.
3. Unnecessary personal or tenant-sensitive content.
4. Any field outside the approved summary-class allowlist.
5. Any content that cannot be deterministically represented as inert
   tenant-derived data.

Prompt Assembly does not perform redaction. A redaction failure discovered at
assembly time rejects narration.

## 5.4 Provider Safety

Memory-derived content remains provider-safe only when:

1. It is bounded and explicitly allowlisted.
2. It is already redacted before assembly.
3. It is relevant to the admitted single intent.
4. It does not introduce instructions, authority, hidden retrieval, or
   provider continuity.
5. It remains subject to post-generation grounding.

## 5.5 Tenant Isolation

Tenant isolation is preserved by:

1. Memory Integration tenant-scoped retrieval.
2. Admission Gate cross-artifact binding.
3. One admitted envelope per request.
4. No Prompt Assembly retrieval.
5. No raw scope identifiers in provider-visible content.
6. No cross-envelope merge.
7. Fail-closed rejection for ambiguity.

# Section 6: Composer Policy

## 6.1 Composer Output That May Enter Prompt Assembly

Only Admission-Gate-approved minimized Composer projection segments may enter:

1. Bounded `compressed_context` projection fields.
2. Approved deterministic status markers.
3. Approved supported-intent markers.
4. Approved exact pass-through numeric values.
5. Sparse, insufficient, partial, and failure disclosures.
6. Exact immutable scoped citation tokens required for narration.

## 6.2 Composer Output That Must Remain Unchanged

Prompt Assembly must preserve:

1. Deterministic values exactly.
2. Numeric precision exactly.
3. Status meaning exactly.
4. Limitation strength exactly.
5. Citation identity exactly.
6. Property-specific citation binding exactly.
7. Scenario facts and assumptions exactly when admitted.
8. Composer ownership of every arithmetic result.

Serialization must not change meaning. If an exact upstream value cannot be
represented safely and unambiguously, Prompt Assembly rejects narration.

## 6.3 Composer Output That Must Never Be Exposed

Prompt Assembly must never expose:

1. Raw `ComposedResponse`.
2. Raw `frontend_payload`.
3. Hidden Composer metadata.
4. Raw execution payloads retained upstream.
5. Unapproved internal identifiers.
6. Any unclassified field.
7. Any field omitted from the approved provider-safe projection.

# Section 7: Citation Policy

## 7.1 Allowed Citation Inputs

Prompt Assembly may receive only exact immutable scoped citation tokens
already selected for provider visibility by the Admission Gate.

The legal presentation form remains:

```text
[citation:<exact-received-id>]
```

The wrapper is presentation syntax only. The underlying identifier remains
unchanged.

## 7.2 Forbidden Citation Inputs

Prompt Assembly must reject:

1. Citation aliases.
2. Fallback evidence IDs.
3. Placeholder comparables.
4. Replacement records.
5. Foreign or cross-workspace citations.
6. Unscoped citations.
7. Unknown citations.
8. Citation lookup instructions.
9. Citation tokens that cannot be represented safely and unambiguously.

## 7.3 Citation Immutability

Prompt Assembly may:

1. Pass through an exact token.
2. Place the exact token inside the already-approved presentation wrapper.
3. Omit an optional evidence segment only when its associated citation
   handling remains consistent under the approved eviction policy.

Prompt Assembly may not:

1. Normalize a token.
2. Escape a token in a way that changes identity.
3. Invent a token.
4. Resolve a token.
5. Repair a token.
6. Rebind a token.

If safe representation and exact identity cannot both be preserved, reject
narration.

## 7.4 Citation Ownership

| Citation action | Owner |
| --- | --- |
| Create and preserve approved citation package | Response Composer and Memory Integration |
| Validate package binding before assembly | Narration Admission Gate |
| Serialize exact provider-visible token without mutation | Prompt Assembly |
| Reference exact token as candidate narration | Provider, untrusted |
| Validate every returned token | Grounding Layer |
| Attach deterministic citations for delivery | Delivery using upstream immutable package |

## 7.5 Citation Leakage Risks

Citation tokens are the only opaque evidence identifiers eligible for
provider visibility. They still create leakage risk when:

1. Tokens encode internal identifiers.
2. Tokens expose tenant structure.
3. Tokens can be used as retrieval paths.
4. Tokens contain unsafe serialization characters.
5. Tokens are over-shared when not needed for narration.

Governance must approve an opaque-token posture and safe representability
rule before implementation.

## 7.6 Citation Injection Risks

A citation token is untrusted as serialized content until proven safe.
Admission and assembly policy must ensure:

1. Exact identity is preserved.
2. Unsafe tokens are rejected, not repaired.
3. Citation tokens cannot alter serialization boundaries.
4. Citation tokens cannot introduce policy instructions.
5. Citation tokens cannot trigger provider retrieval or Tool behavior.

## 7.7 Citation Fabrication Risks

Prompt Assembly cannot prevent provider fabrication through packaging alone.
The required controls are:

1. Expose only exact allowlisted tokens.
2. Keep the immutable package internal.
3. Validate original candidate references downstream.
4. Reject missing, foreign, fabricated, unsupported, or mismatched tokens.
5. Never repair a fabricated token.

# Section 8: Token Budget Policy

## 8.1 Budget Ownership

Budget ownership is split deliberately:

| Budget responsibility | Owner |
| --- | --- |
| Approve hard request, response, output, character, citation-count, and provider-profile limits | Governance |
| Approve tokenizer, serializer, fixed-overhead, reserve, and eviction-policy versions | Governance |
| Preflight projection-class hard limits and non-evictable fit | Narration Admission Gate |
| Perform final exact serialized request-budget accounting | Prompt Assembly |
| Enforce transport request-size and response-size ceilings | Provider Adapter |
| Reject overlong candidate output | Candidate Parser and Grounding Layer under approved limits |

## 8.2 Budget Enforcement

Prompt Assembly must reserve, account for, and enforce:

1. Approved fixed-policy overhead.
2. Protected provider-visible context.
3. Optional provider-visible context after deterministic eviction.
4. Approved response allowance.
5. Approved provider-profile hard ceiling.
6. Approved character ceiling.
7. Approved citation-reference ceiling.

Exact hard values are not approved by this review. Their absence blocks
implementation.

## 8.3 Budget Failure Behavior

Budget failure is fail-closed:

1. Protected content never truncates silently.
2. Numeric values never round to save space.
3. Citation tokens never shorten or alias.
4. Limitations never disappear.
5. Current-turn content never truncates silently.
6. If deterministic optional eviction cannot make the request fit, reject
   narration before provider invocation.
7. Authorized Composer-owned deterministic fallback remains available when
   confidentiality and authorization remain intact.

## 8.4 Budget Governance

Every budget-affecting decision must be versioned and approved:

1. Tokenizer.
2. Serializer.
3. Fixed overhead.
4. Provider request ceiling.
5. Provider response ceiling.
6. Output allowance.
7. Character ceiling.
8. Citation-count ceiling.
9. Segment-level protected or optional classification.
10. Eviction order.
11. Tie-break rules.

## 8.5 Maximum Allowed Responsibilities

Prompt Assembly may count, serialize, evict approved optional segments, and
reject.

Prompt Assembly may not summarize, compress, paraphrase, recalculate,
retrieve, repair, ask a provider to shorten content, or loosen a hard limit.

# Section 9: Eviction Policy

## 9.1 Eviction Authority

Governance owns eviction policy. Prompt Assembly executes that policy
deterministically. It does not invent eviction priorities at runtime.

## 9.2 Protected Context

The following context is protected and non-evictable when present:

1. `ADMIT_NARRATION` binding attestation.
2. Approved single-intent contract marker.
3. Approved narration-policy marker.
4. Required bounded current-turn content.
5. Core Composer projection required to narrate the admitted intent.
6. Exact deterministic values exposed for narration.
7. Required evidence-limitation disclosures.
8. Citation tokens required by included protected evidence.
9. Serialization and budget-policy identifiers.

If protected context cannot fit, narration is rejected.

## 9.3 Non-Protected Context

Only explicitly pre-classified optional segments may be evicted:

1. Optional Memory-summary projection segments.
2. Optional supplemental Composer projection segments.
3. Optional citation-backed supplemental evidence segments together with
   their no-longer-required citation tokens.

Absence of an explicit optional classification means the segment is
protected or ineligible, never silently evictable.

## 9.4 Eviction Order

The approved conceptual eviction order is:

1. Optional Memory-summary segments, in a governance-approved stable order.
2. Optional supplemental Composer segments, in a governance-approved stable
   order.
3. Optional supplemental evidence segments and only their now-unused
   citation tokens, in a governance-approved stable order.
4. Reject narration if the request still exceeds any hard limit.

Exact within-class priorities and tie-break rules remain required approvals
before implementation.

## 9.5 Eviction Failure Conditions

Reject narration when:

1. Protected context would need eviction.
2. A required limitation disclosure would be removed.
3. A citation token would become detached from included evidence.
4. A property-comparison citation binding would be weakened.
5. Eviction order is missing, ambiguous, or version-mismatched.
6. Eviction cannot produce a request within all hard limits.

## 9.6 Deterministic Requirements

Eviction must:

1. Be policy-versioned.
2. Use stable segment classes.
3. Use stable ordering and tie-breaks.
4. Produce auditable redacted omission metadata.
5. Never depend on provider feedback.
6. Never depend on model scoring.
7. Never summarize as a substitute for eviction.
8. Never weaken grounding coverage.

# Section 10: Security Review

## 10.1 Prompt Injection Risks

Risk:

Tenant-derived current-turn content, Composer text, Memory summaries, and
citation tokens can contain adversarial text.

Required controls:

1. Treat every tenant-derived segment as untrusted data.
2. Keep governed policy material structurally distinct from tenant-derived
   content.
3. Reject any segment that cannot be serialized without boundary ambiguity.
4. Give the provider no Tools, functions, browsing, retrieval, files,
   embeddings, memory, or delivery capability.
5. Ground original candidate narration downstream.
6. Reject unsupported claims rather than attempting repair.

Structural isolation reduces prompt-injection risk. It does not make provider
output trustworthy.

## 10.2 Data Leakage Risks

Risk:

Broad context packaging can expose unnecessary tenant data.

Required controls:

1. Use only the Admission-Gate-created provider-safe projection.
2. Deny unknown fields.
3. Exclude raw frontend payloads.
4. Exclude raw Composer and Memory artifacts.
5. Exclude raw identifiers.
6. Exclude transcripts, logs, database rows, and Tool payloads.
7. Keep assembly metadata redacted.

## 10.3 Memory Leakage Risks

Risk:

Memory summaries can become an indirect transcript channel.

Required controls:

1. Allow only explicitly governed Memory-summary classes.
2. Keep Memory segments bounded and redacted.
3. Make Memory segments optional by default unless a policy explicitly
   protects a class.
4. Preserve tenant scope upstream.
5. Prohibit full transcripts and unrestricted history.
6. Prohibit provider-side continuity.

## 10.4 Citation Leakage Risks

Risk:

Citation tokens can reveal scope, encode sensitive identifiers, or become
retrieval handles.

Required controls:

1. Approve opaque-token posture.
2. Expose only provider-necessary exact tokens.
3. Reject unsafe representations.
4. Prohibit retrieval by token.
5. Validate returned tokens downstream.

## 10.5 Cross-Tenant Leakage Risks

Risk:

Mixed-scope context could leave ValorAI before detection.

Required controls:

1. Admission Gate completes binding before assembly.
2. Prompt Assembly consumes one envelope only.
3. Prompt Assembly performs no merge.
4. Opaque internal attestations never become provider-visible content.
5. Any integrity ambiguity rejects narration.
6. `ACCESS_DENIED` never becomes scoped fallback.

## 10.6 Provider Leakage Risks

Risk:

Provider-specific packaging, logging, retry, or failover can silently widen
egress.

Required controls:

1. Use one approved provider profile.
2. Keep Prompt Assembly provider-neutral except for approved hard-limit
   metadata.
3. Keep provider credentials out-of-band.
4. Keep automatic retry and transparent failover forbidden by default.
5. Keep provider-side memory forbidden.
6. Keep content logging forbidden by default.

## 10.7 Grounding Bypass Risks

Risk:

An assembled request or provider response could reach delivery without
original-output grounding.

Required controls:

1. Prompt Assembly never delivers content.
2. Provider Adapter never delivers content.
3. Candidate Parser preserves original output.
4. Grounding acceptance is required before narrative persistence or delivery.
5. No pre-grounding client streaming.
6. No partial repaired narration.

## 10.8 Authority Escalation Risks

Risk:

Packaging rules can quietly become reasoning rules.

Required controls:

1. No dynamic summarization.
2. No semantic rewriting.
3. No numeric transformation.
4. No citation repair.
5. No contract merge.
6. No provider-generated follow-up.
7. No hidden context.
8. Governance approval for every new projection class.

# Section 11: General Question Review

## 11.1 Decision

`GENERAL_QUESTION` is `DETERMINISTIC_ONLY`.

Prompt Assembly does not participate.

## 11.2 Governance Implications

1. The Admission Gate must block provider invocation for `GENERAL_QUESTION`.
2. No generic narration contract may substitute for a missing grounded
   domain-evidence contract.
3. If a `GENERAL_QUESTION` envelope reaches Prompt Assembly, Prompt Assembly
   must reject narration as a boundary violation.
4. Any future general-question narration requires a separate architecture
   review and approved evidence posture.

# Section 12: Multi Intent Review

## 12.1 Decision

`MULTI_INTENT` narration is `DETERMINISTIC_ONLY`.

Prompt Assembly does not participate.

## 12.2 Governance Implications

1. Prompt Assembly may package exactly one approved intent contract.
2. Prompt Assembly may not merge intent contracts.
3. Prompt Assembly may not concatenate multiple provider-safe projections.
4. Prompt Assembly may not ask the provider to arbitrate multiple intents.
5. If a multi-intent envelope reaches Prompt Assembly without a separately
   approved combined contract, Prompt Assembly must reject narration.
6. Any future combined contract requires a separate architecture review.

# Section 13: Failure Policy

| Failure condition | Required outcome | Reason |
| --- | --- | --- |
| Missing authentication or scope proof | `ACCESS_DENIED` | No scoped disclosure is permitted when trust cannot be established. |
| Missing admitted envelope | `REJECT_NARRATION` | Prompt Assembly has no legal input. |
| Admission state other than `ADMIT_NARRATION` | Preserve upstream state and block provider invocation | Prompt Assembly may not reinterpret admission. |
| Missing narration-specific protected context in an otherwise authorized envelope | `REJECT_NARRATION` | Required content cannot be guessed or repaired. |
| Unsafe tenant-derived context representation | `REJECT_NARRATION` | Unsafe serialization must not reach a provider. |
| Unknown or unclassified projection segment | `REJECT_NARRATION` | Denied by default. |
| Raw JWT claim, identifier, secret, row, ORM entity, Tool payload, execution artifact, transcript, or log discovered | `REJECT_NARRATION`; use `ACCESS_DENIED` if confidentiality or scope trust is lost | Forbidden data must not be externalized. |
| Invalid Composer or Memory projection binding | `ACCESS_DENIED` for cross-scope risk; otherwise `REJECT_NARRATION` | Scope risk is distinct from narration-integrity failure. |
| Over-budget context after approved eviction | `REJECT_NARRATION` | Protected context never truncates silently. |
| Missing or ambiguous eviction policy | `REJECT_NARRATION` | Runtime heuristics are prohibited. |
| Grounding-ineligible context | `REJECT_NARRATION` | Provider invocation is pointless and unsafe when deterministic grounding cannot evaluate the future candidate. |
| Tenant mismatch | `ACCESS_DENIED` | No provider invocation and no scoped fallback. |
| Workspace, scenario, or broker-session mismatch | `ACCESS_DENIED` | No provider invocation and no scoped fallback. |
| Foreign or cross-workspace citation | `ACCESS_DENIED` | Citation mismatch indicates scope risk. |
| In-scope malformed, missing, fabricated, aliased, unsupported, or unsafe citation | `REJECT_NARRATION` | Narration cannot proceed safely. |
| Provider-safe projection failure | `REJECT_NARRATION`; use `ACCESS_DENIED` if failure exposes scope uncertainty | Unknown or denylisted content blocks egress. |
| Serialization-policy or tokenizer-version mismatch | `REJECT_NARRATION` | Exact budget and safe representation cannot be proven. |

## 13.1 Fail-Closed Rule

```text
Only a successfully assembled request derived from ADMIT_NARRATION may reach
the Provider Adapter.
```

`DETERMINISTIC_ONLY`, `REJECT_NARRATION`, and `ACCESS_DENIED` must never
contact a provider.

# Section 14: Grounding Relationship

## 14.1 Prompt Assembly to Grounding

Prompt Assembly may emit bounded redacted assembly metadata for downstream
correlation:

1. Assembly-policy version.
2. Serializer version.
3. Tokenizer version.
4. Provider-profile identifier.
5. Included projection-segment identifiers.
6. Evicted optional-segment identifiers.
7. Final budget accounting.
8. Opaque envelope-binding attestation.

This metadata is internal. It must not become provider-visible content unless
an individual bounded marker is explicitly approved.

## 14.2 Grounding to Prompt Assembly

Grounding has no runtime backchannel into Prompt Assembly.

Grounding must never:

1. Ask Prompt Assembly to repair a candidate.
2. Ask Prompt Assembly to produce a second request.
3. Ask Prompt Assembly to widen context.
4. Ask Prompt Assembly to add citations.
5. Ask Prompt Assembly to change deterministic values.
6. Trigger retry or failover.

## 14.3 Allowed Interactions

Allowed interactions are one-way and bounded:

```text
Admission Gate
  -> admitted envelope and provider-safe projection
  -> Prompt Assembly
  -> bounded provider request artifact
  -> Provider Adapter
  -> original provider response
  -> Candidate Parser
  -> Grounding Layer
```

The Grounding Layer also receives its internal grounding manifest through a
separate internal path. Prompt Assembly does not create or weaken that
manifest.

## 14.4 Forbidden Interactions

Forbidden interactions include:

1. Grounding logic inside Prompt Assembly.
2. Prompt Assembly repair after grounding rejection.
3. Provider feedback-driven reassembly.
4. Candidate-driven optional-context expansion.
5. Grounding-driven citation mutation.
6. Grounding-driven provider retry.
7. Direct Prompt Assembly to delivery paths.

## 14.5 Influence Boundaries

Prompt Assembly influences only representation and bounded omission of
pre-approved optional context.

Prompt Assembly must not influence:

1. Truth.
2. Calculation.
3. Evidence.
4. Scope.
5. Narration eligibility.
6. Grounding acceptance.
7. Persistence.
8. Delivery.

## 14.6 Trust Boundaries

| Artifact or layer | Trust posture |
| --- | --- |
| Admission Gate `ADMIT_NARRATION` decision | Trusted only as a deterministic upstream attestation bound to approved policy versions. |
| Provider-safe projection | Trusted as the maximum eligible egress set, but tenant-derived content remains untrusted data. |
| Prompt Assembly output | Trusted only as a bounded request artifact, never as truth. |
| Provider | Untrusted external processor. |
| Provider response | Untrusted candidate narration. |
| Grounding Layer | Exclusive downstream acceptance authority for candidate narration. |

# Section 15: Risk Register

| Risk | Impact | Likelihood | Mitigation | Residual risk |
| --- | --- | --- | --- | --- |
| Hidden side input enters Prompt Assembly | Cross-tenant leakage or authority drift | Medium | Accept one admitted envelope only; deny retrieval and hidden arguments; reject unknown segments. | Low after conformance evidence |
| Raw identifiers leak through internal metadata | Tenant or session disclosure | Medium | Use opaque non-semantic attestations; forbid raw scope identifiers; audit provider-visible output. | Low |
| Current-turn injection changes provider behavior | Unsupported candidate narration | High | Structural isolation, no provider capabilities, original-output grounding, deterministic fallback. | Medium because providers remain untrusted |
| Stored Memory-summary injection persists across turns | Repeated unsupported candidate narration | Medium | Redacted bounded allowlisted summary classes, structural isolation, no provider continuity, grounding rejection. | Medium |
| Citation token injection alters serialization | Policy confusion or leakage | Medium | Approve safe representability rule; reject unsafe exact tokens; prohibit repair. | Low after approval |
| Citation token exposes internal structure | Metadata leakage | Medium | Approve opaque-token posture; expose only necessary tokens; prohibit retrieval by token. | Low to medium |
| Budget overflow causes silent truncation | Missing limitations or grounding context | Medium | Protected-content rule; deterministic eviction; reject when protected context cannot fit. | Low |
| Eviction removes evidence while retaining claim support | Ungroundable or misleading narration | Medium | Evict supplemental evidence atomically with unused citations; preserve core context and limitations. | Low |
| Tokenizer or serializer drift changes budget result | Unreviewed provider request size or inconsistent behavior | Medium | Version and approve tokenizer and serializer; reject version mismatch. | Low |
| Prompt Assembly starts summarizing content | Composer or Memory ownership drift | Medium | Representation-only transformation; no dynamic compression; architecture conformance review. | Low |
| Provider-specific extras widen egress | Unreviewed external disclosure | Medium | Provider-neutral assembly; deny unknown fields; profile approval; no hidden provider additions. | Low |
| General-question flow reaches provider | Ungrounded open-ended narration | Medium | `DETERMINISTIC_ONLY`; reject any accidental assembly path. | Low |
| Multi-intent contract merge occurs implicitly | Cross-contract authority expansion | Medium | Single-contract invariant; deterministic-only multi-intent behavior. | Low |
| Grounding rejection triggers automatic repair or retry | Duplicate egress and hidden authority repair | Medium | No backchannel; retry and failover forbidden by default; deterministic fallback. | Low |
| Assembly metadata becomes a shadow transcript store | Compliance and leakage risk | Medium | Bounded redacted non-content metadata only; retention approval; no content logging by default. | Low |
| Legacy broker LLM path bypasses Prompt Assembly | Ungoverned runtime activation | High until retired | Isolate and retire legacy LLM activation path before modern activation. | Medium until retirement evidence exists |

# Section 16: GO / NO-GO Review

## 16.1 Architecture Strengths

1. Prompt Assembly is constrained to one deterministic packaging boundary.
2. Admission, assembly, provider transport, parsing, grounding, persistence,
   and delivery remain separate.
3. Provider-visible content is limited to an already-approved minimized
   projection.
4. Budget enforcement is fail-closed at both preflight and final assembly.
5. Eviction cannot remove protected context.
6. Memory and Composer authority remain upstream.
7. Citation identity remains immutable.
8. General-question and multi-intent flows remain deterministic-only.
9. Providers remain untrusted and stateless.

## 16.2 Architecture Weaknesses

1. Prompt injection cannot be eliminated by packaging alone.
2. Citation tokens need an explicitly approved opaque-token and safe
   representability posture.
3. Exact hard limits are still undecided.
4. Tokenizer and serializer versions are still undecided.
5. Exact within-class eviction priorities and tie-break rules are still
   undecided.
6. Provider-specific profiles are still unapproved.
7. Legacy broker LLM activation remains a bypass risk until retired.

## 16.3 Remaining Blockers

Implementation remains blocked until governance explicitly approves:

1. Prompt Assembly as a representation-only deterministic boundary.
2. One admitted scoped envelope as the only input.
3. The internal-envelope versus external-projection separation.
4. The exact provider-visible allowlist and denylist.
5. The protected-context list.
6. The optional-context segment classes.
7. The exact stable eviction order and tie-break rules.
8. The tokenizer and serializer versions.
9. Fixed-overhead and response-reserve accounting.
10. Exact hard request, response, output-token, character, citation-count,
    and timeout limits.
11. Safe citation-token representability rules.
12. Opaque citation-token posture and prohibition on retrieval by token.
13. Opaque non-semantic internal binding attestations instead of raw scope
    identifiers.
14. Bounded redacted assembly metadata and retention posture.
15. Single-contract enforcement.
16. Deterministic-only handling for `GENERAL_QUESTION`, clarification,
    unsupported, generic, and multi-intent flows.
17. No repair, retry, failover, second-pass assembly, or provider-feedback
    loop.
18. Provider-specific governance profiles.
19. Isolation and retirement of the legacy broker LLM activation path.
20. Governed disposition of unauthorized prior Phase 5.5C.6 artifacts.
21. A separate Phase 5.5C.6H Grounding Architecture Review.

## 16.4 Required Approvals

Required sign-off roles:

1. AI Systems Architecture.
2. Prompt Engineering Architecture.
3. Multi-Tenant Security Architecture.
4. LLM Security and Governance.
5. Reliability Architecture.
6. Privacy and Compliance.
7. Product or platform owner accountable for accepted narration behavior.

## 16.5 Architecture Decision

Prompt Assembly Architecture is conditionally approvable only as a
deterministic representation-only boundary after `ADMIT_NARRATION`.

Any architecture that retrieves context, resolves scope, summarizes content,
changes facts, calculates values, mutates citations, selects providers,
grounds output, persists content, or delivers narration is `NO_GO`.

# Final Decision

```text
PROMPT_ASSEMBLY_ARCHITECTURE: CONDITIONAL_GO

IMPLEMENTATION: NO_GO

PROVIDER_INTEGRATION: NO_GO

LLM_RUNTIME_ACTIVATION: NO_GO

PRODUCTION_PROMOTION: NO_GO

NEXT_ALLOWED_PHASE:

PHASE 5.5C.6H GROUNDING ARCHITECTURE REVIEW
```
