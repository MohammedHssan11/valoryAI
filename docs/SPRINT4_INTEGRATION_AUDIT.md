# Sprint 4 Integration Audit

Date: 2026-06-11

## Validated Flow

Sprint 4 target flow:

1. Login
2. Direct Valuation
3. Snapshot Creation
4. Property Context
5. ToolEvent
6. Market Intelligence
7. Copilot Explainability

## Login and Auth Configuration

Validated:

- Docker Compose passes Firebase Web SDK values into the frontend build.
- Dockerfile exposes those values during `npm run build`.
- Docker-built static bundle contains configured Firebase values.
- Docker-rendered auth UI shows the configured sign-in screen and does not show the missing Firebase configuration warning.
- Backend token exchange tests passed in the full backend suite.

Limitation:

- A real Firebase login was not executed because no real Firebase credentials were provided in this workspace. The deployment path is now correctly configured to allow it.

## Direct Valuation Continuity

Validated by backend test:

- Direct valuation payload records `request_id`.
- Direct valuation bridge binds the result to workspace and property context.
- Direct valuation ToolEvent creates a `ValuationSnapshot`.
- The `ValuationSnapshot.valuation_id` equals the direct valuation `request_id`.

## ID Continuity

Verified:

- `workspace_id` persists from property bridge into `ValuationSnapshot` and ToolEvent.
- `property_state_id` persists from property bridge into `ValuationSnapshot` and ToolEvent.
- `valuation_id` is written into:
  - `valuation_snapshots.valuation_id`
  - snapshot normalized response
  - direct valuation ToolEvent payload

## Market Intelligence

Verified:

- Market Insight queries `valuation_snapshots` by user and workspace.
- A direct valuation snapshot is counted in `valuation_volume`.
- Direct valuation id appears in `evidence_summary.valuation_ids`.

## Copilot Explainability

Verified:

- `execute_explainability` loads the direct valuation snapshot by `valuation_id`.
- Existing explainability payload is consumed without introducing a new explainability engine.

## Tool Event Persistence

Verified:

- Existing `/v1/copilot/tool-events` endpoint remains the write path.
- Direct valuation ToolEvent is committed with the normalized valuation response attached to payload.

