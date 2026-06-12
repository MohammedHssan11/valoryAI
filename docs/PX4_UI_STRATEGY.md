# PX-4 Market Intelligence UI Strategy

Status: Discovery only
Report date: 2026-06-10
Scope: Placement strategy for Market Intelligence in the existing React frontend

No implementation was performed.

## Decision

Market Intelligence should be implemented as a shared Market Intelligence section in `Pulse`, not primarily embedded inside Valuation, What-if, Negotiation, or Investment.

Recommended placement:

```text
Primary surface: Pulse tab
Secondary context: optional compact Market Context summary near Valuation or Investment later
Copilot: later overlay after product surfaces are real
```

This matches the backend contract because Tool 8 is workspace-first:

```text
POST /v1/copilot/tools/market-insight
required input: workspace_id
optional filters: compound_name, h3_res9, property_type, time_window
```

It does not require a property ID, asking price, scenario ID, or active negotiation state.

## Existing Flow Review

### Valuation Flow

Files:

- `frontend/src/features/valuation/ValuationScreen.tsx`
- `frontend/src/services/valuationService.ts`
- `frontend/src/store/valuationStore.ts`
- `frontend/src/services/propertyContextService.ts`
- `frontend/src/store/propertyContextStore.ts`

Current behavior:

- Direct valuation is a real product surface.
- User submits a property profile to `POST /v1/valuation/fair-price`.
- The result shows fair price, range, confidence, explainability, and comparables.
- After a successful valuation, the frontend bridges the valuation into backend property context:
  - workspace
  - property
  - direct valuation tool event
- The property context store persists:
  - `activeWorkspaceId`
  - `activePropertyId`
  - `activeScenarioId`
  - bridge status

Market Intelligence relevance:

- Valuation is the main source of persisted valuation history that Market Insight later reads.
- Valuation should remain property-specific.
- It should not be overloaded with a full workspace market dashboard.

Best future Valuation integration:

- A compact "Market Context" card can appear after `activeWorkspaceId` exists.
- It should default to the active property's compound or property type only if those filters are available.
- It should link users to the full Pulse surface.

### What-if Flow

Files:

- `frontend/src/features/what-if/WhatIfScenarioPanel.tsx`
- `frontend/src/services/whatIfService.ts`
- `frontend/src/store/whatIfStore.ts`
- `frontend/src/store/scenarioHistoryStore.ts`

Current behavior:

- What-if is nested under a completed valuation.
- It requires backend property context before it can run.
- It edits property features and submits Tool 5.
- It displays scenario deltas, feature changes, assumptions, explainability, comparables, scenario history, and scenario comparison.

Market Intelligence relevance:

- What-if is property and scenario specific.
- Market Insight is workspace and filter specific.
- Market Insight can contextualize scenario decisions, but it should not be embedded as a required step in scenario editing.

Best future What-if integration:

- Show sparse market context only as an optional aside if needed.
- Do not put the full Market Intelligence experience inside the scenario editor.

### Negotiation Flow

Files:

- `frontend/src/features/what-if/NegotiationIntelligencePanel.tsx`
- `frontend/src/services/negotiationService.ts`
- `frontend/src/store/negotiationStore.ts`
- `frontend/src/types/negotiation.ts`

Current behavior:

- Negotiation is nested under What-if.
- It requires `workspace_id`, `property_id`, and `asking_price_egp`.
- It can target base valuation, active unsaved scenario, or selected saved scenario.
- It returns offer strategy, price gap, recommended offer band, evidence, talking points, and risk notes.

Market Intelligence relevance:

- Negotiation answers "how should I position this offer?"
- Market Insight answers "what does our persisted workspace history say?"
- Market Insight can support negotiation context but cannot replace negotiation evidence.

Best future Negotiation integration:

- Add a small "Market evidence quality" line if the active workspace has Market Insight data.
- Keep negotiation outputs grounded in Tool 6.

### Investment Flow

Files:

- `frontend/src/features/investment/InvestmentIntelligencePanel.tsx`
- `frontend/src/services/investmentService.ts`
- `frontend/src/store/investmentStore.ts`
- `frontend/src/types/investment.ts`

Current behavior:

- Investment is nested under What-if.
- It requires `workspace_id`, `property_id`, and `asking_price_egp`.
- It can target base valuation, active unsaved scenario, selected saved scenario, or compared saved scenarios.
- It returns investment position, strengths, risks, evidence, negotiation summary, what-if sensitivity, and scenario comparison.

Market Intelligence relevance:

- Investment is decision support for a specific property and asking price.
- Market Insight is broader evidence context.
- Market Insight should be available before or alongside investment, but not hidden inside it.

Best future Investment integration:

- Add a compact market context component after Pulse is real.
- Use only supported fields such as confidence distribution and comparable density.
- Do not infer investment recommendation from Market Insight alone.

### Pulse Flow

File:

- `frontend/src/features/pulse/PulseScreen.tsx`

Current behavior:

- Pulse is a static/cinematic concept screen.
- It displays hardcoded:
  - liquidity index
  - yield variance
  - intensity spectrum
  - live anomalies
  - buy signal
- It uses a remote map-like image.
- It does not call Market Insight or any backend API.

Market Intelligence relevance:

- Pulse is the correct top-level destination for Tool 8.
- It already carries the product meaning of "market pulse".
- It must be rewritten from unsupported concept metrics into contract-backed analytics.

## Placement Options

### Option A: Embed in Investment

Decision: Not recommended as the primary PX-4 surface.

Pros:

- Investment users benefit from market context.
- Can support opportunity and risk review.

Cons:

- Tool 8 does not require asking price or property ID.
- Market Intelligence would be invisible to non-investment users.
- It would imply market context is only an investment sub-feature.
- Investment is downstream of valuation, scenario, and negotiation state.

