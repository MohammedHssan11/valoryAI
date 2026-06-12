# Next Implementation Plan: What-if Scenario Analysis

Date: 2026-06-09

## Selected Feature

What-if Scenario Analysis.

This plan is intentionally limited to the highest ROI feature. It does not include Negotiation Intelligence, Investment Intelligence, Market Intelligence, broader Copilot UI, auth, security, deployment, infrastructure, or backend rewrites.

## Goal

Expose the existing backend What-if Tool through the React frontend so a user can run a scenario from the current valuation/property context and see:

- Base valuation
- Scenario valuation
- EGP delta
- Percentage delta
- Feature changes
- Assumptions used
- Scenario explainability
- Scenario comparable evidence

## Backend Endpoints

Primary endpoint:

- `POST /v1/copilot/tools/what-if`

Required request shape:

```json
{
  "workspace_id": 1,
  "property_id": 10,
  "scenario_id": null,
  "modifications": {
    "bathrooms": 3,
    "amenities": ["AC", "CP", "GYM"],
    "furnishing_status": "furnished"
  }
}
```

Primary response fields:

- `base_valuation`
- `scenario_valuation`
- `base_valuation_id`
- `scenario_valuation_id`
- `fairness_valuation_id`
- `delta_value`
- `delta_percentage`
- `fairness_status`
- `confidence_level`
- `assumptions_used`
- `feature_changes`
- `explainability`
- `comparables`
- `timestamp`

Supporting product-context endpoints:

- `GET /v1/copilot/workspaces`
- `POST /v1/copilot/workspaces`
- `POST /v1/copilot/properties`
- `GET /v1/copilot/workspaces/{workspace_id}/properties`
- `POST /v1/copilot/scenarios` only if the implementation chooses to persist named scenarios in this phase.

Out of scope:

- Auth transport work
- Security policy work
- Deployment work
- Backend endpoint changes

## Data Flow

```text
User runs direct valuation
  -> frontend already has valuation draft and direct valuation result
  -> frontend ensures an active workspace/property context exists
  -> user opens What-if panel
  -> user edits scenario modifications
  -> frontend submits POST /v1/copilot/tools/what-if
  -> backend runs base valuation + scenario valuation + explanation + comparables + fairness
  -> frontend renders delta, assumptions, feature changes, scenario evidence
```

## UI Placement

Primary placement:

- Add the What-if Scenario Analysis panel below the current valuation result on `ValuationScreen`.

Secondary route behavior:

- `AssetsScreen` currently aliases `ValuationScreen`, so the first implementation can appear there automatically.

Do not create a new app shell, landing page, or separate architecture.

## New Frontend Service

Create a frontend service dedicated to business tools, for example:

- `frontend/src/services/intelligenceToolsService.ts`

Suggested function:

```ts
requestWhatIfScenario(request: WhatIfToolRequest, signal?: AbortSignal): Promise<WhatIfToolResult>
```

This service should call:

- `/v1/copilot/tools/what-if`

Add strict response validation similar to `valuationService.ts` and `brokerService.ts`.

## New Frontend Types

Create or extend types for:

- `WhatIfToolRequest`
- `FeatureChange`
- `FeatureChanges`
- `WhatIfToolResponse`
- `ComparableToolResponse`
- `ExplainabilityToolResponse`

Recommended file:

- `frontend/src/types/intelligenceTools.ts`

The initial type surface should mirror `backend/app/api/schemas/copilot_tools.py` rather than inventing a new frontend contract.

## State Management

Use a small Zustand store, for example:

- `frontend/src/store/scenarioAnalysisStore.ts`

State:

- `activeWorkspaceId`
- `activePropertyId`
- `activeScenarioId`
- `modificationsDraft`
- `lastWhatIfResult`
- `lastWhatIfRequest`
- `isDirty`
- `selectedScenarioComparableId`

Actions:

- `setActivePropertyContext`
- `updateModification`
- `resetModifications`
- `setWhatIfResult`
- `clearWhatIfResult`

Do not replace `valuationStore`. The scenario store should sit beside it.

