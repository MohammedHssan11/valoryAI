# ValorAI Narration Activation Policy

Decision date: 2026-06-02  
Phase: 5.5C.6D Narration Contract Architecture  
Status: Architecture only  

## 1. Activation Principle

LLM narration is optional, default-off, per-intent, and fail-closed. The
existence of an intent contract makes an intent eligible for future activation
review. It does not activate narration.

No generic narration fallback exists.

## 2. Activation States

| State | Meaning |
| --- | --- |
| `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | A contract exists. Later governance, Prompt Assembly architecture, implementation review, and runtime activation evidence are still required. |
| `DETERMINISTIC_ONLY` | The existing deterministic response remains the only allowed behavior. |
| `REJECT_NARRATION` | No LLM narration may proceed for the current request. |

## 3. Intent Activation Matrix

| Intent | State | Contract | Activation boundary |
| --- | --- | --- | --- |
| `VALUATION` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | `VALUATION_NARRATION_CONTRACT.md` | Exact narration of upstream valuation facts only. |
| `EXPLAINABILITY` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | `EXPLAINABILITY_NARRATION_CONTRACT.md` | Exact narration of upstream explanations and limitations only. |
| `COMPARABLES` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | `COMPARABLES_NARRATION_CONTRACT.md` | Exact narration of received comparable evidence and Composer summaries only. |
| `FAIRNESS` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | `FAIRNESS_NARRATION_CONTRACT.md` | Exact narration of Router-owned fairness output only. |
| `WHAT_IF` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | `WHAT_IF_NARRATION_CONTRACT.md` | Exact narration of Tool 5 scenario output and approved deltas only. |
| `NEGOTIATION` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | `NEGOTIATION_NARRATION_CONTRACT.md` | Exact narration of Tool 6 output only. |
| `INVESTMENT` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | `INVESTMENT_NARRATION_CONTRACT.md` | Exact narration of Tool 7 evidence-backed output only. |
| `MARKET_INSIGHT` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | `MARKET_INSIGHT_NARRATION_CONTRACT.md` | Exact descriptive narration of Tool 8 historical observations only. |
| `PROPERTY_COMPARISON` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | `PROPERTY_COMPARISON_NARRATION_CONTRACT.md` | Neutral narration of Composer-owned comparison output only. |
| `GENERAL_QUESTION` | `DETERMINISTIC_ONLY` | None | No grounded domain-evidence contract exists. |
| Clarification-required result | `DETERMINISTIC_ONLY` | None | Existing deterministic clarification behavior remains authoritative. |
| Unsupported intent | `DETERMINISTIC_ONLY` | None | Generic LLM fallback is prohibited. |
| Multi-intent result | `DETERMINISTIC_ONLY` | None | No multi-intent narration contract is approved in Phase 5.5C.6D. |

## 4. Request-Level Admission Rules

Even an eligible intent becomes `REJECT_NARRATION` for the current request
when:

1. Authentication or tenant binding fails.
2. Workspace, optional scenario, optional broker session, response, memory,
   or citations do not bind.
3. Memory status is `FAILED` or `ACCESS_DENIED`.
4. Prompt budget or provider-safe projection requirements fail.
5. The evidence package is invalid or contains illegal citation references.
6. The runtime attempts a generic catch-all narration path.
7. Grounding rejects original candidate output.

## 5. Sparse and Insufficient Evidence Activation

Sparse or insufficient evidence does not automatically require provider
invocation. The intent contract decides whether limited narration is useful.

When narration proceeds:

1. Sparse evidence allows only bounded description plus an explicit sparse
   evidence disclosure.
2. Insufficient evidence allows only the approved limitation statement and
   available factual metadata.
3. Missing evidence may never be repaired with provider knowledge.
4. An intent may remain deterministic-only for that request if no useful
   grounded narration remains.

## 6. Partial Success Activation

For a single approved intent, partial success may activate narration only for
the successful deterministic slice. The unavailable slice must be disclosed
without speculation.

Multi-intent result narration remains deterministic-only because no combined
multi-intent contract exists.

## 7. Activation Preconditions Before Any Intent Is Enabled

An intent remains default-off until governance verifies:

1. Its contract is approved.
2. Its allowed narration fields are mapped only from the provider-safe
   projection.
3. Its prohibited claims are deterministically grounded.
4. Its citation references remain immutable and scoped.
5. Its sparse, insufficient, partial, and failure language is enforced.
6. Its deterministic fallback is defined.
7. Prompt Assembly architecture is separately approved.
8. The modern canonical runtime is the sole activatable LLM path.
9. Runtime evidence satisfies the Phase 5.5C.6B activation gate.

## 8. Formal Decisions

### A-01: Default-Off Per-Intent Activation

**Decision**

Every domain intent is default-off and individually governed.

**Reason**

Tools 1-8 and Property Comparison have distinct authorities and prohibited
claims.

**Alternatives considered**

1. Enable narration globally.
2. Use a generic response contract.
3. Activate all domain intents after one smoke test.

**Risks**

Operational configuration can create accidental broad activation.

**Mitigations**

Require explicit allowlisting and evidence for each intent.

**GO / NO-GO impact**

Global or implicit activation is `NO-GO`.

### A-02: General and Multi-Intent Narration Remain Deterministic-Only

**Decision**

`GENERAL_QUESTION`, clarification, unsupported, and multi-intent flows remain
deterministic-only in Phase 5.5C.6D.

**Reason**

No approved evidence contract grounds open-ended or combined narration.

**Alternatives considered**

1. Permit generic LLM assistance.
2. Compose multiple intent contracts automatically.
3. Let the provider choose the response mode.

**Risks**

The deterministic-only surface may be less conversational.

**Mitigations**

Preserve safe deterministic behavior and govern any future expansion
separately.

**GO / NO-GO impact**

Ungoverned generic or multi-intent narration is `NO-GO`.

## 9. Activation Verdict

```text
NARRATION_ACTIVATION_POLICY: CONDITIONAL_GO
DEFAULT_STATE: OFF
GENERIC_LLM_FALLBACK: FORBIDDEN
```

