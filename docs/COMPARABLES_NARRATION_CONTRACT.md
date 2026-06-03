# ValorAI Comparables Narration Contract

Decision date: 2026-06-02  
Activation state: `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF`  

## Intent

`COMPARABLES`

## Purpose

Narrate received real comparable evidence and Composer-owned comparable
summaries without creating synthetic evidence.

## Allowed Inputs

Only the validated provider-safe projection for this intent:

1. Composer-owned comparable summary.
2. Composer-owned approved comparable arithmetic when exposed: count,
   average, minimum, and maximum received prices.
3. Composer-selected bounded comparable context when exposed.
4. Upstream evidence-depth, sparse, insufficient, partial, or failure
   descriptors.
5. Approved bounded Memory summaries when relevant.
6. Exact immutable scoped citation tokens.

## Allowed Narration Fields

1. Exact restatement of received comparable count.
2. Exact restatement of Composer-owned average, minimum, and maximum values.
3. Neutral description of exposed comparable evidence.
4. Evidence-depth and limitation disclosure.

## Allowed Evidence References

Composer-owned comparable context and Memory-owned bounded summaries only.

## Allowed Citation References

Exact received immutable `valuation_id`, optional `tool_event_id`, and
optional `comparable_id` tokens only:

```text
[citation:<exact-received-id>]
```

## Allowed Language Patterns

1. "The received evidence includes `<exact-upstream-count>` comparables."
2. "The Composer summary reports `<exact-upstream-summary>`."
3. "Comparable support is sparse, so broader conclusions are not supported."

## Forbidden Claims

1. Synthetic comparable records.
2. Placeholder comparable prices, dates, locations, or attributes.
3. Claims that sparse comparables are representative of the market.
4. New valuation, offer, ranking, forecast, or trend claims.

## Forbidden Calculations

1. New comparable averages, ranges, counts, weights, or distances.
2. New price conversions or rounding.
3. New comparable ranking or selection.
4. New deltas or percentages.

## Forbidden Inferences

1. Missing comparable attributes.
2. Market-wide conclusions from limited evidence.
3. Hidden comparable selection logic.
4. Synthetic comparable replacements.

## Sparse Evidence Behavior

Narrate only available comparables and explicit evidence-depth limitations.
Never invent replacement evidence.

## Insufficient Evidence Behavior

State that comparable evidence is insufficient for a substantive comparable
summary. Do not fabricate comparables or arithmetic.

## Partial Success Behavior

Narrate available comparable evidence and identify unavailable portions.

## Failure Behavior

Suppress LLM narration for denied, invalid, failed, or ungroundable context.

## Grounding Requirements

Grounding must verify:

1. Every comparable reference exists in the scoped immutable package.
2. Every number exactly matches Composer-owned output.
3. No synthetic comparable, arithmetic, or market inference appears.
4. Sparse limitations remain explicit.

## Fallback Requirements

Use authorized Composer-owned deterministic comparable delivery without model
text when narration is skipped or rejected.

## GO/NO-GO Conditions

`GO` only for narration of received real evidence after per-intent approval.
Synthetic comparables are `NO-GO`.

