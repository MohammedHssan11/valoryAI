# PX-4 Market Intelligence Implementation Plan

Status: Planning only
Report date: 2026-06-10
Scope: Future frontend implementation plan for Market Intelligence

No implementation was performed. This document is a plan, not a change report.

## Decision Summary

Implement PX-4 before Copilot.

Reason:

Market Intelligence is a core product capability with a complete backend Tool 8 contract. Copilot is an overlay that can already route to Tool 8, but users still cannot inspect Market Intelligence directly in the product. Implementing Pulse first makes the product capability real, testable, and reusable. Copilot can then narrate or invoke a surface users already understand.

## Evidence for Implementing Before Copilot

Backend evidence:

- `POST /v1/copilot/tools/market-insight` is implemented.
- Tool 8 has schemas, service logic, persistence, tests, and Docker validation.
- Orchestrator already classifies `MARKET_INSIGHT`, plans `MARKET_INSIGHT_TOOL`, executes it, normalizes it, and handles sparse evidence.
- The backend response is frontend-safe and evidence-backed.

Frontend evidence:

- `PulseScreen` is currently static and hardcoded.
- It does not call the backend.
- It displays unsupported metrics such as liquidity, yield variance, live anomalies, and a buy signal.
- Existing valuation, what-if, negotiation, and investment flows are now real product surfaces.
- Market Intelligence is the remaining high-value intelligence surface before Copilot.

Product evidence:

- ValorAI is positioned as a real estate valuation and intelligence platform.
- Copilot should sit on top of real product capabilities, not hide missing ones.
- Market Intelligence gives users a non-chat way to inspect evidence.

## Business Impact

Implementing PX-4 before Copilot will:

- Replace a static Pulse concept with real backend value.
- Expose a core intelligence capability without requiring natural language.
- Improve trust by showing evidence quality and traceability.
- Give users a workspace-level market view after they run valuations.
- Make the later Copilot feel grounded in visible product surfaces.

If Copilot is implemented first:

- Users may ask market questions and receive responses from a capability they cannot inspect directly.
- The app would still contain a static Pulse page with unsupported claims.
- Copilot would amplify the product gap instead of resolving it.

## User Impact

PX-4 first gives users:

- A real Market Intelligence tab.
- Filtered workspace history.
- Evidence-backed statements.
- Sparse-state disclosure.
- Confidence and comparable-density context.

Copilot first gives users:

- A conversational entry point, but not a direct market intelligence surface.
- Higher risk of perceived hallucination if the user cannot inspect the underlying market evidence.

Decision:

```text
Market Intelligence should be implemented before Copilot.
```

## Implementation Scope

PX-4 should be a frontend integration of existing backend Tool 8.

Allowed:

- Frontend types.
- Frontend service.
- Frontend store.
- Pulse UI replacement.
- Fixtures.
- Tests.
- Documentation.
- Master-state updates after completion.

Not allowed unless a later phase explicitly authorizes it:

- Backend route changes.
- Backend schema changes.
- Backend service changes.
- Backend migrations.
- Copilot UI.
- Forecasting logic.
- Demand or supply modeling.
- New scraper work.
- New market-data provider work.

## Files to Create

### Types

```text
frontend/src/types/marketInsight.ts
```

Should define:

- `MarketInsightToolRequest`
- `MarketInsightConfidenceDistribution`
- `MarketInsightFairValueDistribution`
- `MarketInsightComparableDensity`
- `MarketInsightSegment`
- `MarketInsightStatement`
- `MarketInsightEvidenceSummary`
- `MarketInsightToolResponse`
- `MarketInsightFilters`
- `MarketInsightRunRecord`, if storing run history is desired

The frontend type names should mirror backend schema names.

### Service

```text
frontend/src/services/marketInsightService.ts
frontend/src/services/marketInsightService.test.ts
```

Service behavior:

- Validate `workspace_id > 0`.
- Validate optional `compound_name`, `h3_res9`, `property_type`, and `time_window`.
- Normalize omitted `time_window` to backend default behavior or send `all` explicitly.
- Strip undefined fields before POST.
- Call `POST /v1/copilot/tools/market-insight`.
- Accept standard API envelopes and unenveloped payloads if the rest of the frontend still supports both patterns.
- Validate the response before the UI receives it.
- Preserve nullable values exactly.
- Reject malformed distributions, density labels, missing source, or unsupported tool name.

