# ValorAI Valuation Narration Contract

Decision date: 2026-06-02  
Activation state: `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF`  

## Intent

`VALUATION`

## Purpose

Narrate an upstream Truth Layer valuation result without becoming a pricing
authority.

## Allowed Inputs

Only the validated provider-safe projection for this intent:

1. Composer-owned valuation summary.
2. Exact authoritative fair price when exposed by Composer.
3. Upstream confidence field or label when exposed.
4. Upstream routing, evidence-depth, sparse, insufficient, partial, or
   failure descriptors when exposed.
5. Approved bounded Memory summaries when relevant.
6. Exact immutable scoped citation tokens.

## Allowed Narration Fields

1. Exact authoritative fair-price restatement.
2. Neutral description of upstream confidence output.
3. Neutral description of upstream valuation status and limitations.
4. Neutral description of upstream routing or evidence depth when exposed.
5. Citation-backed factual summary.

## Allowed Evidence References

Composer-owned valuation context and Memory-owned bounded summaries only.

## Allowed Citation References

Exact received immutable citation IDs only, formatted as:

```text
[citation:<exact-received-id>]
```

## Allowed Language Patterns

1. "The authoritative valuation is `<exact-upstream-value>`."
2. "The upstream result reports `<exact-upstream-confidence>`."
3. "Comparable support is sparse, so the valuation should be read with that
   limitation."
4. "The valuation evidence is unavailable for this request."

## Forbidden Claims

1. A new price estimate or replacement fair price.
2. A future price, forecast, prediction, appreciation, or return claim.
3. A buying, selling, or negotiation recommendation.
4. A claim that the valuation is guaranteed, certain, or comprehensive unless
   upstream context says so.

## Forbidden Calculations

1. New price calculations.
2. New averages, ranges, deltas, percentages, conversions, or rounding.
3. New confidence calculations.
4. New comparable arithmetic.

## Forbidden Inferences

1. Unsupported causality.
2. Missing property facts.
3. Market direction.
4. Evidence representativeness beyond upstream disclosure.

## Sparse Evidence Behavior

Narrate the available valuation fact only with explicit sparse-evidence
disclosure. Do not strengthen certainty or fill comparable gaps.

## Insufficient Evidence Behavior

State that available evidence is insufficient for a substantive valuation
narration. Do not estimate a price.

## Partial Success Behavior

Narrate only successful upstream valuation fields. Identify unavailable
supporting fields without speculation.

## Failure Behavior

Suppress LLM narration for denied, invalid, failed, or ungroundable context.

## Grounding Requirements

Grounding must verify:

1. Every numeric value exactly matches an allowed upstream value.
2. No new pricing or confidence logic appears.
3. Every citation token is exact and scoped.
4. Limitations are preserved.

## Fallback Requirements

Use authorized Composer-owned deterministic valuation delivery without model
text when narration is skipped or rejected.

## GO/NO-GO Conditions

`GO` only for exact pass-through narration after per-intent approval.
Any new valuation authority is `NO-GO`.

