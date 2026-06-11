# ComposedResponse Examples

Phase: 5.5C.4B Response Composer  
Format: Structured excerpts from the V1 contract

## Property Comparison Success

```json
{
  "primary_intent": "PROPERTY_COMPARISON",
  "secondary_intents": [],
  "status": "SUCCESS",
  "evidence_summary": {
    "property_comparison": {
      "status": "AVAILABLE",
      "property_a": {
        "valuation_id": "val_a",
        "fair_price": 1000000,
        "confidence_level_label": "High"
      },
      "property_b": {
        "valuation_id": "val_b",
        "fair_price": 1250000,
        "confidence_level_label": "Medium"
      },
      "price_delta": 250000,
      "price_percentage_delta": 25.0,
      "confidence_level_label": {
        "property_a": "High",
        "property_b": "Medium"
      }
    }
  },
  "citation_package": {
    "valuation_ids": ["val_a", "val_b"],
    "tool_event_ids": [],
    "comparable_ids": [],
    "unavailable_optional_citation_types": ["tool_event_id", "comparable_id"]
  }
}
```

## Property Comparison Partial Failure

```json
{
  "primary_intent": "PROPERTY_COMPARISON",
  "status": "PARTIAL_SUCCESS",
  "evidence_summary": {
    "property_comparison": {
      "status": "UNAVAILABLE",
      "unavailable_reason_code": "PROPERTY_COMPARISON_REQUIRES_TWO_SUCCESSFUL_VALUATIONS",
      "available_slots": ["PROPERTY_A"],
      "failed_slots": ["PROPERTY_B"]
    },
    "failed_tools": [
      {
        "planned_tool": "VALUATION_TOOL:PROPERTY_B",
        "tool_name": "valuation",
        "error_type": "ToolResourceNotFound",
        "failure_category": "TOOL_FAILURE",
        "ordering_metadata": {
          "order_index": 1,
          "parallel_group_index": 0
        }
      }
    ]
  }
}
```

No comparison delta is emitted when one or both valuation slots fail.

## Comparable Compression And Arithmetic

```json
{
  "status": "SUCCESS",
  "compressed_context": {
    "evidence": {
      "tool_summaries": [
        {
          "planned_tool": "COMPARABLES_TOOL",
          "tool_name": "comparable",
          "status": "SUCCESS",
          "summary": {
            "comparables": {
              "statistics": {
                "comparable_count": 51,
                "average_price": 1240784.3137,
                "minimum_price": 1010000,
                "maximum_price": 1490000
              },
              "top_comparables": [
                {"comparable_id": "comp_tie_a", "distance_km": 0.5},
                {"comparable_id": "comp_tie_b", "distance_km": 0.5},
                {"comparable_id": "comp_001", "distance_km": 1.0}
              ]
            }
          }
        }
      ]
    },
    "compression_disclosures": [
      {
        "category": "COMPARABLES_TOOL.comparables",
        "received_count": 51,
        "eligible_count": 51,
        "shown_count": 3,
        "excluded_from_top_n_count": 0,
        "truncated": true,
        "ordering": ["distance_km ASC", "comparable_id ASC"]
      }
    ]
  },
  "frontend_payload": {
    "full_evidence": {
      "comparables": ["51 complete frontend-safe rows"]
    }
  }
}
```

## Sparse Evidence

```json
{
  "primary_intent": "MARKET_INSIGHT",
  "status": "SPARSE_EVIDENCE",
  "evidence_summary": {
    "sparse_evidence": [
      {
        "planned_tool": "MARKET_INSIGHT_TOOL",
        "tool_name": "market_insight",
        "reason_code": "MARKET_INSIGHT_VALUATION_VOLUME_ZERO"
      }
    ]
  }
}
```

## Multi-Intent Composition

```json
{
  "primary_intent": "PROPERTY_COMPARISON",
  "secondary_intents": ["NEGOTIATION"],
  "status": "SUCCESS",
  "compressed_context": {
    "intent": {
      "primary": "PROPERTY_COMPARISON",
      "secondary": ["NEGOTIATION"]
    }
  }
}
```
