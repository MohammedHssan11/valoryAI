# Response Composer Compression Policy

Phase: 5.5C.4A Response Composer Architecture Resolution  
Status: Architecture specification only

## Decision

The Composer emits two structured channels:

```text
compressed_context
frontend_payload
```

`compressed_context` is bounded structured context for a future narration
phase. `frontend_payload` preserves complete frontend-safe normalized evidence.

Neither channel is a prompt, narrative, SSE event, WebSocket message, or
streaming wrapper.

## Dual-Channel Rules

| Channel | Purpose | Evidence depth |
| --- | --- | --- |
| `compressed_context` | Future narration-safe structured context | Top-N and deterministic aggregates |
| `frontend_payload` | Future UI evidence surface | Complete frontend-safe normalized evidence |

Truncation in `compressed_context` must never truncate the corresponding
frontend-safe evidence in `frontend_payload`.

## Comparable Compression

### Governed Comparator

Eligible comparable rows are sorted by:

```text
1. distance_km ASC
2. comparable_id ASC
```

Then:

```text
Top-N limit = 3
```

Rows without a usable numeric `distance_km` or canonical comparable identifier:

```text
remain in frontend_payload
are excluded from compressed Top-N selection
are counted in compression disclosures
```

### Comparable Summary

The Composer calculates statistics over every received comparable row with a
usable numeric price, not only the Top 3:

```json
{
  "comparable_count": 49,
  "average_price": 1200000.0,
  "minimum_price": 1000000,
  "maximum_price": 1400000,
  "comparables_truncated": true,
  "shown_in_compressed_context": 3
}
```

Rules:

```text
average_price is arithmetic mean
average_price is rounded to 4 decimal places
zero usable prices produce null average, minimum, and maximum
```

The future narrator must never be asked to calculate these values.

## Feature-Driver Compression

Explainability feature drivers currently expose categorical direction and
strength, not a governed numeric contribution score.

V1 therefore uses:

```text
Top 3 Positive drivers in received source order
Top 3 Negative drivers in received source order
```

The Composer must not invent numeric ranking, rescore categorical strength, or
reorder ties using an unapproved heuristic.

All received frontend-safe feature drivers remain available in
`frontend_payload`.

## Market Insight Compression

Market Insight Tool output is already descriptive and aggregated.

For `compressed_context`:

```text
preserve received aggregate distributions
preserve received valuation volume
preserve received comparable-density summary
preserve at most 3 active compounds in Tool-owned source order
preserve at most 3 active areas in Tool-owned source order
preserve at most 3 evidence statements in Tool-owned source order
do not create forecasts
do not generate synthetic trends
```

All frontend-safe Tool-owned segments and statements remain available in
`frontend_payload`.

## Structural Safety

`compressed_context` must use strict known-schema normalizers for Tools 1-8.
Unknown fields are not copied into compressed context.

Both channels must exclude:

```text
raw geospatial geometries
raw coordinate traces not approved as frontend evidence
PII
database session data
internal debug payloads
shadow-log tracing payloads
HTTP metadata
stack traces
arbitrary exception messages
```

Approved citation IDs remain available through `citation_package`.

## Compression Disclosures

Each truncated evidence category records:

```json
{
  "category": "comparables",
  "received_count": 49,
  "eligible_count": 49,
  "shown_count": 3,
  "excluded_from_top_n_count": 0,
  "truncated": true,
  "ordering": [
    "distance_km ASC",
    "comparable_id ASC"
  ]
}
```

This disclosure is structured data only.

## Arithmetic Offload

The Composer is the mathematical authority for:

```text
comparable count
comparable average price
comparable minimum price
comparable maximum price
Property Comparison V1 price_delta
Property Comparison V1 price_percentage_delta
```

Received Tool-owned arithmetic remains preserved as received:

```text
What-if delta_value and delta_percentage
Negotiation price_gap and price_gap_percentage
Investment price_gap and price_gap_percentage
Market Insight distributions
```

The Composer must not recalculate or replace Tool-owned business arithmetic.

## Reason

The dual-channel policy keeps future narration context bounded while
preserving complete safe evidence for future frontend use. It prevents hidden
arithmetic work from leaking into later generative phases.

## Alternatives Rejected

Rejected:

```text
passing raw unbounded arrays to a future narrator
truncating frontend evidence to Top 3
sorting by an unavailable relevance score
sorting feature drivers with invented numeric weights
generating market forecasts
copying unknown payload fields into compressed context
wrapping frontend_payload in streaming transport
```

## Risks

| Risk | Impact |
| --- | --- |
| Top-N context omits lower-ranked evidence | Future narration cannot reference omitted comparable detail. |
| Frontend payload remains larger than compressed context | Transport design must be handled later without weakening evidence preservation. |
| Payload schemas may evolve | Strict normalizers must fail closed on missing required fields. |

## Mitigations

```text
preserve full frontend-safe evidence
emit truncation disclosures
use one approved comparable comparator
retain Tool-owned aggregates without recomputation
exclude unknown fields from compressed context
defer transport integration
```

## Governance Impact

The Composer becomes the only approved compression and arithmetic-offload
boundary before future narration. Compression may reduce context size, but it
must never fabricate, forecast, or silently discard frontend-safe evidence.

