# ValorAI Frontend Feature Gap Verification

Date: 2026-06-09

## Scope

This verification reviews the React frontend under `frontend/`, the FastAPI backend under `backend/`, project documentation under `docs/`, workspace-level ValorAI documentation, and available `PROJECT_MASTER_STATE*` files.

This document focuses only on business capabilities:

- Valuation
- Explainability
- Comparables
- What-if analysis
- Market intelligence
- Negotiation intelligence
- Investment intelligence
- Scenario analysis
- Property intelligence
- Decision support
- Copilot as an intelligence layer

Explicitly excluded from this verification:

- Authentication
- Authorization
- Security hardening
- Deployment
- Infrastructure
- Production operations

## Product Positioning Correction

ValorAI should be treated as a real estate valuation and intelligence platform. The Copilot/orchestrator layer is not the primary product surface. It is an intelligence layer above the valuation, evidence, scenario, negotiation, investment, and market intelligence capabilities.

## Evidence Reviewed

Primary backend evidence:

- `backend/app/api/routes/pricing.py`
- `backend/app/api/routes/copilot_tools.py`
- `backend/app/api/routes/copilot.py`
- `backend/app/api/routes/copilot_orchestrator.py`
- `backend/app/api/routes/broker.py`
- `backend/app/api/schemas/pricing.py`
- `backend/app/api/schemas/copilot_tools.py`
- `backend/app/api/schemas/copilot.py`
- `backend/app/api/schemas/copilot_orchestrator.py`
- `backend/app/services/copilot_tools_service.py`
- `backend/app/copilot/orchestrator/*`
- `backend/app/broker/*`

Primary frontend evidence:

- `frontend/src/app/App.tsx`
- `frontend/src/services/valuationService.ts`
- `frontend/src/services/brokerService.ts`
- `frontend/src/features/valuation/ValuationScreen.tsx`
- `frontend/src/features/comparables/ComparablePanel.tsx`
- `frontend/src/features/explainability/ExplainabilityPanel.tsx`
- `frontend/src/features/evidence/*`
- `frontend/src/features/broker/BrokerScreen.tsx`
- `frontend/src/features/pulse/PulseScreen.tsx`
- `frontend/src/features/assets/AssetsScreen.tsx`
- `frontend/src/features/vault/VaultScreen.tsx`
- `frontend/src/types/broker.ts`
- `frontend/src/types/valuation.ts`
- `frontend/src/store/*`

Primary documentation evidence:

- `docs/04_fair_price_engine.md`
- `docs/09_explainability.md`
- `docs/10_tools_layer.md`
- `docs/11_orchestrator.md`
- `docs/12_product_analysis.md`
- `docs/PHASE_5_5B_4_WHAT_IF_IMPLEMENTATION_REPORT.md`
- `docs/PHASE_5_5B_5_NEGOTIATION_TOOL_IMPLEMENTATION_REPORT.md`
- `docs/PHASE_5_5B_6_INVESTMENT_TOOL_IMPLEMENTATION_REPORT.md`
- `docs/PHASE_5_5B_7_MARKET_INSIGHT_IMPLEMENTATION_REPORT.md`
- `docs/PROPERTY_COMPARISON_V1_SPEC.md`
- `docs/COMPOSED_RESPONSE_CONTRACT_V1.md`
- `PROJECT_MASTER_STATE.md`
- Workspace-level `PROJECT_MASTER_STATE*`

## Verification Matrix

