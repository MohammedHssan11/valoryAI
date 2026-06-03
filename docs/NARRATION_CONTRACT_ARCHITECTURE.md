# ValorAI Narration Contract Architecture

Decision date: 2026-06-02  
Phase: 5.5C.6D Narration Contract Architecture  
Status: Architecture only  

## 1. Locked Governance Rule

```text
Planner decides.
Executor executes.
Composer computes.
Memory remembers.
LLM narrates.
```

The LLM is never an authority layer. It receives a bounded provider-safe
projection only after the deterministic chain and Narration Admission Gate
complete. Its output is untrusted candidate narration until deterministic
grounding accepts it.

## 2. Architecture Decision

```text
NARRATION_CONTRACT_ARCHITECTURE: CONDITIONAL_GO
LLM_AUTHORITY: NONE
NARRATION_ACTIVATION: DEFAULT_OFF
EXISTING_LLM_RUNTIME_ACTIVATION: NO_GO
```

The narration contract architecture may advance to governance approval. It
does not approve Prompt Assembly architecture, implementation, provider
activation, runtime activation, or production promotion.

## 3. Narration Definition

Narration is a bounded presentation of locked deterministic context. It may:

1. Restate an upstream fact exactly when the approved intent contract permits
   that fact.
2. Describe an upstream status, limitation, or evidence-depth disclosure.
3. Summarize upstream evidence without changing its meaning.
4. Reference an immutable citation token exactly as received.
5. State that evidence is sparse, insufficient, partially available, or
   unavailable when that status is upstream-authorized.

Narration may not:

1. Create a new fact, value, calculation, comparison, ranking, recommendation,
   forecast, assumption, citation, or evidence record.
2. Repair missing upstream evidence.
3. Convert sparse evidence into confident language.
4. Interpret a failed or denied context as permission to continue.
5. Replace the Composer-owned frontend payload.

## 4. Narration Contract Surface

Each approved intent contract governs four conceptual narration elements:

| Element | Purpose | Authority |
| --- | --- | --- |
| Narrative text | Human-readable explanation of approved upstream facts. | LLM candidate text, accepted only after grounding. |
| Limitation disclosure | Sparse, insufficient, partial, or unavailable evidence statement. | Upstream status narrated without weakening. |
| Citation references | Exact references to received immutable citation IDs. | Composer and Memory owned; LLM may reference but never create. |
| Narration status | Indicates accepted, skipped, rejected, or deterministic-only behavior. | Deterministic runtime owned. |

The contract does not authorize an LLM-owned schema, API, provider, prompt, or
persistence model.

## 5. Allowed Evidence

Narration may describe only evidence exposed through the validated scoped
narration envelope and approved provider-safe projection:

1. Composer-owned `compressed_context`.
2. Composer-owned deterministic status and supported-intent marker.
3. Composer-owned approved arithmetic already present in the context.
4. Memory-owned bounded summaries approved for external egress.
5. Immutable Composer and Memory citation tokens.
6. Upstream sparse, insufficient, partial-success, and failure disclosures.
7. Bounded current-turn content as untrusted user data, not as evidence.

## 6. Evidence That Must Never Be Narrated

Narration must never expose or infer from:

1. `ExecutionPlan`.
2. Raw `ExecutionResult`.
3. Raw Tool 1-8 payloads.
4. ORM entities, database rows, direct query output, or unrestricted logs.
5. Full transcripts or unrestricted message history.
6. Raw `frontend_payload` unless a separately approved provider-safe
   projection explicitly includes a field.
7. Foreign-tenant, deleted-scope, `FAILED`, or `ACCESS_DENIED` context.
8. Authentication tokens, JWT claims, secrets, provider keys, or connection
   strings.
9. Hidden model knowledge, external retrieval, provider memory, or
   unsupported world knowledge.
10. Fabricated evidence IDs, aliases, placeholder comparables, synthetic
    assumptions, or replacement records.

## 7. Exact Pass-Through Rule

An upstream deterministic fact may be narrated only when:

1. The intent-specific contract permits the fact category.
2. The fact appears in the approved provider-safe projection.
3. Any numeric value is repeated exactly without calculation, rounding,
   conversion, recombination, ranking, or extrapolation.
4. Required citation references are exact received tokens.
5. The wording does not increase certainty beyond upstream status.

Repeating an approved upstream value is narration. Deriving a new value from
approved upstream values is calculation and is forbidden.

## 8. Citation Contract

Citations are pass-through only, immutable, and non-generated.

Legal narration citation syntax:

```text
[citation:<exact-received-id>]
```

The wrapper is presentation syntax only. `<exact-received-id>` must match a
token in the immutable scoped citation package byte-for-byte.

Legal citation behavior:

1. Reference an exact received `valuation_id`, optional `tool_event_id`, or
   optional `comparable_id` token when exposed by the scoped package.
2. Attach one or more exact citations to an evidence-dependent statement.
3. Omit a citation claim when no legal citation token exists.
4. Disclose sparse or insufficient evidence instead of creating a citation.

Illegal citation behavior:

1. Invent, alias, rename, normalize, enrich, infer, repair, or resolve a
   citation ID.
2. Create fallback evidence IDs.
3. Create placeholder comparable records.
4. Cite a token outside the scoped immutable package.
5. Use a citation from another tenant, scenario, session, or response.

## 9. Sparse, Insufficient, Partial, and Failed Evidence

### Sparse Evidence

Sparse evidence means some approved evidence exists but its depth is limited.
Narration may describe the available evidence and must disclose the limitation.
It may not fill gaps, imply representative coverage, or strengthen certainty.

