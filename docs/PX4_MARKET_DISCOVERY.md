# PX-4 Market Intelligence Backend Discovery

Status: Discovery only
Report date: 2026-06-10
Scope: Backend Market Intelligence capability, existing frontend placement context, and PX-4 readiness

No implementation was performed. No UI, service, store, route, schema, or backend code was created.

## Executive Finding

Market Intelligence already exists in the backend as Tool 8, named `market_insight`.

It is not a fresh market data fetcher, forecasting engine, demand model, supply model, liquidity model, yield model, or anomaly detector. It is a deterministic descriptive analytics tool over persisted tenant-scoped TruthLayer history.

The implemented backend answers:

- What valuation history exists in this workspace?
- What persisted fair-value range and median have been observed?
- What confidence levels dominate those saved valuations?
- How dense was comparable evidence across those valuations?
- Which compounds and areas appear most often in the persisted workspace history?
- Which filters were used, and which persisted records support each statement?

The implemented backend does not answer:

- Is real market demand increasing?
- Is real listing supply decreasing?
- Is the area appreciating?
- Is the market overheated?
- What will prices do in the future?
- What is the live liquidity index, yield variance, or capital inflow?

## Backend Surfaces

### Route

File: `backend/app/api/routes/copilot_tools.py`

Endpoint:

```text
POST /v1/copilot/tools/market-insight
```

Route behavior:

- Requires authenticated user through `get_authenticated_user`.
- Derives `user_id` from the JWT actor, not from the request body.
- Instantiates `CopilotToolsService`.
- Calls `service.execute_market_insight(user_id, data)`.
- Returns `MarketInsightToolResponse`.
- Maps `ToolResourceNotFound` to `404`.
- Maps `ValueError` to `422`.

### Schema

File: `backend/app/api/schemas/copilot_tools.py`

Request:

```text
workspace_id: int, required, gt=0
compound_name: string | null, min_length=1, max_length=255
h3_res9: string | null, min_length=1, max_length=32
property_type: string | null, min_length=1, max_length=120
time_window: string | null, pattern "all" or positive integer days such as "30d"
```

Only `workspace_id` is required. Optional filters can be supplied independently.

Response:

```text
tool_name: "market_insight"
market_summary: string
valuation_volume: int
confidence_distribution
fair_value_distribution
comparable_density
active_compounds
active_areas
evidence_summary
data_sources_used: string[]
timestamp: datetime
source: "TruthLayer"
```

Nested response fields:

- `confidence_distribution.valuation_count: int`
- `confidence_distribution.counts: Record<string, int>`
- `confidence_distribution.predominant_level: string | null`
- `fair_value_distribution.valuation_count: int`
- `fair_value_distribution.minimum_fair_value: float | null`
- `fair_value_distribution.median_fair_value: float | null`
- `fair_value_distribution.maximum_fair_value: float | null`
- `comparable_density.valuation_count: int`
- `comparable_density.minimum_comparable_count: int | null`
- `comparable_density.median_comparable_count: float | null`
- `comparable_density.maximum_comparable_count: int | null`
- `comparable_density.density_level: "High" | "Moderate" | "Sparse" | "Insufficient Evidence"`
- `comparable_density.measurement_sources: Record<string, int>`
- `active_compounds[]`: segment rows by compound
- `active_areas[]`: segment rows by property location
- `evidence_summary.valuation_ids: string[]`
- `evidence_summary.source_record_counts: Record<string, int>`
- `evidence_summary.filters_used: Record<string, unknown>`
- `evidence_summary.statements[]`: text plus evidence references
- `evidence_summary.traceability_note: string`

Nullable fields are intentional. They represent absent persisted observations, not computation failure.

## Data Sources

File: `backend/app/models/copilot.py`

Market Insight reads existing persisted data:

- `workspaces`
- `property_states`
- `scenario_states`, indirectly through `valuation_snapshots.scenario_state_id`
- `valuation_snapshots`
- `prediction_logs`
- `shadow_logs`
- `tool_events`

It does not invoke:

- Router pricing.
- CMT valuation.
- ML valuation.
- External APIs.
- Scrapers.
- LLMs.

### `valuation_snapshots`

Primary source. Queried by:

```text
user_id == authenticated user
workspace_id == request.workspace_id
created_at >= now - time_window, when time_window is not "all"
```

Important fields:

- `valuation_id`
- `user_id`
- `workspace_id`
- `property_state_id`
- `scenario_state_id`
- `router_request`
- `normalized_response`
- `explainability_payload`
- `created_at`

Used for:

- Tenant-scoped valuation population.
- Fair price via `normalized_response.fair_price`.
- Confidence level via `normalized_response.confidence_level`.
- Comparable evidence fallback via `explainability_payload.comparable_evidence`.
- Filter fallbacks via `router_request`.

### `property_states`

Loaded by owned snapshot property IDs within the same user and workspace.

Important fields:

- `id`
- `workspace_id`
- `user_id`
- `location`
- `property_type`
- `property_category`
- `valuation_inputs`

Used for:

- Area segment name through `property.location`.
- Property type fallback.
- Workspace-history source counts.

### `prediction_logs`

Loaded by `request_id in valuation_ids`.

Important fields:

- `request_id`
- `compound`
- `h3_res9`
- `property_type`
- `price`
- `engine`
- `routing_decision`
- `created_at`

Used for:

- Compound filter and segment source.
- H3 filter source.
- Property-type filter source.
- Evidence references.

Security note: prediction logs are joined by owned valuation IDs after the tenant-scoped snapshot query. The tool does not trust caller-supplied valuation IDs.

### `shadow_logs`

Loaded by `request_id in valuation_ids`.

Important fields:

- `request_id`
- `actual_response`
- `router_prediction`
- `ml_prediction`
- `cmt_prediction`
- `engine_used`
- `routing_reason`
- `comparable_count`
- `confidence_score`
- `compound_name`
- `h3_res9`
- `created_at`

Used for:

- Comparable count when present.
- Compound and H3 fallbacks.
- Evidence references.

### `tool_events`

Queried by authenticated user and workspace.

Relevant events are counted when:

```text
event.payload.response.valuation_id is in filtered valuation_ids
```

Market Insight also persists its own durable `tool_events` row after every run:

```text
tool_name = "market_insight"
property_id = null
scenario_id = null
payload.request.filters_used
payload.request.data_sources_used
payload.response
```

### Migrations and Indexes

File: `backend/app/db/migrations/008_market_insight_analytics_indexes.sql`

Indexes:

```text
ix_prediction_logs_market_filters on prediction_logs(compound, h3_res9, property_type, created_at)
ix_shadow_logs_market_filters on shadow_logs(compound_name, h3_res9, created_at)
```

These are read-path support indexes for descriptive analytics.

## Service Logic

File: `backend/app/services/copilot_tools_service.py`

Method:

```text
execute_market_insight(user_id, MarketInsightToolRequest) -> MarketInsightToolResponse
```

### Ownership and Filtering

Business rule:

1. Resolve the workspace through `_workspace(user_id, workspace_id)`.
2. Query valuation snapshots for that authenticated user and workspace.
3. Apply `time_window` to snapshot `created_at` only when it is not `all`.
4. Load related properties, predictions, and shadows using owned snapshots.
5. Build records.
6. Apply optional filters:
   - `compound_name` case-insensitive exact match.
   - `h3_res9` exact match.
   - `property_type` case-insensitive exact match.

The service stores `filters_used` with the supplied filters plus the normalized `time_window`, defaulting to `all`.

### Record Assembly

For each snapshot:

- `fair_price` comes from `snapshot.normalized_response.fair_price`.
- `confidence_level` comes from `snapshot.normalized_response.confidence_level`.
- `compound_name` falls back in this order:
  1. `prediction.compound`
  2. `shadow.compound_name`
  3. `router_request.compound_name`
- `h3_res9` falls back in this order:
  1. `prediction.h3_res9`
  2. `shadow.h3_res9`
  3. computed H3 res 9 from `router_request.lat` and `router_request.lng`
- `property_type` falls back in this order:
  1. `prediction.property_type`
  2. `router_request.property_type`
  3. `property_state.property_type`
- `area_name` is `property_state.location`.
- `comparable_count` comes from `shadow.comparable_count` when available, otherwise the length of `explainability_payload.comparable_evidence`.
- `comparable_count_source` is either `shadow_logs` or `comparable_evidence`.