### Store

```text
frontend/src/store/marketInsightStore.ts
frontend/src/store/marketInsightStore.test.ts
```

Store state:

- `lastRequest`
- `lastResponse`
- `filters`
- `isLoading`
- `error`
- optional `runs`
- `runMarketInsight`
- `setFilters`
- `resetFilters`
- `clearMarketInsight`
- `resetMarketInsight`

Recommended persistence:

- Do not persist full responses initially.
- Persist only filters if useful.
- Use `activeWorkspaceId` from `propertyContextStore` as the default workspace source.

### UI Components

```text
frontend/src/features/pulse/MarketIntelligencePanel.tsx
frontend/src/features/pulse/MarketIntelligencePanel.test.tsx
```

Component responsibilities:

- Read `activeWorkspaceId` from `propertyContextStore`.
- Render no-workspace state when no workspace exists.
- Render filter controls.
- Run Market Insight.
- Render loading, error, empty, sparse, and success states.
- Render summary, distributions, segments, and evidence.
- Avoid unsupported market claims.

Optional subcomponents can be created only if the panel becomes too large:

```text
frontend/src/features/pulse/MarketInsightFilters.tsx
frontend/src/features/pulse/MarketInsightSummary.tsx
frontend/src/features/pulse/MarketInsightSegments.tsx
frontend/src/features/pulse/MarketInsightEvidence.tsx
```

Keep subcomponents local to `features/pulse` unless reuse is needed.

### Fixtures

```text
frontend/src/test/fixtures.ts
```

Add:

- `sampleMarketInsightResponse`
- `sampleSparseMarketInsightResponse`
- `sampleEmptyMarketInsightResponse`

Fixtures should include:

- non-null fair-value distribution
- null fair-value distribution
- active compounds
- active areas
- evidence statements
- source record counts
- sparse density
- `valuation_volume = 0`

## Files to Modify

### Pulse Screen

```text
frontend/src/features/pulse/PulseScreen.tsx
```

Modify by:

- Removing unsupported hardcoded metrics.
- Rendering `MarketIntelligencePanel`.
- Preserving the route and tab identity.
- Keeping visual treatment consistent with the app, but grounded in real backend fields.

Do not keep:

- Liquidity index.
- Yield variance.
- Live anomalies.
- Buy signal.
- Capital inflow copy.

### Top Navigation, Optional

```text
frontend/src/components/layout/TopNav.tsx
```

Optional small update:

- Add a truthful Pulse status label only if needed.

Allowed copy:

```text
MARKET HISTORY
```

Avoid:

```text
LIVE MARKET
```

### Documentation

After implementation only, update:

```text
pf_scraper/fair-price-eg/docs/PX4_COMPLETION_REPORT.md
pf_scraper/fair-price-eg/PROJECT_MASTER_STATE.md
PROJECT_MASTER_STATE_V2.md
PROJECT_MASTER_STATE_v3.md
docs/PROJECT_MASTER_STATE.md
docs/PROJECT_MASTER_STATE_BACKUP.md
docs/PROJECT_MASTER_STATE_V2.md
docs/PROJECT_MASTER_STATE_v3.md
```

Only update master-state files after PX-4 is actually implemented and verified.

## Files Not to Modify

Do not modify backend files for PX-4 frontend integration:

```text
backend/app/api/routes/copilot_tools.py
backend/app/api/schemas/copilot_tools.py
backend/app/services/copilot_tools_service.py
backend/app/models/copilot.py
backend/app/db/migrations/*
backend/app/copilot/orchestrator/*
```

Do not modify Copilot UI or orchestrator routes for PX-4:

```text
frontend/src/features/broker/*
frontend/src/services/brokerService.ts
backend/app/api/routes/copilot_orchestrator.py
```

## UI Requirements

### No Workspace State

Trigger:

- `activeWorkspaceId` is null.

UI:

- Explain that Market Intelligence needs a workspace with persisted valuation history.
- Provide a route/action toward valuation.

No backend call should be made.

### Loading State

UI:

- Show skeleton or subdued loading cards.
- Preserve filter layout to avoid layout shift.

### Empty Evidence State

Trigger:

- `valuation_volume == 0`.

UI:

- Show the backend statement.
- Show filters used.
- Show data sources.
- Tell user to run valuations or widen filters.

No fake charts.

