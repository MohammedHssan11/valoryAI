# ValorAI Grounding Prohibited Claims Enforcement

Review date: 2026-06-02  
Phase: 5.5C.6H Grounding Architecture Review  
Status: Architecture only  

## Principle

The prohibited-claims matrix is normative. Grounding rejects original
candidate narration that introduces any forbidden generated authority claim.

Grounding does not repair a prohibited claim. Grounding rejects the candidate.

## Prohibited Claims Matrix

| Claim category | Grounding decision | Exact upstream pass-through exception |
| --- | --- | --- |
| New price estimate | `REJECT_NARRATION` | Exact Composer-owned authoritative value may be restated when contract permits. |
| Future price | `REJECT_NARRATION` | None |
| Forecast | `REJECT_NARRATION` | None |
| Prediction | `REJECT_NARRATION` | Exact approved historical observation only; no new prediction. |
| ROI | `REJECT_NARRATION` | None |
| IRR | `REJECT_NARRATION` | None |
| CAGR | `REJECT_NARRATION` | None |
| Yield | `REJECT_NARRATION` | None |
| Appreciation | `REJECT_NARRATION` | None for predicted or inferred appreciation |
| Investment return | `REJECT_NARRATION` | None |
| New negotiation offer | `REJECT_NARRATION` | Exact Tool 6 endpoints only |
| New negotiation tactic or strategy | `REJECT_NARRATION` | Exact Tool 6 talking points and risks only |
| New confidence calculation | `REJECT_NARRATION` | Exact upstream label or field only when allowed |
| Property ranking | `REJECT_NARRATION` | None |
| Winner declaration | `REJECT_NARRATION` | None |
| Recommendation | `REJECT_NARRATION` | None unless a future approved contract grants authority |
| New comparison arithmetic | `REJECT_NARRATION` | Exact Composer-owned delta only |
| Synthetic market trend | `REJECT_NARRATION` | Exact Tool 8 historical observation only |
| Synthetic comparable | `REJECT_NARRATION` | None |
| Synthetic assumption | `REJECT_NARRATION` | Exact upstream `assumptions_used` disclosure only |
| Synthetic citation | `REJECT_NARRATION` | Exact received token only |
| New fairness threshold | `REJECT_NARRATION` | Exact Router-owned status and explanation only |
| Causal feature claim | `REJECT_NARRATION` | Exact upstream explanation without strengthened causality |
| Evidence representativeness | `REJECT_NARRATION` | Exact evidence-depth disclosure only |
| Missing-data repair | `REJECT_NARRATION` | None |
| External real-estate knowledge | `REJECT_NARRATION` | None under current architecture |

## Detection Architecture

Grounding must validate the original candidate against:

1. The selected intent contract.
2. The versioned prohibited-claims policy.
3. The exact upstream allowed-facts manifest.
4. The immutable citation package.
5. Required evidence-limitation disclosures.

This review approves no implementation mechanism. It approves only the
deterministic requirement:

> Any unsupported or ambiguous authority claim rejects the entire candidate.

## Hidden Calculation Rule

Grounding must reject a candidate when a factual, numeric, comparative, or
decision claim is not an exact permitted upstream pass-through claim.

Grounding must never derive whether a candidate calculation is mathematically
correct. Correct but newly calculated output is still forbidden.

## Forensic Finding

The observed legacy grounding validator checks only a limited valuation and
citation surface. It does not enforce the full prohibited-claims matrix.
That behavior is `NO_GO`.

