# ValorAI Narration Prohibited Claims Matrix

Decision date: 2026-06-02  
Phase: 5.5C.6D Narration Contract Architecture  
Status: Normative narration-governance matrix  

## 1. Interpretation Rule

`FORBIDDEN` means the LLM may never generate, calculate, infer, invent, or
repair the claim. Where stated, the LLM may narrate an exact upstream
deterministic value without modification. Exact pass-through is not
generation.

## 2. Mandatory Prohibited Claim Review

| Claim category | Decision | Exact upstream pass-through exception | Justification |
| --- | --- | --- | --- |
| Price estimates | `FORBIDDEN` | An exact Composer-owned authoritative fair price may be restated when the intent contract allows it. | The Truth Layer and Composer own valuation authority. |
| Future prices | `FORBIDDEN` | None. | No approved Tool generates future prices. |
| Forecasts | `FORBIDDEN` | None. | Narration is descriptive, not predictive. |
| Predictions | `FORBIDDEN` | None for new predictions. Historical persisted observations may be described only through approved Market Insight output. | The LLM is not a predictive model or interpretation layer. |
| ROI | `FORBIDDEN` | None. | Tool 7 explicitly excludes ROI generation. |
| IRR | `FORBIDDEN` | None. | Tool 7 explicitly excludes IRR generation. |
| CAGR | `FORBIDDEN` | None. | Tool 7 explicitly excludes CAGR generation. |
| Yield | `FORBIDDEN` | None, including rental-yield estimates. | Tool 7 explicitly excludes yield estimates. |
| Appreciation | `FORBIDDEN` | None for predicted or inferred appreciation. | Tool 7 and Tool 8 exclude appreciation forecasts. |
| Investment return | `FORBIDDEN` | None. | Tool 7 explicitly excludes return generation. |
| Negotiation offers | `FORBIDDEN` | Exact Tool 6 offer-band endpoints may be restated without modification. | Tool 6 alone owns grounded offer-band output. |
| Confidence calculations | `FORBIDDEN` | Exact upstream confidence fields or labels may be restated when allowed by the intent contract. | Composer and upstream Tools own confidence output. |
| Property rankings | `FORBIDDEN` | None. | Property Comparison V1 does not authorize ranking. |
| Property winner declarations | `FORBIDDEN` | None. | Property Comparison V1 is neutral comparison only. |
| New comparisons | `FORBIDDEN` | Exact Composer-owned comparison deltas may be restated without modification. | Composer alone owns approved comparison arithmetic. |
| Synthetic market trends | `FORBIDDEN` | None. Historical Tool 8 observations may be restated exactly. | Tool 8 is descriptive only and excludes synthetic trends. |
| Synthetic comparable evidence | `FORBIDDEN` | None. | Comparable evidence must remain received real evidence. |
| Synthetic assumptions | `FORBIDDEN` | Exact upstream `assumptions_used` disclosures may be restated. | Narration may disclose assumptions but never create them. |
| Synthetic citations | `FORBIDDEN` | None. Exact received immutable citation tokens may be referenced. | Citation identity remains Composer and Memory owned. |

## 3. Additional Prohibited Claims

| Claim category | Decision | Exact upstream pass-through exception | Justification |
| --- | --- | --- | --- |
| New negotiation strategies | `FORBIDDEN` | Exact Tool 6 talking points and risks may be narrated. | Tool 6 owns negotiation guidance. |
| Invented negotiation positions | `FORBIDDEN` | Exact Tool 6 position may be narrated. | Narration cannot classify or reclassify a negotiation. |
| Investment advice | `FORBIDDEN` | Exact Tool 7 evidence-backed position, strengths, and risks may be narrated as upstream output, not personal advice. | Tool 7 is evidence-backed analysis, not an LLM advice license. |
| New fairness thresholds | `FORBIDDEN` | Exact Router-owned fairness status and explanation may be narrated. | Router-owned fairness must remain authoritative. |
| Causal feature claims | `FORBIDDEN` | Exact upstream explainability statements may be narrated without strengthening causality. | Narration cannot infer causation from correlation or feature contribution. |
| Evidence representativeness | `FORBIDDEN` | Exact evidence-depth disclosure may be narrated. | Sparse evidence cannot be described as comprehensive. |
| Missing-data repair | `FORBIDDEN` | None. | Missing evidence must remain missing. |
| External real-estate knowledge | `FORBIDDEN` | None unless a future approved evidence source and contract explicitly authorize it. | The provider is not an external research authority. |

