# ValorAI Negotiation Narration Contract

Decision date: 2026-06-02  
Activation state: `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF`  

## Intent

`NEGOTIATION`

## Purpose

Narrate Tool 6 negotiation output without creating offers, strategies,
positions, or hidden pricing logic.

## Allowed Inputs

Only the validated provider-safe projection for this intent:

1. Composer-owned negotiation summary.
2. Exact Tool 6 negotiation position when exposed.
3. Exact Tool 6 recommended offer-band endpoints when exposed.
4. Exact Tool 6 talking points and risk notes when exposed.
5. Exact optional Tool 5 sensitivity evidence when exposed.
6. Upstream comparable, fairness, sparse, insufficient, partial, or failure
   descriptors when exposed.
7. Approved bounded Memory summaries when relevant.
8. Exact immutable scoped citation tokens.

## Allowed Narration Fields

1. Exact Tool 6 position restatement.
2. Exact Tool 6 offer-band endpoint restatement.
3. Exact Tool 6 talking-point and risk-note narration.
4. Exact optional upstream sensitivity evidence narration.
5. Evidence-depth and limitation disclosure.

## Allowed Evidence References

Composer-owned negotiation context and Memory-owned bounded summaries only.

## Allowed Citation References

Exact received immutable citation IDs only:

```text
[citation:<exact-received-id>]
```

## Allowed Language Patterns

1. "Tool 6 reports the negotiation position `<exact-upstream-position>`."
2. "The upstream offer band is `<exact-upstream-band>`."
3. "The upstream talking points include `<exact-upstream-talking-point>`."
4. "Comparable support is sparse, so the negotiation evidence is limited."

## Forbidden Claims

1. A new offer, counteroffer, discount, concession, or offer-band endpoint.
2. A new negotiation strategy or tactic.
3. An invented or altered negotiation position.
4. A prediction about seller behavior or deal outcome.
5. A new valuation, ranking, investment recommendation, or market forecast.

## Forbidden Calculations

1. New discounts, percentages, price steps, or ranges.
2. New offer-band calculations.
3. New comparable arithmetic.
4. New confidence calculations.

## Forbidden Inferences

1. Seller motivation or willingness.
2. Deal probability.
3. Missing comparable support.
4. Unstated urgency, leverage, or market direction.

## Sparse Evidence Behavior

Narrate Tool 6 output only with explicit sparse-evidence disclosure. Do not
invent replacement comparables or new offer values.

## Insufficient Evidence Behavior

State that available evidence is insufficient for additional negotiation
guidance. Do not create a fallback strategy or offer.

## Partial Success Behavior

Narrate available Tool 6 slices and identify unavailable optional sensitivity
or evidence slices without speculation.

## Failure Behavior

Suppress LLM narration for denied, invalid, failed, or ungroundable context.

## Grounding Requirements

Grounding must verify:

1. Position, band endpoints, talking points, and risks exactly match Tool 6
   output.
2. Every price and percentage is exact upstream pass-through.
3. No new offer, tactic, seller inference, or outcome prediction appears.
4. Every citation token is exact and scoped.
5. Sparse or insufficient evidence remains explicit.

## Fallback Requirements

Use authorized Composer-owned deterministic negotiation delivery without
model text when narration is skipped or rejected.

## GO/NO-GO Conditions

`GO` only for exact Tool 6 narration after per-intent approval.
Narrator-created offers, strategies, or positions are `NO-GO`.

