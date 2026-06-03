# ValorAI What-if Narration Contract

Decision date: 2026-06-02  
Activation state: `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF`  

## Intent

`WHAT_IF`

## Purpose

Narrate Tool 5 ephemeral scenario output without treating a scenario as a
forecast or mutating the base property.

## Allowed Inputs

Only the validated provider-safe projection for this intent:

1. Composer-owned What-if summary.
2. Exact exposed base-state and sandbox-state facts.
3. Exact Tool 5 or Composer-owned `delta_value` and `delta_percentage` when
   exposed.
4. Exact upstream feature changes and `assumptions_used` disclosures when
   exposed.
5. Upstream comparable, fairness, sparse, insufficient, partial, or failure
   descriptors when exposed.
6. Approved bounded Memory summaries when relevant.
7. Exact immutable scoped citation tokens.

## Allowed Narration Fields

1. Neutral description of the ephemeral scenario overlay.
2. Exact restatement of approved current-state, sandbox-state, and delta
   output.
3. Exact disclosure of upstream assumptions used.
4. Evidence-depth and limitation disclosure.

## Allowed Evidence References

Composer-owned What-if context and Memory-owned bounded summaries only.

## Allowed Citation References

Exact received immutable citation IDs only:

```text
[citation:<exact-received-id>]
```

## Allowed Language Patterns

1. "In the evaluated sandbox scenario, `<exact-upstream-change>`."
2. "The upstream What-if result reports `<exact-upstream-delta>`."
3. "This is an ephemeral scenario evaluation, not a forecast."
4. "The upstream result disclosed `<exact-upstream-assumption>`."

## Forbidden Claims

1. A forecast, future price, prediction, or appreciation claim.
2. A claim that the scenario will occur.
3. A new scenario assumption or property mutation.
4. A new valuation, recommendation, offer, or strategy.

## Forbidden Calculations

1. New deltas or percentages.
2. New scenario values.
3. New comparable arithmetic.
4. New confidence calculations.

## Forbidden Inferences

1. Likelihood that the scenario will occur.
2. Missing scenario facts.
3. Causality beyond upstream output.
4. Persistence of the ephemeral overlay.

## Sparse Evidence Behavior

Narrate the evaluated scenario only with explicit sparse-evidence disclosure.
Do not treat the scenario as predictive.

## Insufficient Evidence Behavior

State that available evidence is insufficient for a substantive scenario
narration. Do not estimate missing values.

## Partial Success Behavior

Narrate successful scenario slices and identify unavailable slices without
speculation.

## Failure Behavior

Suppress LLM narration for denied, invalid, failed, or ungroundable context.

## Grounding Requirements

Grounding must verify:

1. Every scenario fact and assumption is upstream-owned.
2. Every numeric value exactly matches upstream output.
3. No forecast, likelihood, persistence, or new assumption appears.
4. Every citation token is exact and scoped.

## Fallback Requirements

Use authorized Composer-owned deterministic What-if delivery without model
text when narration is skipped or rejected.

## GO/NO-GO Conditions

`GO` only for narration of Tool 5 output after per-intent approval.
Forecasting or synthetic scenarios are `NO-GO`.