Potential corruption edge:

- The code indexes `properties[snapshot.property_state_id]`.
- Under normal FK integrity this is safe.
- If persisted snapshots reference missing property rows, this would raise before response construction.

### Distributions

Confidence distribution:

- Counts `record.confidence_level`.
- Missing confidence becomes `Unknown`.
- Predominant level is the highest count, tie-broken alphabetically.
- Empty records return empty counts and `predominant_level = null`.

Fair-value distribution:

- Uses only non-null `fair_price`.
- Returns minimum, median, maximum.
- If no fair prices exist, all value fields are null and count is 0.

Comparable density:

- Uses only records with non-null comparable counts.
- Measurement sources count `shadow_logs` vs `comparable_evidence`.
- Density rules:

| Median persisted comparable count | Density |
| ---: | --- |
| no counts | `Insufficient Evidence` |
| `>= 5` | `High` |
| `>= 1` and `< 5` | `Moderate` |
| `0` | `Sparse` |

### Segments

Segments are produced for:

- `active_compounds` from `compound_name`.
- `active_areas` from `area_name`.

Segment rows require at least one non-null fair price. Segments with no fair-price values are skipped.

Segment fields:

- `name`
- `valuation_count`
- `median_fair_value`
- `confidence_distribution`
- `comparable_density`
- `median_comparable_count`

Segments are sorted by valuation count descending, then name ascending case-insensitively.

### Statements

When records exist, the service can generate these statements:

- Number of persisted TruthLayer valuations matching filters.
- Observed fair-value minimum, median, and maximum.
- Predominant confidence level.
- Comparable density and median comparable count.
- Most evaluated compound.
- Most evaluated area.

When no records exist:

- Statement: no persisted TruthLayer valuations match the selected filters.
- Evidence: `valuation_snapshots:workspace_id={workspace_id}`.

Every statement carries evidence references. References are capped at 20 records per source, then a filtered-count reference is added if needed.

### Source Counts

`source_record_counts` returns:

- `valuation_snapshots`
- `prediction_logs`
- `shadow_logs`
- `comparable_evidence`
- `tool_events`
- `workspace_history`
- `scenario_history`

`data_sources_used` always includes:

- `valuation_snapshots`
- `prediction_logs`
- `shadow_logs`
- `tool_events`
- `workspace_history`

It conditionally includes:

- `comparable_evidence`, when evidence rows exist.
- `scenario_history`, when filtered snapshots include scenario IDs.

### Traceability Boundary

The response embeds this governing concept:

```text
Descriptive analytics only. Every statement is derived from persisted tenant-scoped TruthLayer records; no forecast or future-price assertion is generated.
```

This boundary is central to PX-4. The UI must preserve it.

## Orchestrator Integrations

Market Insight is already wired into the governed Copilot backend.

### Intent Engine

Files:

- `backend/app/copilot/orchestrator/intents/contracts.py`
- `backend/app/copilot/orchestrator/intents/engine.py`

Intent:

```text
MARKET_INSIGHT
```

High-confidence phrases include:

- `market insight`
- `area trend`
- `compound trend`
- `market trend`
- `market activity`
- `market condition`
- `market conditions`
- `happening in`
- `mivida`

Medium-confidence keywords include:

- `market`
- `trend`
- `trends`
- `activity`
- `demand`
- `supply`
- `markit`

Risk: the intent vocabulary includes `demand` and `supply`, but Tool 8 cannot compute true demand or supply. Copilot narration must not turn those keywords into unsupported conclusions.

### Tool Planner

Files:

- `backend/app/copilot/orchestrator/planner/contracts.py`
- `backend/app/copilot/orchestrator/planner/planner.py`

Mapping:

```text
MARKET_INSIGHT -> MARKET_INSIGHT_TOOL
```

Single Market Insight intent is sequential. Multi-intent plans can run Market Insight in parallel with independent tools, such as Negotiation.

### Tool Executor

File: `backend/app/copilot/orchestrator/executor/executor.py`

Binding:

```text
MARKET_INSIGHT_TOOL -> tool_name "market_insight" -> MarketInsightToolRequest -> execute_market_insight
```

The executor:

