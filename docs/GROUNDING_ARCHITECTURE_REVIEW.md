# ValorAI Phase 5.5C.6H Grounding Architecture Review

Review date: 2026-06-02  
Review scope: Grounding Architecture  
Review mode: Architecture only  
Implementation status: Prohibited  

## Authoritative Sources

This review is based on the complete authoritative Phase 5.5C source set:

1. `PROJECT_MASTER_STATE_V2.md`
2. Approved Intent Engine documents.
3. Approved Tool Planner documents.
4. Approved Tool Executor documents.
5. Approved Response Composer documents.
6. Approved Memory Integration documents.
7. All Phase 5.5C.6B architecture documents.
8. `NARRATION_CONTRACT_ARCHITECTURE.md`
9. `NARRATION_ACTIVATION_POLICY.md`
10. `NARRATION_PROHIBITED_CLAIMS_MATRIX.md`
11. All nine narration contracts.
12. `NARRATION_APPROVAL_DECISION.md`
13. `PHASE_5_5C_6FG_ARCHITECTURE_REVIEW.md`
14. `PHASE_5_5C_6E_PROMPT_ASSEMBLY_ARCHITECTURE_REVIEW.md`

The review also performed the required read-only forensic inspection of the
existing grounding-related LLM paths. No source code, tests, validators,
contracts, prompts, migrations, Docker files, or runtime state were modified.

## Locked Rule

```text
Planner decides.
Executor executes.
Composer computes.
Memory remembers.
LLM narrates.
Grounding validates.
```

Grounding must never calculate, narrate, repair, summarize, infer, retrieve,
re-run providers, reassemble prompts, or create evidence.

# Section 1: Grounding Purpose Review

## 1.1 Purpose

Grounding is the deterministic post-provider validation boundary for original
candidate narration. Its only mission is to decide whether the original
candidate may proceed toward optional Memory-owned accepted-narration commit
and Delivery.

Grounding answers one narrow question:

> Does this original candidate narration remain entirely inside the exact
> upstream facts, immutable citations, evidence limitations, intent contract,
> and prohibited-claims policy already approved for this request?

## 1.2 Scope

Grounding validates:

1. Original candidate narration only.
2. Exact upstream pass-through values exposed by the internal grounding
   manifest.
3. Exact immutable scoped citation references.
4. Intent-specific narration-contract compliance.
5. Prohibited-claim absence.
6. Evidence-limitation preservation.
7. Binding integrity and policy-version consistency.

## 1.3 Authority

Grounding is:

| Role | Decision | Reason |
| --- | --- | --- |
| Validator | `YES` | It validates the original candidate against locked upstream authority. |
| Auditor | `CONDITIONAL` | It may emit bounded redacted decision metadata, but it does not own a content archive or unrestricted logs. |
| Gatekeeper | `YES` | Accepted narration cannot persist or reach Delivery without Grounding acceptance. |
| Narrator | `NO` | It cannot create, edit, shorten, summarize, sanitize, or repair narration. |
| Calculator | `NO` | Composer and upstream Tools retain all calculation authority. |
| Retrieval layer | `NO` | Memory and upstream scope owners retain retrieval authority. |

## 1.4 Architectural Form

Grounding should exist as:

| Form | Decision | Reason |
| --- | --- | --- |
| Layer | `YES` | It is a mandatory stage after Candidate Parser and before persistence or Delivery. |
| Contract boundary | `YES` | It has narrow allowed inputs, explicit outputs, and fail-closed behavior. |
| Governance authority | `YES`, narrowly | It exclusively decides candidate narration acceptance or rejection. |
| Independent I/O service | `NO` | Database, network, provider, Tool, memory, and retrieval access would create ownership drift. |

# Section 2: Grounding Ownership Matrix

The full normative matrix is in
`GROUNDING_BOUNDARY_OWNERSHIP_MATRIX.md`.

