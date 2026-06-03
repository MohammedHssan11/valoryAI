# ValorAI Grounding Numeric Validation Policy

Review date: 2026-06-02  
Phase: 5.5C.6H Grounding Architecture Review  
Status: Architecture only  

## Principle

Grounding validates exact pass-through use of upstream numbers. Grounding does
not calculate.

## Numeric Authority

| Value category | Authority owner | Grounding role |
| --- | --- | --- |
| Authoritative valuation price | Truth Layer and Composer projection | Validate exact permitted restatement only. |
| Valuation range | Upstream Tool and Composer projection | Validate exact permitted restatement only when contract allows. |
| What-if delta and percentage | Tool 5 and Composer projection | Validate exact permitted restatement only. |
| Negotiation offer-band endpoints | Tool 6 and Composer projection | Validate exact permitted restatement only. |
| Negotiation price gap and percentage | Tool 6 and Composer projection | Validate exact permitted restatement only when exposed and allowed. |
| Investment evidence-backed values | Tool 7 and Composer projection | Validate exact permitted restatement only. |
| Comparable count, average, minimum, maximum | Composer | Validate exact permitted restatement only. |
| Property-comparison price delta and percentage delta | Composer | Validate exact permitted restatement only. |
| Confidence label | Upstream Tool and Composer projection | Validate exact label restatement only. |
| Numeric confidence calculation | None for narration | Reject. |

## Formal Decisions

| Question | Decision |
| --- | --- |
| May Grounding recompute valuation numbers? | `NO` |
| May Grounding recalculate deltas? | `NO` |
| May Grounding recalculate percentages? | `NO` |
| May Grounding recompute counts or averages? | `NO` |
| May Grounding independently verify arithmetic by calculation? | `NO` |
| May Grounding round or normalize a number? | `NO` |
| May Grounding convert currency or units? | `NO` |
| May Grounding repair a malformed number? | `NO` |
| May Grounding infer a missing value? | `NO` |
| May Grounding accept exact upstream pass-through values? | `YES`, when the selected contract permits the category |

## Validation Rules

Grounding must reject:

1. Any number not present in the approved grounding manifest for the selected
   contract.
2. Any rounded, converted, recombined, averaged, compared, or extrapolated
   number not explicitly present upstream.
3. Any new delta or percentage.
4. Any confidence score or confidence superiority claim not explicitly
   approved upstream.
5. Any new price estimate.
6. Any future price.
7. Any ROI, IRR, CAGR, yield, appreciation, or return value.
8. Any inferred count, range, rank, or score.

## Ambiguity Rule

When Grounding cannot deterministically prove exact upstream pass-through, it
must return `REJECT_NARRATION` with reason category `AMBIGUOUS_VALIDATION`.

## Forensic Finding

The observed grounding path does not enforce the full numeric policy and
mutates authoritative fields before validation. That behavior is `NO_GO`.