## Property Context Bridge

Tool 5 requires `workspace_id` and `property_id`. The React frontend currently has only a local valuation draft.

Minimal bridge:

1. After a successful direct valuation, map the current `RentFairPriceRequest` draft into a `PropertyStateCreate` payload.
2. Use an existing workspace if one is already known.
3. If no workspace is known, create or select a single default product workspace.
4. Store returned `workspace_id` and `property_id` in the scenario analysis store.
5. Do not build full workspace management in this phase.

This bridge is a product-context requirement, not a security or auth feature.

## UI Components

Add the smallest complete component set:

| Component | Purpose |
| --- | --- |
| `WhatIfScenarioPanel` | Parent panel; owns submit/cancel/reset UX. |
| `ScenarioModificationControls` | Controls for size, bedrooms, bathrooms, furnishing, quality, view, and amenities. |
| `ScenarioDeltaSummary` | Shows base valuation, scenario valuation, delta EGP, delta percent, confidence, and fairness status. |
| `FeatureChangesList` | Renders added/removed/modified feature changes from backend response. |
| `ScenarioAssumptions` | Renders `assumptions_used` with an honest empty state. |
| `ScenarioEvidenceTabs` | Tabs for Scenario Summary, Comparables, Explainability. |

Reuse existing:

- `ComparablePanel` where practical
- `ExplainabilityPanel` patterns where practical
- Existing valuation formatting helpers and visual system

## User Journey

1. User opens Valuation.
2. User enters property details and target/asking price.
3. User runs valuation.
4. Result appears with fair price, confidence, comparables, and explainability.
5. User opens "Scenario" or "What-if" panel.
6. User changes one or more property attributes.
7. User runs scenario.
8. UI shows base vs scenario valuation and delta.
9. User reviews feature changes, assumptions, scenario comparables, and scenario explanation.
10. User can reset scenario modifications and try another variation.

## Acceptance Criteria

Functional:

- A user can run a What-if scenario from a completed valuation.
- The frontend sends `workspace_id`, `property_id`, optional `scenario_id`, and non-empty `modifications`.
- Empty modifications are blocked client-side before calling the API.
- The UI renders base valuation, scenario valuation, delta value, delta percentage, confidence, and fairness status.
- The UI renders added, removed, and modified feature changes.
- The UI renders assumptions when the backend returns them.
- Scenario comparables are visible when returned.
- Scenario explainability is visible when returned.
- Sparse or empty comparables render an honest empty state.
- API failures render a visible error with request context.
- User can reset the scenario draft without clearing the original valuation result.

Business:

- The feature clearly communicates that scenario valuation is based on backend TruthLayer evidence.
- The UI does not imply ROI, yield, forecast, or guaranteed return.
- The UI does not allow the scenario result to overwrite the original valuation without explicit user action.
- Scenario output can later feed Negotiation and Investment Intelligence.

Technical:

- No backend endpoint changes.
- No frontend architecture rewrite.
- No authentication/security/deployment work.
- Types mirror backend response contracts.
- Tests cover service validation, store behavior, empty modifications, successful render, sparse evidence render, and error render.

## Out Of Scope

- Negotiation Intelligence
- Investment Intelligence
- Market Intelligence
- Full workspace management
- Full scenario library
- Persisted named scenario UX
- Decision history/Vault integration
- Copilot/orchestrator chat integration
- Export/report generation

## Implementation Sequence

1. Add `intelligenceTools` types for What-if response contracts.
2. Add `requestWhatIfScenario` service.
3. Add `scenarioAnalysisStore`.
4. Add minimal property context bridge from valuation draft to backend property context.
5. Add `WhatIfScenarioPanel` below valuation result.
6. Add modification controls.
7. Add delta summary and feature changes rendering.
8. Add assumptions, comparables, and explainability sections.
9. Add tests.
10. Run frontend typecheck, tests, and a browser smoke of `/valuation`.

## Recommended Next Phase

PX-1 should implement What-if Scenario Analysis only. After PX-1 is complete, PX-2 should use the same active property context to expose Negotiation Intelligence.