- Requires explicit tool input payload.
- Validates through the Pydantic request model.
- Uses isolated database sessions per tool invocation.
- Supports timeout and partial-failure reporting.

### Response Composer

Files:

- `backend/app/copilot/orchestrator/composer/composer.py`
- `backend/app/copilot/orchestrator/composer/contracts.py`

Market Insight response normalization:

- Validates against `MarketInsightToolResponse`.
- Preserves aggregate distributions.
- Preserves valuation volume.
- Preserves comparable-density summary.
- Preserves up to 3 active compounds in compressed context.
- Preserves up to 3 active areas in compressed context.
- Preserves up to 3 evidence statements in compressed context.
- Keeps full frontend-safe payload in `frontend_payload`.

Sparse evidence rules:

- `valuation_volume == 0` -> sparse reason `MARKET_INSIGHT_VALUATION_VOLUME_ZERO`.
- `comparable_density.density_level in {"Sparse", "Insufficient Evidence"}` -> sparse reason `MARKET_INSIGHT_COMPARABLE_DENSITY_SPARSE`.

### Runtime

Files:

- `backend/app/copilot/orchestrator/runtime.py`
- `backend/app/api/routes/copilot_orchestrator.py`
- `backend/app/api/schemas/copilot_orchestrator.py`

Runtime sequence:

```text
Intent Engine -> Tool Planner -> Tool Executor -> Response Composer -> Memory Integration -> Narration
```

The orchestrator route accepts `tool_inputs.market_insight` as an alias and normalizes it to `MARKET_INSIGHT_TOOL`.

## Tests and Validation

### Dedicated Market Insight Integration Test

File: `backend/app/tests/test_copilot_market_insight_postgis_integration.py`

Coverage:

- Creates workspace and properties.
- Runs real Tool 1 valuations to create persisted history.
- Calls Market Insight overall.
- Calls compound filter.
- Calls H3 area filter.
- Calls property-type filter.
- Calls `30d` history filter.
- Confirms source is `TruthLayer`.
- Confirms valuation volume.
- Confirms fair-value, confidence, comparable density counts.
- Confirms active compound and active area segments.
- Confirms prediction and shadow log counts.
- Confirms required data sources are present.
- Confirms statements have evidence.
- Confirms no `forecast` or `future` language appears.
- Confirms durable `market_insight` tool events persist filters.
- Confirms cross-tenant request returns `404`.

### Persistence Hardening

File: `backend/app/tests/test_copilot_persistence_hardening.py`

Coverage:

- Forward-only migration ordering.
- `008_market_insight_analytics_indexes.sql` is last.
- Market Insight read-path indexes exist.

### Intent, Planner, Executor, Composer

Files:

- `backend/app/tests/test_intent_engine.py`
- `backend/app/tests/test_tool_planner.py`
- `backend/app/tests/test_tool_executor.py`
- `backend/app/tests/test_tool_executor_postgis_integration.py`
- `backend/app/tests/test_response_composer.py`
- `backend/app/tests/test_response_composer_postgis_integration.py`

Coverage:

- `What is happening in Mivida?` maps to `MARKET_INSIGHT`.
- Multi-intent `What is happening in Mivida and should I negotiate?` preserves Market Insight as primary and Negotiation as secondary.
- Planner maps `MARKET_INSIGHT` to `MARKET_INSIGHT_TOOL`.
- Planner can group Market Insight and Negotiation in a parallel plan.
- Executor binds and invokes the real `market_insight` tool.
- Executor timeout and tenant-isolation failures are structured.
- Composer preserves sparse evidence.
- Composer includes Market Insight as a secondary intent when combined with valuation.
- Composer marks empty Market Insight evidence as sparse.

### Docker Validation

Files:

- `scripts/validate_copilot_market_insight.ps1`
- `docs/MARKET_INSIGHT_DOCKER_VALIDATION_REPORT.md`
- `docs/PHASE_5_5B_7_MARKET_INSIGHT_IMPLEMENTATION_REPORT.md`

Validated against:

- Real Docker Compose stack.
- Real PostgreSQL and PostGIS.
- Real JWT ownership layer.
- Real Router, CMT, and ML infrastructure for upstream valuation history.
- Real prediction logs.
- Real shadow logs.
- Real valuation snapshots.
- Real comparable evidence.
- Real tool events.
- Backend restart recovery.
- PostgreSQL restart recovery.
- No forecasting fields.
- No future or synthetic summary language.

