# ValorAI Market Insight Narration Contract

Decision date: 2026-06-02  
Activation state: `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF`  

## Intent

`MARKET_INSIGHT`

## Purpose

Narrate Tool 8 persisted descriptive observations and historical evidence
without forecasting, predicting, or creating synthetic trends.

## Allowed Inputs

Only the validated provider-safe projection for this intent:

1. Composer-owned market-insight summary.
2. Exact Tool 8 descriptive observations when exposed.
3. Exact Tool 8 historical-window, compound, area, property-type,
   fair-value, confidence, or comparable-density observations when exposed.
4. Upstream sparse, insufficient, partial, or failure descriptors.
5. Approved bounded Memory summaries when relevant.
6. Exact immutable scoped citation tokens.

## Allowed Narration Fields

1. Exact descriptive observation restatement.
2. Neutral historical-evidence description.
3. Neutral description of exposed scope and historical window.
4. Evidence-depth and limitation disclosure.

## Allowed Evidence References

Composer-owned Tool 8 context and Memory-owned bounded summaries only.

## Allowed Citation References

Exact received immutable citation IDs only:

```text
[citation:<exact-received-id>]
```

## Allowed Language Patterns

1. "The persisted historical evidence describes `<exact-upstream-observation>`."
2. "Within the exposed historical window, Tool 8 reports
   `<exact-upstream-observation>`."
3. "History is sparse, so no broader trend or projection is supported."

## Forbidden Claims

1. Forecast, prediction, future value, projected appreciation, or return.
2. Synthetic trend, momentum, direction, seasonality, or market-cycle claim.
3. New valuation, ranking, offer, or investment recommendation.
4. A claim that sparse history establishes a trend.

## Forbidden Calculations

1. New trend, growth-rate, appreciation, CAGR, yield, or forecast arithmetic.
2. New historical aggregation.
3. New confidence arithmetic.
4. New comparable arithmetic.

## Forbidden Inferences

1. Future market direction.
2. Missing historical observations.
3. Representativeness beyond upstream scope.
4. Causality for observed historical patterns.

## Sparse Evidence Behavior

Narrate only exposed historical observations and state that history is sparse.
Do not invent or project a trend.

## Insufficient Evidence Behavior

State that persisted history is insufficient for a substantive market
observation. Do not substitute external knowledge.

## Partial Success Behavior

Narrate available descriptive slices and identify unavailable slices without
speculation.

## Failure Behavior

Suppress LLM narration for denied, invalid, failed, or ungroundable context.

## Grounding Requirements

Grounding must verify:

1. Every observation appears in Tool 8 output.
2. Every scope and time-window statement matches upstream context.
3. No forecast, trend invention, aggregation, or causal claim appears.
4. Every citation token is exact and scoped.
5. Sparse or insufficient history remains explicit.

## Fallback Requirements

Use authorized Composer-owned deterministic market-insight delivery without
model text when narration is skipped or rejected.

## GO/NO-GO Conditions

`GO` only for descriptive Tool 8 narration after per-intent approval.
Forecasts, predictions, and synthetic trends are `NO-GO`.

