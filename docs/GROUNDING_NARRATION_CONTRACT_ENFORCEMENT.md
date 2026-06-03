# ValorAI Grounding Narration Contract Enforcement

Review date: 2026-06-02  
Phase: 5.5C.6H Grounding Architecture Review  
Status: Architecture only  

## Principle

Grounding applies exactly one approved narration contract to the original
candidate. It validates candidate compliance without creating new authority.

## Contract Matrix

| Intent | Grounding must validate | Grounding must reject |
| --- | --- | --- |
| `VALUATION` | Exact authoritative valuation facts, exact upstream confidence output, routing or evidence-depth facts, limitations, and exact citations. | New price, new range, rounding, confidence logic, forecast, recommendation, or stronger certainty. |
| `EXPLAINABILITY` | Exact exposed explanations, drivers, contributions, evidence depth, limitations, and citations. | New driver, causal strengthening, hidden-model claim, reweighting, ranking, or unavailable internal reasoning. |
| `COMPARABLES` | Exact received comparable summary, Composer-owned count, average, minimum, maximum, exposed evidence, sparse limitations, and citations. | Synthetic comparable, placeholder evidence, new average, range, count, distance, selection, market-wide inference, or representative-coverage claim. |
| `FAIRNESS` | Exact Router-owned status, explanation, approved target-price context, limitations, and citations. | New threshold, reclassification, arithmetic, advice, compliance conclusion, or social or legal fairness inference. |
| `WHAT_IF` | Exact ephemeral scenario facts, Tool 5 or Composer-owned deltas, assumptions used, limitations, and citations. | Forecast, likelihood, persistence, new assumption, property mutation, new scenario value, or causal claim. |
| `NEGOTIATION` | Exact Tool 6 position, offer-band endpoints, talking points, risks, optional sensitivity evidence, limitations, and citations. | New offer, counteroffer, discount, concession, tactic, seller inference, deal probability, price step, or range. |
| `INVESTMENT` | Exact Tool 7 position, strengths, risks, reasons, summaries, optional sensitivity status, limitations, and citations. | Advice, suitability, ROI, IRR, CAGR, yield, appreciation, return, future price, scoring, ranking, rental-income assumption, or financing assumption. |
| `MARKET_INSIGHT` | Exact Tool 8 historical observations, exposed scope, historical window, limitations, and citations. | Forecast, prediction, future value, synthetic trend, momentum, direction, seasonality, market cycle, growth rate, or causal claim. |
| `PROPERTY_COMPARISON` | Exact Composer-owned reduced comparison fields, neutral property identification, property-bound citations, confidence labels, and limitations. | Winner, recommendation, ranking, confidence superiority, new delta, ratio, score, or reason not exposed upstream. |

## Enforcement Boundaries

Grounding must:

1. Require exactly one active approved contract version.
2. Validate only facts present in the internal grounding manifest.
3. Preserve sparse, insufficient, partial, and unavailable disclosures.
4. Reject stronger certainty than the upstream context supports.
5. Reject contract ambiguity.
6. Reject contract merge.

Grounding must never:

1. Select a different contract.
2. Merge contracts.
3. Add an allowed field.
4. Repair a missing field.
5. Convert an unsupported claim into a supported one.
6. Deliver a partial candidate.

## Deterministic-Only Flows

The following do not reach Grounding:

1. `GENERAL_QUESTION`
2. Clarification-required result
3. Unsupported intent
4. Generic catch-all narration
5. Multi-intent narration without a separately approved combined contract

## Forensic Finding

The observed legacy grounding schema cannot enforce all nine modern contracts.
Reusing it as the modern Grounding boundary is `NO_GO`.

