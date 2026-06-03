# ValorAI Property Comparison Narration Contract

Decision date: 2026-06-02  
Activation state: `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF`  

## Intent

`PROPERTY_COMPARISON`

## Purpose

Narrate Composer-owned reduced Property Comparison V1 output neutrally,
without declaring a winner, recommending a property, ranking properties, or
calculating new comparisons.

## Allowed Inputs

Only the validated provider-safe projection for this intent:

1. Composer-owned reduced comparison summary.
2. Exact Composer-owned `price_delta` when exposed.
3. Exact Composer-owned `price_percentage_delta` when exposed.
4. Exact Composer-owned label-only `confidence_level_label` when exposed.
5. Upstream sparse, insufficient, partial, or failure descriptors.
6. Approved bounded Memory summaries when relevant.
7. Exact immutable scoped citation tokens for both compared properties.

## Allowed Narration Fields

1. Neutral identification of the compared properties.
2. Exact restatement of Composer-owned delta fields.
3. Exact restatement of Composer-owned confidence label.
4. Neutral description of upstream evidence limitations.

## Allowed Evidence References

Composer-owned comparison context and Memory-owned bounded summaries only.

## Allowed Citation References

Exact received immutable citation IDs only:

```text
[citation:<exact-received-id>]
```

Each property-specific statement must use the citations bound to that property.

## Allowed Language Patterns

1. "The Composer comparison reports `<exact-upstream-price-delta>`."
2. "The Composer percentage delta is `<exact-upstream-percentage-delta>`."
3. "The upstream confidence label is `<exact-upstream-label>`."
4. "This comparison describes Composer output and does not select a preferred
   property."

## Forbidden Claims

1. Winner declaration.
2. Property recommendation.
3. Property ranking.
4. Confidence superiority claim.
5. New investment, negotiation, valuation, or market recommendation.

## Forbidden Calculations

1. New deltas.
2. New percentages.
3. New price ratios, scores, rankings, or confidence comparisons.
4. New cross-property arithmetic of any kind.

## Forbidden Inferences

1. Which property is better.
2. Which property is a better investment.
3. Which property should be purchased, rented, negotiated, or prioritized.
4. Missing property facts.
5. Reasons for differences unless already exposed upstream.

## Sparse Evidence Behavior

Narrate only Composer-owned comparison output and disclose sparse evidence.
Do not select a winner.

## Insufficient Evidence Behavior

State that evidence is insufficient for a substantive comparison. Do not
rank, recommend, or calculate.

## Partial Success Behavior

If either required property valuation is unavailable, do not narrate a
substantive comparison. State that the comparison is incomplete and use the
deterministic fallback.

## Failure Behavior

Suppress LLM narration for denied, invalid, failed, incomplete, or
ungroundable comparison context.

## Grounding Requirements

Grounding must verify:

1. Every delta, percentage, and label exactly matches Composer output.
2. Property-specific citations remain correctly bound.
3. No winner, recommendation, ranking, superiority, or new comparison
   arithmetic appears.
4. Partial or sparse limitations remain explicit.

## Fallback Requirements

Use authorized Composer-owned deterministic comparison delivery without model
text when narration is skipped or rejected.

## GO/NO-GO Conditions

`GO` only for neutral Composer-output narration after per-intent approval.
Winner declarations, rankings, recommendations, and new comparisons are
`NO-GO`.