| Layer | Exclusive ownership |
| --- | --- |
| Prompt Assembly | Deterministic bounded request serialization and final exact budget decision. |
| Provider Adapter | Stateless approved-profile transport and original-response preservation. |
| Candidate Parser | Parse original provider response without repair, enrichment, or authority mutation. |
| Grounding | Validate original candidate against one internal grounding manifest, immutable citations, one contract, and prohibited-claims policy. |
| Memory Integration | Pre-generation governed memory work and optional separately approved post-generation accepted-narration commit. |
| Delivery | Deliver Composer-owned deterministic payload and optional accepted grounded narration. |

Grounding must not overlap with any neighboring layer.

# Section 3: Grounding Input Review

The full input matrix is in `GROUNDING_INPUT_OUTPUT_MATRIX.md`.

Grounding may receive only:

1. Original parsed candidate narration linked to the preserved original
   provider response.
2. One internal grounding manifest produced upstream by the Admission Gate.
3. One immutable scoped citation package.
4. Bounded redacted Prompt Assembly correlation metadata.
5. Approved narration-contract and prohibited-claims policy versions.
6. Opaque binding attestations required to prove artifact continuity.

Grounding must never receive raw `MemoryContext`, raw `ComposedResponse`,
`ExecutionResult`, `ExecutionPlan`, Tool payloads, database rows, ORM entities,
JWT claims, raw frontend payload, provider credentials, or hidden retrieval
results.

# Section 4: Grounding Output Review

Grounding may output only one deterministic decision:

| Output | Meaning |
| --- | --- |
| `ACCEPT_NARRATION` | Original candidate is fully grounded and may proceed under downstream policy. |
| `REJECT_NARRATION` | Candidate is not acceptable; narration is suppressed and authorized deterministic fallback may remain available. |
| `ACCESS_DENIED` | A foreign, cross-scope, or untrusted binding condition was detected; narration and scoped fallback are blocked. |

The following are bounded reason categories, not separate delivery states:

| Reason category | Parent outcome |
| --- | --- |
| `UNGROUNDED` | `REJECT_NARRATION` |
| `POLICY_VIOLATION` | `REJECT_NARRATION` |
| `CITATION_MISMATCH` | `REJECT_NARRATION` or `ACCESS_DENIED` for cross-scope risk |
| `CONTRACT_MISMATCH` | `REJECT_NARRATION` |
| `BINDING_MISMATCH` | `ACCESS_DENIED` |
| `AMBIGUOUS_VALIDATION` | `REJECT_NARRATION` |

Grounding must not output repaired narration, sanitized narration, partial
narration, replacement values, new citations, new evidence, prompts, provider
requests, persistence operations, or delivery instructions.

# Section 5: Numeric Grounding Review

The normative policy is in `GROUNDING_NUMERIC_VALIDATION_POLICY.md`.

Grounding may validate exact upstream pass-through use of:

1. Valuation numbers.
2. Composer-owned property-comparison deltas.
3. Composer-owned percentage deltas.
4. Composer-owned comparable counts, averages, minimums, and maximums.
5. Tool-owned approved values already exposed through the grounding manifest.
6. Exact upstream confidence labels.

Grounding may not:

1. Recompute a value.
2. Recalculate a delta.
3. Recalculate a percentage.
4. Check arithmetic by independently deriving a result.
5. Round, convert, normalize, or repair a number.
6. Fill a missing value.
7. Compare values to create a new claim.

Grounding validates membership and exactness. It does not become a second
Composer.

# Section 6: Citation Grounding Review

The normative policy is in `GROUNDING_CITATION_POLICY.md`.

Allowed citation categories:

1. `valuation_id`
2. Optional `tool_event_id`
3. Optional `comparable_id`

Grounding validates exact immutable scoped token use. It performs no lookup,
resolution, aliasing, enrichment, repair, or retrieval.

Required outcomes:

