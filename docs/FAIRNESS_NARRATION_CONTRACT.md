# ValorAI Fairness Narration Contract

Decision date: 2026-06-02  
Activation state: `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF`  

## Intent

`FAIRNESS`

## Purpose

Narrate Router-owned fairness output without creating thresholds, prices, or
advice.

## Allowed Inputs

Only the validated provider-safe projection for this intent:

1. Composer-owned fairness summary.
2. Exact Router-owned fairness status and explanation when exposed.
3. Exact target-price context when exposed and approved for narration.
4. Upstream sparse, insufficient, partial, or failure descriptors.
5. Approved bounded Memory summaries when relevant.
6. Exact immutable scoped citation tokens.

## Allowed Narration Fields

1. Exact fairness-status restatement.
2. Neutral narration of Router-owned fairness explanation.
3. Neutral target-price context when upstream-approved.
4. Evidence-depth and limitation disclosure.

## Allowed Evidence References

Composer-owned fairness context and Memory-owned bounded summaries only.

## Allowed Citation References

Exact received immutable citation IDs only:

```text
[citation:<exact-received-id>]
```

## Allowed Language Patterns

1. "The Router-owned fairness result is `<exact-upstream-status>`."
2. "The upstream explanation states `<exact-upstream-explanation>`."
3. "Available evidence is insufficient for a stronger fairness statement."

## Forbidden Claims

1. New fairness status.
2. New fairness threshold or classification rule.
3. New offer, valuation, recommendation, or negotiation strategy.
4. Social, legal, or protected-class fairness claims not present upstream.

## Forbidden Calculations

1. New price difference or percentage calculations.
2. New threshold calculations.
3. New confidence calculations.
4. Reclassification from upstream values.

## Forbidden Inferences

1. Why a fairness threshold exists unless upstream explains it.
2. Missing target-price context.
3. Legal compliance conclusions.
4. Market-wide fairness conclusions.

## Sparse Evidence Behavior

Narrate the upstream fairness output with explicit evidence limitation.

## Insufficient Evidence Behavior

State that evidence is insufficient for a substantive fairness narration. Do
not classify.

## Partial Success Behavior

Narrate only available Router-owned fields and identify unavailable fields.

## Failure Behavior

Suppress LLM narration for denied, invalid, failed, or ungroundable context.

## Grounding Requirements

Grounding must verify:

1. Status and explanation match upstream output.
2. No new threshold, arithmetic, advice, or compliance claim appears.
3. Every citation token is exact and scoped.

## Fallback Requirements

Use authorized Composer-owned deterministic fairness delivery without model
text when narration is skipped or rejected.

## GO/NO-GO Conditions

`GO` only for Router-owned fairness narration after per-intent approval.
Narrator-owned classification is `NO-GO`.

