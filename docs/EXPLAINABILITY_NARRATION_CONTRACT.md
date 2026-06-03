# ValorAI Explainability Narration Contract

Decision date: 2026-06-02  
Activation state: `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF`  

## Intent

`EXPLAINABILITY`

## Purpose

Narrate upstream explainability output without inventing drivers, causality,
or confidence logic.

## Allowed Inputs

Only the validated provider-safe projection for this intent:

1. Composer-owned explainability summary.
2. Upstream Router explanation, fairness explanation, narrative explanation,
   evidence summary, and feature-driver descriptions when exposed.
3. Upstream positive or negative feature contributions when exposed.
4. Upstream sparse, insufficient, partial, or failure descriptors.
5. Approved bounded Memory summaries when relevant.
6. Exact immutable scoped citation tokens.

## Allowed Narration Fields

1. Neutral restatement of upstream explanations.
2. Neutral summary of exposed feature drivers or contributions.
3. Evidence-depth and limitation disclosure.
4. Citation-backed explanation summary.

## Allowed Evidence References

Composer-owned explainability context and Memory-owned bounded summaries only.

## Allowed Citation References

Exact received immutable citation IDs only:

```text
[citation:<exact-received-id>]
```

## Allowed Language Patterns

1. "The upstream explanation identifies `<exact-upstream-driver>`."
2. "The provided evidence describes `<exact-upstream-explanation>`."
3. "The available explanation is limited because `<upstream-limitation>`."

## Forbidden Claims

1. New feature drivers.
2. New causal claims.
3. New confidence interpretations.
4. Hidden model behavior, undisclosed thresholds, or undisclosed reasoning.
5. Price recommendations, forecasts, or rankings.

## Forbidden Calculations

1. New feature contribution arithmetic.
2. New confidence arithmetic.
3. Reweighting, ordering, or ranking drivers unless already upstream-owned.
4. Any new comparison calculation.

## Forbidden Inferences

1. Treating a contribution as proof of causation.
2. Inferring missing property facts.
3. Explaining unavailable model internals.
4. Generalizing beyond exposed evidence.

## Sparse Evidence Behavior

Narrate only exposed explanation fields and disclose that explanation depth is
limited.

## Insufficient Evidence Behavior

State that the available evidence does not support a substantive explanation.
Do not invent drivers.

## Partial Success Behavior

Narrate available explanation slices and name unavailable slices without
speculation.

## Failure Behavior

Suppress LLM narration for denied, invalid, failed, or ungroundable context.

## Grounding Requirements

Grounding must verify:

1. Every narrated driver or explanation is present upstream.
2. No causal strengthening appears.
3. No new arithmetic or hidden-model claim appears.
4. Every citation token is exact and scoped.

## Fallback Requirements

Use authorized Composer-owned deterministic explainability delivery without
model text when narration is skipped or rejected.

## GO/NO-GO Conditions

`GO` only for upstream explanation narration after per-intent approval.
Invented drivers or causality are `NO-GO`.