| Condition | Outcome |
| --- | --- |
| Fabricated citation | `REJECT_NARRATION` |
| Foreign or cross-tenant citation | `ACCESS_DENIED` |
| Modified citation | `REJECT_NARRATION` |
| Missing required citation | `REJECT_NARRATION` |
| Extra unsupported citation | `REJECT_NARRATION` |
| Citation bound to wrong compared property | `REJECT_NARRATION` or `ACCESS_DENIED` when cross-scope |

# Section 7: Narration Contract Enforcement Review

The detailed review is in
`GROUNDING_NARRATION_CONTRACT_ENFORCEMENT.md`.

Grounding must apply exactly one approved intent-specific contract:

1. `VALUATION`
2. `EXPLAINABILITY`
3. `COMPARABLES`
4. `FAIRNESS`
5. `WHAT_IF`
6. `NEGOTIATION`
7. `INVESTMENT`
8. `MARKET_INSIGHT`
9. `PROPERTY_COMPARISON`

Grounding may validate candidate compliance with the selected contract. It
must not merge contracts, invent fields, create stronger language, or
reinterpret upstream authority.

# Section 8: Prohibited Claim Review

The detailed review is in
`GROUNDING_PROHIBITED_CLAIMS_ENFORCEMENT.md`.

Grounding must reject original candidate narration containing:

1. Forecasts or future prices.
2. Predictions.
3. Investment advice.
4. New ROI, IRR, CAGR, yield, appreciation, or return claims.
5. Property rankings.
6. Recommendations.
7. Winner declarations.
8. Invented evidence.
9. Hidden calculations.
10. New offers, tactics, strategies, thresholds, causal claims, synthetic
    assumptions, or synthetic market trends.

If Grounding cannot deterministically distinguish a legal exact pass-through
claim from a forbidden new claim, it must reject narration.

# Section 9: General Question Review

`GENERAL_QUESTION` remains `DETERMINISTIC_ONLY`.

| Question | Decision |
| --- | --- |
| Should a provider be invoked? | `NO` |
| Should Grounding see a candidate? | `NO` |
| Should Grounding run? | `NO` |
| What if a `GENERAL_QUESTION` candidate reaches Grounding? | Reject as a contract-boundary violation. |

No generic LLM fallback is approved.

# Section 10: Multi Intent Review

Multi-intent narration remains `DETERMINISTIC_ONLY`.

| Question | Decision |
| --- | --- |
| Should Grounding support merged multi-intent narration? | `NO` |
| Should contracts merge? | `NO` |
| Should a provider be invoked for multi-intent narration? | `NO` |
| What if a multi-intent candidate reaches Grounding? | Reject as a contract-boundary violation. |

Any future combined-intent narration requires a separate architecture review.

# Section 11: Failure Matrix

The full matrix is in `GROUNDING_FAILURE_MATRIX.md`.

Grounding is fail-closed:

1. Any unsupported claim rejects narration.
2. Any fabricated or modified citation rejects narration.
3. Any cross-tenant or cross-workspace evidence returns `ACCESS_DENIED`.
4. Any malformed candidate rejects narration.
5. Any ambiguity rejects narration.
6. No failure triggers repair, retry, prompt reassembly, second-provider use,
   partial delivery, or persistence.

# Section 12: Security Review

The full review is in `GROUNDING_SECURITY_REVIEW.md`.

Grounding must treat:

1. Provider output as untrusted.
2. Tenant-derived prompt content as potentially adversarial.
3. Citation tokens as scoped immutable values, not retrieval handles.
4. Memory summaries as upstream-governed data, not instructions.
5. Every unknown claim, field, citation, or binding as rejectable.

Grounding must have no database, network, Tool, provider, Memory retrieval,
prompt assembly, or delivery capability.

# Section 13: Determinism Review

The full review is in `GROUNDING_DETERMINISM_REVIEW.md`.

Grounding must be:

1. Deterministic.
2. Repeatable.
3. Restart-stable.
4. Provider-independent.
5. Policy-version-bound.
6. No-I/O.
7. Fail-closed under ambiguity.

