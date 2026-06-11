# Final Tool Audit

Audit date: 2026-06-10

## Tool Status Matrix

| Tool / Capability | Backend Status | React Status | Mobile Status | Verdict |
| --- | --- | --- | --- | --- |
| Direct valuation | Implemented at `/v1/valuation/fair-price`; public success envelope. Evidence: `backend/app/api/routes/pricing.py:17`. | Implemented through valuation service and screen. | Implemented through Dio data source. | Usable core workflow. |
| Protected valuation tool | Implemented in Copilot tools. Evidence: `backend/app/api/routes/copilot_tools.py:40-47`, `backend/app/services/copilot_tools_service.py:425`. | Service/store inputs exist, but requests need auth. | Indirectly reachable through Copilot orchestrator. | Backend ready; React blocked by auth. |
| Explainability tool | Implemented and requires a persisted `valuation_id`. Evidence: `backend/app/services/copilot_tools_service.py:487`. | Copilot store only sends explainability when a tool-generated valuation id exists. Evidence: `frontend/src/store/copilotStore.ts:152-156`. | Not a full standalone UX. | Real but prerequisite-sensitive. |
| Comparable tool | Implemented. Evidence: `backend/app/services/copilot_tools_service.py:517`. | Used through services/stores and direct valuation result presentation. | Valuation response mapping covers comparables. | Mostly ready after auth/context. |
| Fairness tool | Implemented. Evidence: `backend/app/services/copilot_tools_service.py:571`. | Indirectly used in what-if/negotiation/investment flows. | Not a full standalone UX. | Backend ready; product exposure partial. |
| What-if | Implemented. Evidence: `backend/app/services/copilot_tools_service.py:1822`. | UI/service/store/tests exist; run button requires workspace/property context. Evidence: `frontend/src/features/what-if/WhatIfScenarioPanel.tsx:1246`. | Not full parity. | React UI is present but blocked by auth bridge. |
| Negotiation | Implemented. Evidence: `backend/app/services/copilot_tools_service.py:995`. | UI/service/store/tests exist; requires protected context. | Not full parity. | Backend ready; React blocked by auth bridge. |
| Investment | Implemented. Evidence: `backend/app/services/copilot_tools_service.py:1393`. | UI/service/store/tests exist; requires protected context. | Not full parity. | Backend ready; React blocked by auth bridge. |
| Market insight | Implemented as descriptive workspace analysis from snapshots/logs/events. Evidence: `backend/app/services/copilot_tools_service.py:1566-1678`. | UI/service/store/tests exist; requires authenticated workspace and prior protected-tool snapshots. | Not full parity. | Real but empty for first-time/direct-only web users. |
| Broker reasoning | Implemented as protected broker endpoints. Evidence: `backend/app/api/routes/broker.py:31,100-126`. | UI exists, but request contract is missing `workspace_id` and `scenario_id`. | Not primary. | Blocked on web by auth and schema mismatch. |
| Copilot orchestrator | Implemented deterministic runtime. Evidence: `backend/app/copilot/orchestrator/runtime.py:93-248`. | Drawer/store/service exist; require active workspace and protected endpoint. | Implemented in mobile remote data source and covered by tests. | Backend real; React integration incomplete. |

## Tool Chain Findings

1. Direct valuation is the most demo-ready tool. It is public, wired in React, and mapped in Flutter.
2. The protected tools are not stubs. `CopilotToolsService` persists `ValuationSnapshot`, `ToolEvent`, `PredictionLog`, and `ShadowLog`, then composes higher-order results.
3. The React intelligence layer depends on a property-context bridge after direct valuation. That bridge calls protected Copilot persistence endpoints, so it will fail without a bearer token.
4. Direct valuation and protected tool valuation are separate lifecycle paths. A direct valuation result does not automatically create the backend `ValuationSnapshot` required by later explainability/market/Copilot flows.
5. Market insight is descriptive over persisted protected-tool history; it is not an external market intelligence feed.
6. Broker tooling is real on the backend, but the active React payload does not satisfy the backend schema.

## Tool Audit Verdict

Backend tool maturity is high. Product tool maturity is mixed because the active React client cannot authenticate protected tool calls and cannot satisfy the broker contract. The tool layer should be described as implemented but not fully productized end to end.
