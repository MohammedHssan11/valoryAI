# PX-1 Types Audit

Status: Complete
Date: 2026-06-09

## Created

- `frontend/src/types/whatIf.ts`

## Coverage

The frontend type file mirrors the backend Tool 5 contracts from `backend/app/api/schemas/copilot_tools.py`:

- `WhatIfToolRequest`
- `WhatIfToolResponse`
- `FeatureChange`
- `FeatureChanges`
- `ExplainabilityToolResponse`
- `ComparableToolItem`
- `ComparableToolResponse`
- `ValuationToolResponse`
- `ToolPriceRange`

## Contract Decisions

- `scenario_id` is nullable and optional on the frontend to match backend request semantics.
- `FeatureChange.before`, `FeatureChange.after`, and `FeatureChange.unit` preserve backend nullable behavior.
- `source` is constrained to `TruthLayer`.
- `fairness_status` is constrained to the backend literal values.
- Modifications are typed as supported backend request keys plus backend-documented service aliases.

## Non-Additions

- No scenario range fields were added because Tool 5 does not return them.
- No negotiation, investment, market, auth, deployment, or backend-only fields were added.