The same original candidate, manifest, citations, bindings, and policy
versions must always yield the same decision and bounded reason categories.

# Section 14: Trust Boundary Review

The full review is in `GROUNDING_TRUST_BOUNDARY_REVIEW.md`.

Grounding sits between untrusted candidate narration and trusted downstream
acceptance:

| Artifact or layer | Trust posture |
| --- | --- |
| Provider | Untrusted external processor |
| Provider response | Untrusted original response |
| Candidate Parser | Trusted only to preserve and parse without repair |
| Prompt Assembly | Trusted only as a bounded request packager |
| Narration contracts | Trusted normative governance |
| Composer | Trusted upstream deterministic arithmetic owner |
| Memory | Trusted upstream governed memory owner |
| Grounding manifest | Trusted only when bound to the admitted request and approved versions |
| Delivery | Downstream consumer that must honor Grounding outcome |

# Section 15: Risk Register

The enterprise risk register is in `GROUNDING_RISK_REGISTER.md`.

The highest current risks are:

1. Mutation before grounding.
2. Citation fabrication.
3. Legacy grounding reuse.
4. Incomplete prohibited-claim enforcement.
5. Raw Memory coupling.
6. Hidden persistence outside Memory ownership.
7. Legacy fallback revalidation and self-healing behavior.
8. Competing activatable LLM paths.

# Section 16: GO / NO-GO Decision

## 16.1 Required Forensic Review

The mandatory forensic review found grounding-boundary violations:

| Review area | Finding | Decision impact |
| --- | --- | --- |
| Authority drift | Existing unauthorized adapter overwrites parsed authoritative values before grounding. | `NO_GO` |
| Ownership overlap | Existing adapter owns persistence and citation synthesis outside Memory and Composer. | `NO_GO` |
| Hidden retrieval | Existing adapter queries the latest workspace chat directly. | `NO_GO` |
| Hidden calculations | Existing grounding path does not enforce prohibited free-text arithmetic and receives synthetic zero-price comparable wrappers. | `NO_GO` |
| Hidden memory usage | Existing prompt path consumes raw `MemoryContext` slices and session context. | `NO_GO` |
| Hidden provider trust | Existing path depends on prompt instructions and incomplete legacy checks. | `NO_GO` |
| Grounding repair behavior | Existing path replaces parsed authoritative values before validation. | `NO_GO` |
| Grounding retry behavior | No approved Grounding retry exists; legacy runtime contains retry-adjacent and fallback flows that must not define the modern boundary. | `NO_GO` |
| Grounding self-healing behavior | Legacy broker finalization creates and revalidates a fallback response after failure. | `NO_GO` |
| Grounding inference behavior | Existing grounding validator does not enforce all inference prohibitions required by the nine narration contracts. | `NO_GO` |

## 16.2 Architecture Strengths of the Required Target

1. Grounding can be defined as a narrow no-I/O acceptance gate.
2. Composer remains the arithmetic authority.
3. Memory remains the memory authority.
4. Citation packages remain immutable.
5. Providers remain untrusted.
6. Original candidate narration remains unmodified before decision.
7. General-question and multi-intent narration remain deterministic-only.

## 16.3 Current Blockers

The observed runtime shape contains prohibited grounding behavior. The target
boundary is documented for governance, but it is not approved for
implementation or activation.

## 16.4 Decision

```text
ARCHITECTURE_DECISION: NO_GO

GROUNDING_ARCHITECTURE: NO_GO

TARGET_GROUNDING_BOUNDARY: DEFINED_FOR_GOVERNANCE_REVIEW_ONLY

OBSERVED_GROUNDING_RUNTIME: NO_GO

IMPLEMENTATION: NO_GO

RUNTIME_ACTIVATION: NO_GO

PRODUCTION_PROMOTION: NO_GO

NEXT_ALLOWED_PHASE: NONE

NEXT_ALLOWED_WORK: GOVERNANCE RESOLUTION OF FORENSIC BLOCKERS ONLY
```