Use later:

- Add a compact Market Context card in Investment after Pulse is real.

### Option B: Embed in Valuation

Decision: Not recommended as the primary PX-4 surface.

Pros:

- Valuation produces the history Market Insight needs.
- Users naturally want local context around a valuation.

Cons:

- Valuation is property-specific.
- Full Market Intelligence is workspace-level and filterable.
- The valuation screen is already dense with explainability, comparables, What-if, Negotiation, and Investment.

Use later:

- Add a compact "Workspace Market Context" card after valuation results.

### Option C: Embed in Scenario Analysis

Decision: Not recommended.

Pros:

- Scenarios benefit from market context.

Cons:

- Tool 8 is not scenario-specific.
- Scenario users need feature deltas first.
- Full Market Intelligence would distract from the scenario workflow.

Use later:

- Market evidence quality can be shown when comparing saved scenarios.

### Option D: Standalone Panel

Decision: Recommended if implemented as the Pulse surface.

Pros:

- Matches workspace-level nature.
- Supports filtering and sparse states.
- Replaces a static product gap with real backend data.
- Can become a reusable shared section.

Cons:

- Empty workspaces need a strong no-data state.
- Users may expect live market metrics because existing Pulse copy implies them.

Mitigation:

- Use accurate copy and evidence disclosures.
- Provide a call to run valuations when no history exists.

### Option E: Shared Intelligence Section

Decision: Recommended product model.

Meaning:

- Market Intelligence should be a shared source of workspace context.
- Pulse owns the full experience.
- Valuation, Investment, and Copilot can consume compact summaries later.

This is the best long-term shape.

## Recommended UI Architecture

### Primary Surface: Pulse Market Intelligence

Replace the static Pulse content with a contract-backed panel:

```text
PulseScreen
  -> MarketIntelligencePanel
     -> MarketInsightFilters
     -> MarketSummaryCards
     -> MarketDistributionGrid
     -> ActiveSegmentsTable
     -> EvidenceStatements
     -> DataSourcesDisclosure
     -> EmptySparseState
```

Suggested file placement for implementation:

```text
frontend/src/features/pulse/MarketIntelligencePanel.tsx
frontend/src/types/marketInsight.ts
frontend/src/services/marketInsightService.ts
frontend/src/store/marketInsightStore.ts
```

### Inputs

Minimum:

- `workspace_id`

Filters:

- `compound_name`
- `property_type`
- `h3_res9`
- `time_window`

Recommended first PX-4 controls:

- Time window segmented control:
  - `all`
  - `30d`
  - `90d`
- Property type select.
- Compound text/select if discovered from returned active compounds.
- H3 field only as an advanced filter unless a user-facing area selector exists.

Do not create a fake map interaction unless it maps to real H3 filters.

### Output Sections

Summary:

- Market summary text.
- Valuation volume.
- Source label: TruthLayer.
- Timestamp.

Evidence quality:

- Comparable density label.
- Median comparable count.
- Confidence distribution.
- Sparse-state warning if needed.

Observed fair values:

- Minimum.
- Median.
- Maximum.
- Count of fair-value observations.

Segments:

- Active compounds:
  - name
  - valuation count
  - median fair value
  - confidence distribution
  - comparable density
- Active areas:
  - same fields

Traceability:

- Statements with evidence references.
- Filters used.
- Source record counts.
- Data sources used.

### Empty State

When `valuation_volume == 0`, the UI should say:

```text
No persisted TruthLayer valuations match these filters.
```

It should offer a path back to valuation:

```text
Run valuations to build workspace market history.
```

It should not show blank charts with fake trend lines.

### Sparse State

When comparable density is `Sparse` or `Insufficient Evidence`, the UI should emphasize evidence quality:

```text
Evidence is sparse. The market pulse is descriptive only and should not be treated as a forecast.
```

## What UI Should Exist

PX-4 should create:

- Real Pulse Market Intelligence panel.
- Market Insight request and response types.
- Market Insight service wrapper.
- Market Insight store for request, response, filters, loading, and error.
- Filter controls that map exactly to backend request fields.
- Summary cards using only backend fields.
- Segment tables for compounds and areas.
- Evidence statements list.
- Traceability disclosure.
- Empty and sparse states.
- Tests for service validation, store behavior, and UI states.

## What UI Should Not Exist

PX-4 should not create:

- Forecast charts.
- Demand/supply trend charts.
- Yield cards.
- Liquidity index cards.
- Buy/sell signal cards.
- Capital inflow or live anomaly cards.
- Heatmap claims without H3-backed values.
- Investment recommendations from Market Insight alone.
- A Copilot chat UI.
- New backend routes.
- New backend services.
- New backend stores.

## Copy Strategy

Use:

- "Market Intelligence"
- "Workspace market pulse"
- "Persisted valuation history"
- "Observed fair values"
- "Comparable density"
- "Evidence quality"
- "Traceable statements"
- "No persisted valuations match"

Avoid:

- "Live"
- "Real-time"
- "Predictive"
- "Forecast"
- "Demand up"
- "Supply down"
- "Buy signal"
- "Yield"
- "Liquidity"
- "Overheated"
- "Undervalued market"

## Critical UX Boundary

Market Insight can make the product feel much more intelligent, but only if it stays honest.

The UI should make this clear:

```text
This is descriptive analytics over persisted TruthLayer records.
```

That line is not decoration. It is the product safety boundary.

## UI Strategy Conclusion

Market Intelligence belongs in Pulse as a shared workspace intelligence section. It should be available to Valuation and Investment later as compact context, but PX-4 should first turn Pulse from a static concept into a real evidence-backed backend surface.
