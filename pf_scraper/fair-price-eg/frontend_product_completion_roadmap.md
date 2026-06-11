# ValorAI Frontend Product Completion Roadmap

Date: 2026-06-09

## Product Positioning

ValorAI is a real estate valuation and intelligence platform.

Primary product surfaces should expose:

- Fair Price Engine
- Valuation Engine
- Explainability
- Comparables
- Market Intelligence
- Negotiation Intelligence
- Investment Intelligence
- Scenario Analysis

Copilot should be treated as an intelligence layer on top of these capabilities, not as the core product identity.

## Roadmap Principles

1. Do not redesign the architecture.
2. Do not rewrite the frontend.
3. Do not introduce auth, security, deployment, infrastructure, or production-hardening work.
4. Expose existing backend business capabilities through additive frontend surfaces.
5. Prefer reuse of current React routes, panels, stores, valuation types, and visual language.
6. Prioritize business value and visible product completeness.

## Current Frontend Status

| Area | Status |
| --- | --- |
| Direct valuation | Exposed |
| Fair price/range/confidence display | Exposed |
| Direct valuation explainability | Partially exposed |
| Direct valuation comparables | Partially exposed |
| Target price/fairness signal | Partially exposed |
| What-if analysis | Missing UI |
| Scenario analysis | Missing UI |
| Market intelligence | Missing UI; Pulse is static |
| Negotiation intelligence | Missing dedicated UI |
| Investment intelligence | Missing UI |
| Property intelligence / saved assets | Missing UI; Assets aliases Valuation |
| Decision history / reports | Missing UI; Vault is static |
| Copilot orchestrator | Hidden |

## Current Backend Status

| Capability | Backend readiness |
| --- | --- |
| Direct valuation route | Ready |
| Tool 1: Valuation | Ready |
| Tool 2: Explainability | Ready |
| Tool 3: Comparable | Ready |
| Tool 4: Fairness | Ready |
| Tool 5: What-if | Ready |
| Tool 6: Negotiation | Ready |
| Tool 7: Investment | Ready |
| Tool 8: Market Insight | Ready |
| Workspaces/properties/scenarios/assumptions | Ready |
| Scenario lineage/tree | Ready |
| Decision history/tool events | Ready |
| Orchestrator response layer | Ready |
| Property comparison through orchestrator/composer | Ready |

## Priority Roadmap

### P0 - Core Product Completion

| Feature | Business value | Why P0 | Backend surface | Frontend work |
| --- | --- | --- | --- | --- |
| What-if Scenario Analysis | Lets users test how property changes affect valuation. This directly expands ValorAI from a price calculator into an intelligence product. | Highest ROI: backend Tool 5 returns deltas, explainability, and comparables; existing valuation UI can be reused. | `POST /v1/copilot/tools/what-if`; scenario/property endpoints as needed. | Add Scenario/What-if panel to Valuation or Assets result view. |
| Minimal Property Intelligence Binding | Enables tool endpoints to operate on a saved property rather than only an ephemeral valuation draft. | Required product bridge for Tools 1-8; not an auth/security task. | `/v1/copilot/workspaces`, `/v1/copilot/properties`, optional `/v1/copilot/scenarios`. | Store current valuation draft as an active property context. |
| Negotiation Intelligence | Converts valuation evidence into buyer/seller leverage, counter-offer range, talking points, and risks. | High user value, especially for brokers and buyers; reuses target price already in the valuation form. | `POST /v1/copilot/tools/negotiation`. | Add Negotiation panel after valuation result. |

### P1 - Intelligence Expansion

| Feature | Business value | Why P1 | Backend surface | Frontend work |
| --- | --- | --- | --- | --- |
| Market Intelligence Pulse | Turns static Pulse into real workspace-level market analytics. | Strong product perception increase, but depends on saved valuation history. | `POST /v1/copilot/tools/market-insight`. | Replace hardcoded Pulse metrics with real distributions, segments, and evidence summary. |
| Investment Intelligence | Gives investors structured opportunity/risk analysis backed by negotiation and valuation evidence. | Valuable but downstream of negotiation and what-if. | `POST /v1/copilot/tools/investment`. | Add Investment panel/cards for position, strengths, risks, and what-if sensitivity. |
| Scenario Library | Lets users save, revisit, and compare valuation scenarios. | Makes What-if durable and repeatable. | `/v1/copilot/scenarios`, scenario lineage/tree endpoints. | Add scenario list, active scenario selector, and scenario detail drawer. |