### Insufficient Evidence

Insufficient evidence means the upstream deterministic context does not
support a substantive statement. Narration must say that the evidence is
insufficient for the requested conclusion. It may not guess, generalize, or
substitute provider knowledge.

### Partial Success

Partial success means an approved deterministic slice succeeded while another
slice failed or is unavailable. Narration may describe only the successful
slice and must identify the unavailable slice without speculation.

### Failure

Authentication, tenant binding, `ACCESS_DENIED`, invalid scope, unsupported
intent, invalid citation binding, or failed grounding causes fail-closed
narration behavior. No scoped narrative disclosure is allowed when
authorization or tenant binding fails.

## 10. Narration Activation Classes

| Class | Meaning |
| --- | --- |
| `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | An intent-specific contract exists. Narration remains off until governance approval and later Prompt Assembly, implementation, and runtime gates pass. |
| `DETERMINISTIC_ONLY` | No LLM narration may activate. Existing deterministic response behavior remains authoritative. |
| `REJECT_NARRATION` | Narration must fail closed for the current request. |

Nine evidence-bearing domain intents are `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF`:

1. `VALUATION`
2. `EXPLAINABILITY`
3. `COMPARABLES`
4. `FAIRNESS`
5. `WHAT_IF`
6. `NEGOTIATION`
7. `INVESTMENT`
8. `MARKET_INSIGHT`
9. `PROPERTY_COMPARISON`

Clarification, `GENERAL_QUESTION`, unsupported intents, generic catch-all
flows, and multi-intent narration are `DETERMINISTIC_ONLY` until separate
contracts are approved.

## 11. Grounding Requirements

Grounding must validate the original unmodified candidate narration. It must
verify:

1. The intent is approved for narration activation.
2. Every factual statement belongs to an allowed narration field.
3. Every numeric value is an exact permitted upstream pass-through value.
4. No new arithmetic, percentage, delta, comparison, rank, recommendation,
   threshold, offer, forecast, or assumption appears.
5. Every citation token is legal, exact, immutable, scoped, and received.
6. Sparse, insufficient, partial, and failure disclosures are preserved.
7. No hidden external knowledge, provider memory, or unsupported inference is
   introduced.
8. The narration does not contradict Composer or Memory context.

Grounding rejection is required for any violation. Candidate narration must
not be repaired before the rejection decision.

## 12. Global Narration Rejection Conditions

Reject narration when:

1. Authentication, tenant, workspace, optional scenario, optional session,
   response, memory, or citation binding fails.
2. Memory status is `FAILED` or `ACCESS_DENIED`.
3. The intent is deterministic-only or unsupported.
4. Multi-intent narration is attempted without a separately approved
   contract.
5. The provider-safe projection or prompt budget is invalid.
6. The candidate includes a prohibited claim.
7. The candidate includes a fabricated, missing, foreign, or unsupported
   citation.
8. The candidate creates new arithmetic or changes an upstream value.
9. The candidate weakens an evidence limitation.
10. The candidate cannot be deterministically grounded.

## 13. Fallback Requirements

Narration failure must fail closed. When authorization remains valid, delivery
may fall back to the Composer-owned deterministic frontend payload with an
explicit narration status. Authorization or tenant-binding failure permits no
scoped disclosure.

## 14. Formal Decisions

### D-01: Exact Pass-Through Narration Only

**Decision**

The LLM may summarize or repeat permitted upstream facts exactly. It may not
derive new claims.

**Reason**

The deterministic chain already owns truth, calculation, and evidence.

**Alternatives considered**

1. Permit model reasoning over Composer facts.
2. Permit calculations when inputs are cited.
3. Permit unsupported general real-estate knowledge.

**Risks**

Natural language can disguise a new inference as a summary.

**Mitigations**

Use intent-specific allowlists and deterministic grounding of original output.

**GO / NO-GO impact**

Any derivation authority is `NO-GO`.

### D-02: Citation Identity Never Moves Into Narration

**Decision**

Citations remain immutable upstream artifacts. Narration may reference exact
tokens only.

**Reason**

Citation aliases and synthesized records create a second evidence system.

**Alternatives considered**

1. Permit friendly aliases.
2. Permit fallback tokens.
3. Permit model-generated references.

**Risks**

Sparse evidence can pressure narration to fabricate support.

**Mitigations**

Require limitation disclosure when legal citations are absent.

**GO / NO-GO impact**

Citation mutation or invention is `NO-GO`.

### D-03: Domain Narration Is Default-Off and Per-Intent

**Decision**

Every evidence-bearing intent is default-off until its contract is approved.
No generic fallback narration mode exists.

**Reason**

Each Tool has distinct authority limits and failure semantics.

**Alternatives considered**

1. One generic narration contract.
2. Enable all intents together.
3. Let the provider infer intent behavior.

**Risks**

Contract drift can remain hidden behind generic prose.

**Mitigations**

Require per-intent activation and grounding coverage.

**GO / NO-GO impact**

Catch-all narration is `NO-GO`.

## 15. Minimum Approvals Before Phase 5.5C.6E

Before Prompt Assembly Architecture may begin, governance must explicitly
approve:

1. Exact pass-through narration only.
2. The nine intent-specific contracts.
3. Deterministic-only treatment for clarification, general-question,
   unsupported, and multi-intent flows.
4. The prohibited-claims matrix.
5. Immutable pass-through citation behavior and exact citation syntax.
6. Sparse, insufficient, partial-success, and failure language rules.
7. Original-output grounding and rejection conditions.
8. Deterministic fallback behavior.
9. Default-off per-intent activation.