## Edge Cases

| Case | Current behavior |
| --- | --- |
| Missing or invalid `workspace_id` | Schema rejects non-positive values; unknown or cross-tenant workspace returns `404`. |
| Invalid `time_window` | Schema accepts only `all` or positive day strings like `30d`; invalid values fail validation. |
| `time_window = all` or omitted | Uses all persisted snapshots in the workspace. |
| Valid filter with no matching records | Returns `valuation_volume = 0`, empty segments, null fair values, density `Insufficient Evidence`, and traceable empty-evidence statement. |
| Missing confidence level | Counted as `Unknown`. |
| Missing fair price | Excluded from fair-value distribution and segment median. |
| No fair prices in a segment | Segment is skipped. |
| Missing shadow comparable count | Falls back to persisted comparable evidence length. |
| No comparable count observations | Density is `Insufficient Evidence`. |
| Comparable count median is 0 | Density is `Sparse`. |
| Missing H3 in logs | Attempts to compute H3 res 9 from router request latitude and longitude. |
| Missing lat/lng or invalid coordinates | H3 fallback returns null; H3 filter will not match that record. |
| Mixed-case compound or property type | Filter matching is case-insensitive. |
| Tool events without `payload.response.valuation_id` | Not counted as relevant tool events for filtered valuation IDs. |
| Corrupt snapshot references missing property rows | Could raise during record assembly; normal FK constraints should prevent this. |
| Large result sets | Evidence references are capped per source; segments are not capped by Tool 8 but composer compressed context caps display context to 3. |

## What Data Exists Today

Market Intelligence can expose:

- Workspace valuation volume.
- Filtered valuation volume.
- Persisted observed fair-value minimum.
- Persisted observed fair-value median.
- Persisted observed fair-value maximum.
- Confidence distribution.
- Predominant confidence level.
- Comparable count minimum, median, maximum.
- Comparable density label.
- Comparable measurement source counts.
- Active compound segments.
- Active area segments.
- Source record counts.
- Filters used.
- Evidence-backed statements.
- Valuation IDs.
- Data sources used.
- Traceability note.
- Timestamp.

## What Data Does Not Exist Today

The backend response does not include:

- Demand counts.
- Supply counts.
- Inventory changes.
- Listing velocity.
- Days on market.
- Transaction volume.
- Price appreciation.
- Price depreciation.
- Time-series deltas.
- Window-over-window comparison.
- Yield.
- Rental yield.
- Liquidity index.
- Capital inflow.
- Live anomalies.
- Heat index.
- Market overheating score.
- Undervaluation score by area.
- Investment recommendation.
- Forecasts.

Some of these could be future capabilities, but PX-4 should not imply them unless the backend contract changes first.

## UI-Relevant Contract Summary

PX-4 frontend should treat Tool 8 as a workspace Market Intelligence source with optional filters.

Recommended UI objects:

- Summary card from `market_summary`.
- Valuation volume card from `valuation_volume`.
- Fair-value distribution card from `fair_value_distribution`.
- Confidence distribution card from `confidence_distribution`.
- Comparable density card from `comparable_density`.
- Active compounds table from `active_compounds`.
- Active areas table from `active_areas`.
- Evidence statements list from `evidence_summary.statements`.
- Traceability and data sources disclosure from `evidence_summary` and `data_sources_used`.
- Sparse or empty state from `valuation_volume` and `comparable_density.density_level`.

Forbidden UI claims unless future backend contracts add support:

- "Demand is increasing."
- "Supply is decreasing."
- "This market is overheated."
- "This area is undervalued."
- "Prices will rise."
- "Buy signal."
- "Liquidity index."
- "Yield variance."
- "Capital inflow."
- "Live anomaly."

## Discovery Conclusion

The Market Intelligence backend is complete enough for a frontend integration that is honest about persisted, descriptive, evidence-backed workspace analytics.

PX-4 should not implement a market forecasting product. It should expose Tool 8 as a trustable Market Intelligence Pulse over saved valuation history, with clear sparse-state handling and traceability.