### P2 - Evidence Depth and Decision Support

| Feature | Business value | Why P2 | Backend surface | Frontend work |
| --- | --- | --- | --- | --- |
| Dedicated Explainability Tool UI | Allows explanation replay from saved valuation snapshots. | Existing direct explainability is usable; dedicated replay is a depth upgrade. | `POST /v1/copilot/tools/explainability`. | Add valuation snapshot selector and explanation replay panel. |
| Dedicated Comparable Tool UI | Allows comparable retrieval/replay by property, scenario, or valuation snapshot. | Existing comparables are usable; dedicated tool improves saved workflows. | `POST /v1/copilot/tools/comparable`. | Add saved comparable explorer mode. |
| Decision History and Tool Events | Turns Vault into a real decision support surface. | Valuable once users run multiple intelligence actions. | `/v1/copilot/workspaces/{workspace_id}/decisions`, `/tool-events`. | Replace static Vault cards with decision timeline and evidence records. |
| Copilot Orchestrator Integration | Provides natural-language access to valuation/intelligence tools. | Important but should sit above completed product surfaces. | `POST /v1/copilot/orchestrator/respond`. | Add an intelligence drawer/contextual assistant tied to active property/scenario. |

### P3 - Advanced Product Surfaces

| Feature | Business value | Why P3 | Backend surface | Frontend work |
| --- | --- | --- | --- | --- |
| Property Comparison | Supports side-by-side valuation decisions. | Useful, but not as foundational as single-property scenarios and negotiation. | Orchestrator/composer property comparison flow. | Add compare mode with Property A/B selection and delta cards. |
| Investment Committee Evidence Packet | Creates executive-ready decision artifacts. | Strong later-stage value but requires decision history maturity. | Existing valuation/comparable/explainability/tool event payloads. | Add export/report UI after decision history exists. |
| Advanced Market Filters | Improves Pulse precision. | Best after initial market insight binding is complete. | Market Insight filters: compound, h3, property type, time window. | Add filters and segment drilldowns. |

## Highest ROI Feature Selection

Selected feature: What-if Scenario Analysis.

### Business Impact

What-if Scenario Analysis changes ValorAI from "tell me the fair price" into "help me decide what to do with this property." It directly supports renovation planning, amenity upgrades, unit configuration decisions, and scenario-based pricing conversations.

### User Impact

Users can answer questions such as:

- What happens if I add a bathroom?
- What happens if this unit is furnished?
- What happens if I add parking or a gym?
- Does this upgrade materially change the fair-price range?
- Which comparable evidence supports the scenario result?

### Backend Readiness

Backend readiness is high. Tool 5 already accepts `workspace_id`, `property_id`, optional `scenario_id`, and `modifications`, then returns:

- Base valuation
- Scenario valuation
- Absolute delta
- Percentage delta
- Fairness status
- Assumptions used
- Feature changes
- Scenario explainability
- Scenario comparables

### UI Complexity

UI complexity is moderate but contained. The frontend can reuse:

- `ValuationScreen`
- `HeroValuationCard` patterns
- `ComparablePanel`
- `ExplainabilityPanel`
- Existing valuation draft fields
- Existing local Zustand valuation state

New UI is mainly a scenario editor and delta panel.

### Engineering Complexity

Engineering complexity is moderate. The largest required bridge is not the What-if panel itself; it is creating or selecting a backend property context so Tool 5 can receive `workspace_id` and `property_id`. This should be implemented as a narrow product bridge, not as a broader architecture rewrite.

### Why This Beats The Alternatives

| Alternative | Why not selected first |
| --- | --- |
| Negotiation Intelligence | Very high value, but stronger after scenario deltas can be used as sensitivity evidence. |
| Market Intelligence | Strong visual impact, but depends on accumulated workspace valuation history. |
| Investment Intelligence | High value, but depends on negotiation and optional what-if evidence. |
| Dedicated Explainability/Comparables | Lower incremental value because direct valuation already exposes a usable subset. |
| Copilot Orchestrator | Important overlay, but product surfaces should expose core intelligence first. |

## Recommended Implementation Order

1. Implement What-if Scenario Analysis on the valuation result surface.
2. Add Negotiation Intelligence using the same active property context.
3. Bind Pulse to Market Insight once multiple valuations/snapshots exist.
4. Add Investment Intelligence after negotiation output is visible.
5. Add Scenario Library and Decision History to make scenarios and decisions durable.
6. Add Copilot orchestrator integration as a contextual intelligence layer over active property/scenario data.