### Sparse Evidence State

Trigger:

- `comparable_density.density_level` is `Sparse` or `Insufficient Evidence`.

UI:

- Show evidence warning.
- Still render available distributions and statements.
- Do not hide the response.

### Success State

Render:

- Market summary.
- Valuation volume.
- Fair-value min/median/max.
- Confidence distribution.
- Comparable density.
- Active compounds.
- Active areas.
- Evidence statements.
- Data sources and source record counts.
- Traceability note.

## Service Validation Requirements

Request validation:

- `workspace_id` must be a positive integer.
- `time_window` must be `all` or positive day string.
- Empty optional strings should be treated as omitted.
- `compound_name`, `h3_res9`, and `property_type` should be bounded strings.

Response validation:

- `tool_name` must be `market_insight`.
- `source` must be `TruthLayer`.
- Density must be one of backend literals.
- Nullable fair-value fields must be accepted.
- Nullable comparable-count fields must be accepted.
- Arrays must be arrays.
- Evidence statements must include text and evidence array.

## Store Requirements

The store should:

- Set loading true before request.
- Store `lastRequest`.
- Store `lastResponse` on success.
- Store normalized `Error` on failure.
- Clear loading after success or failure.
- Avoid stale errors after a new run.
- Support reset for valuation context resets if needed.

## Test Plan

### Service Tests

Test:

- Posts to `/v1/copilot/tools/market-insight`.
- Sends valid request body.
- Strips undefined optional fields.
- Accepts enveloped response.
- Accepts unenveloped response if matching app service pattern.
- Preserves null fair-value fields.
- Preserves empty segments.
- Rejects invalid `workspace_id`.
- Rejects invalid `time_window`.
- Rejects malformed backend payload.
- Supports abort signal.

### Store Tests

Test:

- Runs service and stores request/response.
- Stores filters.
- Clears stale errors.
- Maps thrown values to `Error`.
- Resets state.

### UI Tests

Test:

- No workspace state disables or avoids run.
- Run button calls store with active workspace.
- Filter controls map to backend request fields.
- Success renders:
  - market summary
  - valuation volume
  - median fair value
  - confidence distribution
  - comparable density
  - active compounds
  - active areas
  - evidence statements
- Empty state renders without fake metrics.
- Sparse state renders evidence warning.
- Error state renders service error.
- Unsupported words such as `Buy Signal`, `Yield Var`, `Liquidity Index`, and `Capital Inflow` are absent.

### Regression Tests

Run from `frontend`:

```text
npm run lint
npm test
npm run build
```

If backend integration validation is requested later:

```text
scripts/validate_copilot_market_insight.ps1
```

## Implementation Sequence

1. Add `marketInsight.ts` types.
2. Add `marketInsightService.ts` and tests.
3. Add `marketInsightStore.ts` and tests.
4. Add market fixtures.
5. Add `MarketIntelligencePanel.tsx` and tests.
6. Replace static `PulseScreen` body with the real panel.
7. Run frontend lint, tests, and build.
8. Create PX-4 completion report.
9. Update master-state files with actual changed files and verification results.

## Acceptance Criteria

PX-4 is complete only when:

- Pulse calls the real Market Insight backend service.
- The UI renders real Tool 8 fields.
- Empty and sparse evidence are handled truthfully.
- Unsupported static Pulse claims are removed.
- Service, store, and UI tests pass.
- Frontend build passes.
- No backend code was changed.
- No Copilot implementation was started.
- Master state is updated after verification.

## Non-Goals

PX-4 does not include:

- Copilot chat UI.
- Orchestrator frontend integration.
- Market forecasts.
- Time-series growth analytics.
- Demand/supply analytics.
- Fresh scraping.
- External market data.
- Portfolio asset management.
- Decision history.
- Property comparison.

## Future Follow-Ups

After PX-4:

- Add compact Market Context cards to Valuation and Investment.
- Add advanced H3 area selection if there is a real map or area resolver UI.
- Add decision history or Vault integration for persisted market insight runs.
- Add Copilot UI only after Market Intelligence is visible as a normal product surface.

## Final Recommendation

Implement Market Intelligence before Copilot.

PX-4 should make the existing Tool 8 backend visible through Pulse as a truthful, filterable, evidence-backed market history surface. Copilot should come after that, as a conversational layer over capabilities users can already inspect directly.
