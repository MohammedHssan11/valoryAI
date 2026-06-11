# PX-1 Contract Audit

Status: Complete
Date: 2026-06-09

## Backend Sources Audited

- `backend/app/api/schemas/copilot_tools.py`
- `backend/app/api/routes/copilot_tools.py`
- `backend/app/services/copilot_tools_service.py`
- `backend/app/tests/test_copilot_tools.py`
- `backend/app/tests/test_copilot_what_if_postgis_integration.py`

## Route

- Method: `POST`
- Path: `/v1/copilot/tools/what-if`
- Response model: `WhatIfToolResponse`
- Auth: inherited from `get_authenticated_user`

## Request Contract

`WhatIfToolRequest`

- `workspace_id: int` with `gt=0`
- `property_id: int` with `gt=0`
- `scenario_id: int | None` with `gt=0` when supplied
- `modifications: dict[str, Any]`

Validation:

- `modifications` must include at least one property change.
- Service-level normalization rejects unsupported fields in strict mode.
- `target_price_egp` is rejected for what-if because fairness owns target-price evaluation.
- `valuation_inputs` may be supplied as a nested object and is recursively normalized.
- Amenity changes may be supplied through `amenities`, `amenities_added`, `amenities_removed`, or supported boolean toggles.

Supported service aliases:

- `area` and `size` -> `size_sqm`
- `location` -> `address`
- `furnished` and `furnishing` -> `furnishing_status`
- `finishing` -> `building_quality`
- `parking` -> amenity `CP`
- `gym` -> amenity `SY`
- `clubhouse` -> amenity `CH`

## Response Contract

`WhatIfToolResponse`

- `tool_name: "what_if"`
- `base_valuation: int`
- `scenario_valuation: int`
- `base_valuation_id: str`
- `scenario_valuation_id: str`
- `fairness_valuation_id: str`
- `delta_value: int`
- `delta_percentage: float`
- `fairness_status: "Below Fair Value" | "Within Fair Value" | "Above Fair Value"`
- `confidence_level: str`
- `assumptions_used: list[str]`
- `feature_changes: FeatureChanges`
- `explainability: ExplainabilityToolResponse`
- `comparables: ComparableToolResponse`
- `timestamp: datetime`
- `source: "TruthLayer"`

Nested `FeatureChange`:

- `feature: str`
- `before: Any = None`
- `after: Any = None`
- `unit: str | None = None`

Nested comparables:

- `compound_name` and `similarity_reason` are nullable.
- `source` is always `TruthLayer`.

## Edge Cases

- Empty modifications fail with `422`.
- Unsupported strict modifications fail with `422`.
- Missing workspace, property, or scenario fails with `404`.
- Missing explainability/comparable payloads fail with `409`.
- If base valuation is zero, backend returns `delta_percentage = 0.0`.
- Existing scenario lineage is applied first; sandbox modifications are ephemeral and do not mutate the persisted scenario state.

## Frontend Constraint Noted

Tool 5 does not expose `base_price_range` or `scenario_price_range`. PX-1 UI shows the base range from the already-returned valuation result and marks the scenario range as unavailable rather than inventing a field.
