# PX-1A Property Context Bridge

Date: 2026-06-09

## Mission

Create the minimum viable bridge between a successful direct valuation result and the backend Copilot property context.

## Scope

Implemented:

- Frontend property context types for backend workspace, property, and tool-event responses.
- `propertyContextService.ts` to ensure a backend workspace, bind or create a property context, and persist a direct valuation context event.
- `propertyContextStore.ts` to expose and persist:
  - `activeWorkspaceId`
  - `activePropertyId`
  - `activeScenarioId`
- Silent valuation-success binding from the existing valuation flow.

Not implemented:

- What-if UI
- Negotiation
- Investment
- Market Intelligence
- Copilot changes
- Dashboard changes
- Backend route, schema, model, or migration changes

## Runtime Flow

1. User completes `POST /v1/valuation/fair-price`.
2. The existing valuation UI stores the direct valuation result as before.
3. The bridge calls `GET /v1/copilot/workspaces`.
4. If `activeWorkspaceId` is already present and still returned by the backend, that workspace is reused.
5. If no active workspace is available, the first backend workspace is reused.
6. If no workspace exists, the bridge creates `ValorAI Active Valuations`.
7. The bridge lists workspace properties and binds to a matching intrinsic property profile.
8. If no matching property exists, it creates a backend property context using the valuation request.
9. The bridge records a `direct_valuation` tool event with the valuation request, valuation summary, request id, and property-context signature.
10. The persisted frontend store updates the active backend context ids.

## Backend Contracts Used

- `GET /v1/copilot/workspaces`
- `POST /v1/copilot/workspaces`
- `GET /v1/copilot/workspaces/{workspace_id}/properties`
- `POST /v1/copilot/properties`
- `POST /v1/copilot/tool-events`

## Binding Rules

- Workspace reuse prefers the current `activeWorkspaceId`.
- Property reuse compares intrinsic valuation inputs and excludes `target_price_egp`, because asking price is not part of the property identity.
- `activeScenarioId` is stored as `null`; scenario creation remains optional and is deliberately out of PX-1A scope.
- Direct valuation result persistence is represented as a scoped tool event, not a Copilot Tool 1 valuation snapshot. The direct valuation route remains authoritative for the current UI result.

## Files Created

- `frontend/src/types/propertyContext.ts`
- `frontend/src/services/propertyContextService.ts`
- `frontend/src/store/propertyContextStore.ts`
- `frontend/src/services/propertyContextService.test.ts`
- `frontend/src/store/propertyContextStore.test.ts`
- `property_context_bridge.md`

## Files Updated

- `frontend/src/features/valuation/ValuationScreen.tsx`
- `PROJECT_MASTER_STATE.md`
- Repository-level and docs-level `PROJECT_MASTER_STATE*` mirrors

## Known Limitations

- The bridge uses authenticated Copilot persistence endpoints. It does not implement React authentication or JWT acquisition.
- No visible UI indicates bridge status by design.
- Scenario binding is intentionally deferred; future intelligence tools can read `activeScenarioId` as nullable.
