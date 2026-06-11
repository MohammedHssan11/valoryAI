# Sprint 4 Snapshot Discovery

Date: 2026-06-11

## Scope

Audited direct valuation continuity across backend Copilot persistence, frontend property context bridging, market insight, and explainability.

Files reviewed:

- `pf_scraper/fair-price-eg/backend/app/api/routes/pricing.py`
- `pf_scraper/fair-price-eg/backend/app/api/routes/copilot.py`
- `pf_scraper/fair-price-eg/backend/app/models/copilot.py`
- `pf_scraper/fair-price-eg/backend/app/services/copilot_service.py`
- `pf_scraper/fair-price-eg/backend/app/services/copilot_tools_service.py`
- `pf_scraper/fair-price-eg/frontend/src/services/valuationService.ts`
- `pf_scraper/fair-price-eg/frontend/src/services/propertyContextService.ts`
- `pf_scraper/fair-price-eg/frontend/src/store/valuationStore.ts`
- `pf_scraper/fair-price-eg/frontend/src/types/propertyContext.ts`
- `pf_scraper/fair-price-eg/frontend/src/types/valuation.ts`

## Existing Flow

Direct valuation flow before Sprint 4:

1. React calls `/v1/valuation/fair-price`.
2. Backend returns `RentFairPriceResponse`.
3. React property bridge creates or reuses a workspace.
4. React property bridge creates or reuses a property context.
5. React property bridge records a `direct_valuation` ToolEvent.

Missing piece:

- No `ValuationSnapshot` was created for the direct valuation.

## Existing Snapshot Path

`CopilotToolsService.execute_valuation` already creates:

- `ValuationSnapshot`
- normalized valuation response
- explainability payload
- valuation ToolEvent

That path is used by Copilot tools, not by the direct React valuation screen.

## Smallest Safe Implementation

The direct valuation route cannot bind a snapshot to workspace/property because workspace/property context is created after the valuation response in the frontend bridge.

The smallest safe insertion point is `CopilotService.record_tool_event`, because the existing direct bridge ToolEvent already includes:

- authenticated user
- `workspace_id`
- `property_state_id`
- `request_id`
- original valuation request
- valuation response summary

Sprint 4 extends that existing persistence point to create a `ValuationSnapshot` atomically with the direct valuation ToolEvent.

## Non-Goals Preserved

- No valuation engine changes.
- No valuation response contract changes.
- No Copilot orchestration changes.
- No broker behavior changes.
- No new intelligence tools.
- No UI redesign.