| Claimed gap | Verification result | Classification | Notes |
| --- | --- | --- | --- |
| Direct valuation is missing from the frontend | `frontend/src/services/valuationService.ts` calls `POST /v1/valuation/fair-price`; `ValuationScreen` renders a real valuation form and result card. | False positive | Direct valuation is exposed. |
| Core fair-price output is not exposed | `HeroValuationCard` and `ValuationScreen` render fair price, range, confidence, target price context, and request metadata. | False positive | Core fair-price output exists. |
| Explainability is completely hidden | `ExplainabilityPanel` renders confidence, trace events, retrieval timeline, evidence summary, valuation contract, and amenity intelligence from the direct valuation response. | False positive | The complete dedicated Tool 2 workflow is still missing, but direct response explainability is present. |
| Dedicated backend Explainability Tool is not exposed | No frontend service calls `/v1/copilot/tools/explainability`. Frontend only uses explainability fields already embedded in direct valuation output. | Partial gap | The business capability is partially visible, but not as a snapshot replay or standalone explanation workflow. |
| Comparable evidence is completely hidden | `ComparablePanel` renders `top_comps`, supports sorting/filtering, and uses `EvidenceMap`. | False positive | Direct valuation comparables are exposed. |
| Dedicated backend Comparable Tool is not exposed | No frontend service calls `/v1/copilot/tools/comparable`. Comparable analysis is limited to the latest direct valuation response. | Partial gap | Users cannot retrieve comparables from a saved property/scenario/valuation snapshot. |
| Fairness analysis is completely missing | Direct valuation accepts `target_price_egp` and can surface the valuation flag/price range relationship. | Partial gap | Basic fairness is present through the direct valuation route, but `/v1/copilot/tools/fairness` is not exposed. |
| What-if analysis is missing | Backend implements `POST /v1/copilot/tools/what-if` and docs show Tool 5 as complete. Frontend has no what-if service, route, panel, scenario editor, or delta display. | Real gap | This is a true missing product capability. |
| Scenario analysis is missing | Backend exposes scenario CRUD, lineage, scenario tree, and Tool 5 scenario overlays. Frontend has no saved scenario model or scenario UI. | Real gap | Scenario analysis is a product gap, not an infrastructure gap. |
| Market intelligence is missing | Backend implements `POST /v1/copilot/tools/market-insight`; frontend `PulseScreen` displays hardcoded metrics and no backend calls. | Real gap | Pulse is a visual concept screen, not a market intelligence integration. |
| Negotiation intelligence is missing | Backend implements `POST /v1/copilot/tools/negotiation` with offer bands, positions, talking points, risks, and optional what-if evidence. Frontend Broker has generic investor-risk prompts but no Tool 6 integration or structured negotiation UI. | Partial gap | Conceptually hinted through Broker UI, but the real negotiation capability is not exposed. |
| Investment intelligence is missing | Backend implements `POST /v1/copilot/tools/investment`. Frontend has broker prompt language and static Vault concepts, but no Tool 7 service or structured investment UI. | Real gap | Investment capability is effectively hidden in React. |
| Property intelligence is missing | Backend exposes workspaces, properties, scenarios, assumptions, tool events, and decisions. Frontend only keeps valuation draft/result in local Zustand stores. | Real gap | There is no React property workspace or saved property intelligence workflow. |
| Decision history is missing | Backend exposes `/v1/copilot/workspaces/{workspace_id}/decisions` and tool events. `VaultScreen` is static and does not query backend history. | Real gap | Vault is not connected to persisted decision support. |
| Copilot orchestrator is not integrated | Backend exposes `POST /v1/copilot/orchestrator/respond`. Frontend has no service, types, or route calling it. | Real gap | The Copilot layer is hidden in React. |
| Broker screen is absent | `BrokerScreen` exists and calls legacy broker endpoints. | False positive | The screen exists. The gap is contract/current capability alignment. |
| Broker is fully aligned with backend | Backend broker request schemas require `workspace_id` and `scenario_id`; frontend `BrokerReasonRequest` omits both and sends only `session_id`, `message`, and optional `valuation_request`. | Real gap | This is a business-context binding gap. It is not counted as auth/security work here. |
| Assets/portfolio is exposed | `AssetsScreen` simply returns `ValuationScreen`. | Real gap | There is no asset list, saved property portfolio, or property intelligence surface. |
| Vault is a real intelligence/history product surface | `VaultScreen` contains hardcoded values such as global data points, persisted queries, and reports without backend calls. | Real gap | Vault is a static concept screen. |
| Pulse is a real market intelligence surface | `PulseScreen` contains hardcoded liquidity/yield/anomaly content and a remote image background without backend calls. | Real gap | Pulse is a static concept screen. |
| Property comparison is exposed | Backend Response Composer supports reduced Property Comparison V1 over two Tool 1 calls; frontend has no property comparison screen or input flow. | Real gap | No side-by-side property comparison UI exists. |
| Assumptions are exposed | Backend exposes assumptions and What-if responses include `assumptions_used`; frontend has no assumptions panel or assumption confirmation flow. | Real gap | Missing from React. |

## Backend Capability Summary

| Capability | Backend status | Frontend status |
| --- | --- | --- |
| Fair Price Engine | Implemented through direct pricing route and Tool 1 | Exposed through valuation screen |
| Explainability | Implemented in direct response and Tool 2 | Partially exposed through valuation result |
| Comparables | Implemented in direct response and Tool 3 | Partially exposed through valuation result |
| Fairness | Implemented in direct response path and Tool 4 | Partially exposed through target price/flag |
| What-if | Implemented as Tool 5 | Missing UI |
| Negotiation | Implemented as Tool 6 | Missing dedicated UI |
| Investment | Implemented as Tool 7 | Missing UI |
| Market Insight | Implemented as Tool 8 | Missing UI; Pulse is static |
| Workspace/property/scenario memory | Implemented | Missing React product surface |
| Scenario lineage/tree | Implemented | Missing UI |
| Decision history/tool events | Implemented | Missing UI; Vault is static |
| Orchestrator/Copilot response layer | Implemented | Hidden in React |
| Property comparison | Implemented in composer/orchestrator path | Missing UI |

## Corrected Gap Conclusions

The previous audit was directionally correct that the backend is ahead of the React frontend, but several "missing" claims need precision:

1. Valuation is not missing. It is the strongest exposed React capability.
2. Explainability is not missing. It is partially exposed from direct valuation responses.
3. Comparables are not missing. They are partially exposed from direct valuation responses.
4. Fairness is not missing. It is partially exposed through target price and pricing flag behavior.
5. The true high-value frontend gaps are What-if Scenario Analysis, Market Intelligence, Negotiation Intelligence, Investment Intelligence, Property/Scenario Intelligence, Decision History, and the Copilot intelligence layer.
6. Pulse, Assets, and Vault currently read as product surfaces but do not expose the backend business systems their labels imply.

## Highest-Confidence Real Gaps

1. What-if Scenario Analysis
2. Market Intelligence
3. Negotiation Intelligence
4. Investment Intelligence
5. Property Workspace / Saved Property Intelligence
6. Scenario Library / Lineage
7. Decision History / Tool Events
8. Copilot Orchestrator Integration
9. Property Comparison

## Highest-Confidence Partial Gaps

1. Explainability: direct response exposed; dedicated Tool 2 hidden.
2. Comparables: direct response exposed; dedicated Tool 3 hidden.
3. Fairness: target price behavior exposed; dedicated Tool 4 hidden.
4. Broker: UI exists; current React request contract does not bind workspace/scenario and does not expose Tools 3-8.

