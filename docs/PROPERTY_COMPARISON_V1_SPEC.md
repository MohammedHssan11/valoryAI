# Property Comparison V1 Specification

Phase: 5.5C.4A Response Composer Architecture Resolution  
Status: Architecture specification only

## Decision

Property Comparison V1 is implemented by the Response Composer over two
received Tool 1 payload envelopes:

```text
VALUATION_TOOL:PROPERTY_A
VALUATION_TOOL:PROPERTY_B
```

No Tool 9 is created.

Approved V1 comparison metrics:

```text
price_delta
price_percentage_delta
confidence_level_label
```

Not approved:

```text
sqm_delta
feature_delta
numeric_confidence_delta
winner
recommendation
```

## Input Requirements

The comparison is available only when both planned slots return successful
Tool 1 payloads containing:

```text
valuation_id
fair_price
confidence_level
```

The Composer must not retrieve property state, inspect invocation input,
query snapshots, or call Tool 1.

## Calculation Rules

Property B is compared relative to Property A.

```text
price_delta = property_b.fair_price - property_a.fair_price

price_percentage_delta =
  ((property_b.fair_price - property_a.fair_price)
    / property_a.fair_price) * 100
```

Rules:

```text
price_delta is an integer EGP amount
price_percentage_delta is rounded to 4 decimal places
positive values mean Property B is higher than Property A
negative values mean Property B is lower than Property A
zero means equal received fair prices
```

If `property_a.fair_price` is zero, `price_percentage_delta` is `null` and the
comparison carries:

```text
percentage_unavailable_reason_code =
  PROPERTY_A_FAIR_PRICE_ZERO
```

No substitute denominator is permitted.

## Confidence Labels

Confidence is label-only in V1:

```json
{
  "confidence_level_label": {
    "property_a": "High",
    "property_b": "Medium"
  }
}
```

The Composer preserves the two received labels. It must not:

```text
rank labels
convert labels into numbers
calculate a confidence delta
declare one valuation more trustworthy
```

## Output Shape

Available:

```json
{
  "status": "AVAILABLE",
  "property_a": {
    "valuation_id": "val_a",
    "fair_price": 1000000,
    "confidence_level_label": "High"
  },
  "property_b": {
    "valuation_id": "val_b",
    "fair_price": 1200000,
    "confidence_level_label": "Medium"
  },
  "price_delta": 200000,
  "price_percentage_delta": 20.0,
  "confidence_level_label": {
    "property_a": "High",
    "property_b": "Medium"
  }
}
```

Unavailable:

```json
{
  "status": "UNAVAILABLE",
  "unavailable_reason_code": "PROPERTY_COMPARISON_REQUIRES_TWO_SUCCESSFUL_VALUATIONS",
  "available_slots": ["PROPERTY_A"],
  "failed_slots": ["PROPERTY_B"]
}
```

## Partial Failure

If either valuation slot fails:

```text
do not calculate price_delta
do not calculate price_percentage_delta
preserve the successful slot summary
preserve normalized failure metadata
emit ComposedResponse status PARTIAL_SUCCESS when one slot succeeded
emit ComposedResponse status FAILED when neither slot succeeded
```

## Citation Rules

Each successful slot contributes its received `valuation_id` to the citation
package.

No snapshot lookup or Tool-event lookup is permitted.

## Reason

Tool 1 already exposes fair price and confidence label. Restricting V1 to
those fields makes comparison truthful without modifying the Tool Layer or
inventing inaccessible property facts.

## Alternatives Rejected

Rejected:

```text
extending Tool 1
adding property-state queries
passing Tool invocation inputs into the Composer
creating Tool 9
calculating size or feature deltas from unavailable facts
ranking confidence labels
letting a future narrator calculate differences
```

## Risks

| Risk | Impact |
| --- | --- |
| Comparison scope is narrow | Users do not receive size or feature comparisons in V1. |
| Zero denominator | Percentage delta cannot be calculated when Property A fair price is zero. |
| Partial Tool failure | No cross-property arithmetic is valid with only one successful valuation. |

## Mitigations

```text
return explicit unavailable reason codes
preserve successful slot evidence during partial failures
disclose the V1 metric boundary
keep all approved arithmetic inside the Composer
```

## Governance Impact

The Composer becomes the only authority allowed to calculate dual-property
price deltas. The future narrator receives precomputed fields only and must
not calculate, rank, recommend, or infer unavailable comparisons.

