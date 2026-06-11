# Final Integration Audit

Audit date: 2026-06-10

## End-To-End Integration Paths

| Path | Expected Flow | Actual Source Finding | Status |
| --- | --- | --- | --- |
| React direct valuation | React form -> `/v1/valuation/fair-price` -> valuation result | Public endpoint and React service exist. | Works structurally. |
| React valuation to property context | Direct valuation result -> create/list workspace/property/tool event | Calls protected `/v1/copilot/*` without a bearer token. | Blocked. |
| React what-if | Active property context -> `/v1/copilot/tools/what-if` | UI/backend exist; `canRun = hasContext && hasChanges`. Missing auth prevents context. | Blocked in real web session. |
| React negotiation | Active property context -> `/v1/copilot/tools/negotiation` | UI/backend exist; protected request cannot authenticate. | Blocked. |
| React investment | Active property context -> `/v1/copilot/tools/investment` | UI/backend exist; protected request cannot authenticate. | Blocked. |
| React market insight | Workspace -> `/v1/copilot/tools/market-insight` | Backend reads snapshots/events; React cannot authenticate and direct valuation does not seed snapshots. | Blocked/sparse. |
| React Copilot drawer | Prompt + workspace + tool inputs -> `/v1/copilot/orchestrator/respond` | Backend runtime real; React requires active workspace and auth. | Blocked. |
| React broker | Broker UI -> `/v1/broker/stream` or `/v1/broker/reason` | Missing auth and missing `workspace_id`/`scenario_id`. | Blocked. |
| Flutter auth | Firebase user -> `/v1/auth/token-exchange` -> bearer JWT | Implemented. | Works structurally. |
| Flutter Copilot | Workspace context -> protected orchestrator | Implemented and covered by tests. | Works structurally. |

## Deployment Integration

| Integration | Finding |
| --- | --- |
| Docker Compose | Backend and frontend are containerized. |
| Frontend Nginx | Proxies `/v1/`, `/health`, and `/health/ready` to backend. This is coherent for same-origin API calls. |
| Backend production secrets | Production expects `JWT_SECRET`, Firebase config, database settings, and optional LLM/provider settings. |
| Auth | Backend and mobile agree on Firebase token exchange -> ValorAI JWT. React does not implement this. |
| Postgres/PostGIS | Backend tests and code expect PostGIS-capable behavior for some integration paths. Some root tests execute Postgres SQL during collection against SQLite. |
| Optional Gemini narration | Copilot narration is gated and default-off unless settings and allowlist are configured. |

## External/System Integrations

| Integration | Role | Status |
| --- | --- | --- |
| Firebase Auth | Client identity and token exchange. | Backend/mobile integrated; React missing. |
| Postgres/PostGIS | Spatial search, persistence, broker/Copilot state. | Core backend dependency. |
| Google Maps/geocoding style inputs | Location-oriented valuation UX/data. | Present in clients/data model surfaces. |
| CatBoost/model artifacts | Valuation/shadow model support. | Present in backend model pipeline context. |
| H3/spatial tooling | Spatial valuation features. | Present in backend dependencies/context. |
| Gemini/LLM provider | Optional Copilot narration. | Guarded, default-off. |

## Integration Verdict

The backend integration architecture is credible, but the active React product is not end-to-end integrated. The most important system break is not UI absence; it is authentication and request-contract alignment between the web client and the protected backend.
