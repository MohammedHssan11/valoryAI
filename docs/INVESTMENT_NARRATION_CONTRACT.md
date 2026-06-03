# ValorAI Investment Narration Contract

Decision date: 2026-06-02  
Activation state: `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF`  

## Intent

`INVESTMENT`

## Purpose

Narrate Tool 7 evidence-backed opportunity analysis without creating
investment advice, forecasts, returns, or independent pricing.

## Allowed Inputs

Only the validated provider-safe projection for this intent:

1. Composer-owned investment summary.
2. Exact Tool 7 investment position when exposed.
3. Exact Tool 7 strengths, risks, position reasons, evidence summaries,
   comparable summaries, and negotiation summaries when exposed.
4. Exact optional Tool 5 sensitivity evidence or `Insufficient Evidence`
   disclosure when exposed.
5. Upstream sparse, insufficient, partial, or failure descriptors.
6. Approved bounded Memory summaries when relevant.
7. Exact immutable scoped citation tokens.

## Allowed Narration Fields

1. Exact Tool 7 position restatement.
2. Exact upstream strengths, risks, reasons, and summaries.
3. Exact optional sensitivity-evidence narration.
4. Explicit absent-evidence disclosure.
5. Evidence-depth and limitation disclosure.

## Allowed Evidence References

Composer-owned investment context and Memory-owned bounded summaries only.

## Allowed Citation References

Exact received immutable citation IDs only:

```text
[citation:<exact-received-id>]
```

## Allowed Language Patterns

1. "Tool 7 reports the evidence-backed position `<exact-upstream-position>`."
2. "The upstream strengths include `<exact-upstream-strength>`."
3. "The upstream risks include `<exact-upstream-risk>`."
4. "Optional What-if evidence is insufficient, so no sensitivity conclusion
   is supported."

## Forbidden Claims

1. Personal or general investment advice.
2. ROI, IRR, CAGR, yield, appreciation, return, or future-price claims.
3. A forecast, prediction, or deal-outcome claim.
4. A new investment position, valuation, offer, strategy, or recommendation.
5. A claim that an upstream position guarantees suitability or performance.

## Forbidden Calculations

1. ROI, IRR, CAGR, yield, appreciation, or return calculations.
2. New prices, deltas, percentages, or ranges.
3. New comparable or confidence arithmetic.
4. New scoring or ranking logic.

## Forbidden Inferences

1. Investor suitability.
2. Expected return or resale outcome.
3. Rental income, occupancy, liquidity, or financing assumptions.
4. Missing sensitivity evidence.
5. Market direction.

## Sparse Evidence Behavior

Narrate Tool 7 output with explicit sparse-evidence disclosure. Do not
strengthen the position or invent missing sensitivity evidence.

## Insufficient Evidence Behavior

State that evidence is insufficient for the requested conclusion. Preserve
Tool 7 `Insufficient Evidence` behavior and do not create return logic.

## Partial Success Behavior

Narrate available Tool 7 slices and identify unavailable optional What-if or
supporting slices without speculation.

## Failure Behavior

Suppress LLM narration for denied, invalid, failed, or ungroundable context.

## Grounding Requirements

Grounding must verify:

1. Position, strengths, risks, reasons, and summaries exactly match Tool 7.
2. No advice, forecast, return, yield, appreciation, price, score, or ranking
   invention appears.
3. Missing optional What-if evidence remains explicit.
4. Every citation token is exact and scoped.

## Fallback Requirements

Use authorized Composer-owned deterministic investment delivery without model
text when narration is skipped or rejected.

## GO/NO-GO Conditions

`GO` only for exact Tool 7 narration after per-intent approval.
Investment advice or return generation is `NO-GO`.