## 4. Property Comparison Mandatory Review

| Proposed narration behavior | Decision | Reason |
| --- | --- | --- |
| Declare a winner | `FORBIDDEN` | Composer does not own a winner declaration. |
| Recommend a property | `FORBIDDEN` | Recommendation authority is not approved for comparison narration. |
| Rank properties | `FORBIDDEN` | Composer emits reduced comparison fields, not ranking. |
| Calculate new deltas | `FORBIDDEN` | Composer alone computes approved deltas. |
| Calculate new percentages | `FORBIDDEN` | Composer alone computes approved percentage deltas. |
| Calculate confidence superiority | `FORBIDDEN` | Composer emits label-only confidence context, not superiority. |
| Narrate Composer output neutrally | `ALLOWED` | Exact pass-through narration preserves Composer authority. |

## 5. Negotiation Mandatory Review

| Proposed narration behavior | Decision | Reason |
| --- | --- | --- |
| Create a new offer | `FORBIDDEN` | Tool 6 alone owns grounded offer-band output. |
| Create a new negotiation strategy | `FORBIDDEN` | Narration may not invent guidance. |
| Invent or alter a negotiation position | `FORBIDDEN` | Tool 6 alone owns the position. |
| Narrate Tool 6 position | `ALLOWED` | Exact pass-through narration is allowed with evidence references. |
| Narrate Tool 6 offer band | `ALLOWED` | Exact endpoints only, without modification or new discount logic. |
| Narrate Tool 6 talking points and risks | `ALLOWED` | Exact upstream guidance only. |

## 6. Investment Mandatory Review

| Proposed narration behavior | Decision | Reason |
| --- | --- | --- |
| Create investment advice | `FORBIDDEN` | Narration is not an advice authority. |
| Generate ROI logic | `FORBIDDEN` | Tool 7 explicitly excludes ROI. |
| Generate return expectations | `FORBIDDEN` | Tool 7 explicitly excludes returns and forecasts. |
| Narrate Tool 7 position | `ALLOWED` | Exact upstream evidence-backed position only. |
| Narrate Tool 7 strengths and risks | `ALLOWED` | Exact upstream evidence-backed summaries only. |
| Disclose absent What-if evidence | `ALLOWED` | Insufficient evidence must remain explicit. |

## 7. Market Insight Mandatory Review

| Proposed narration behavior | Decision | Reason |
| --- | --- | --- |
| Describe approved historical observations | `ALLOWED` | Tool 8 owns persisted descriptive observations. |
| Describe approved historical evidence | `ALLOWED` | Exact pass-through description is allowed. |
| Forecast | `FORBIDDEN` | Tool 8 excludes forecasts. |
| Predict | `FORBIDDEN` | Tool 8 excludes future predictions. |
| Project future values | `FORBIDDEN` | No future-value authority exists. |
| Invent a trend from sparse history | `FORBIDDEN` | Sparse history must be disclosed, not extrapolated. |

## 8. Grounding Enforcement

Grounding must reject original candidate narration when it:

1. Contains a forbidden claim category.
2. Changes, rounds, converts, recombines, extrapolates, or compares numeric
   values beyond exact upstream pass-through.
3. Creates a citation, alias, assumption, comparable, strategy, position, or
   trend.
4. Describes sparse or insufficient evidence with stronger certainty.
5. Introduces external knowledge or provider-memory content.

## 9. Matrix Verdict

```text
PROHIBITED_CLAIMS_MATRIX: APPROVABLE
LLM_GENERATED_AUTHORITY_CLAIMS: FORBIDDEN
EXACT_UPSTREAM_PASS_THROUGH: CONDITIONALLY_ALLOWED
```

