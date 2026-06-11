# Sprint 5 End-to-End Certification

Date: 2026-06-11

## Execution Context

API journeys were executed against:

- Backend: `http://localhost:18000`
- Frontend/nginx: `http://localhost:13000`
- Database: Docker PostGIS service

Browser login was blocked by missing Firebase web config, so authenticated business journeys were certified through protected backend APIs using a ValorAI JWT minted by the running backend. This validates API integration and authorization but does not certify real React Firebase login.

## Shared Test State

Created through live API:

- User id: `589`
- Workspace id: `533`
- Property id: `606`
- Scenario id: `349`
- Baseline valuation id: `val_1640a08ddfd142af8872dc0b95424d12`

Valuation payload:

- Property: Mivida apartment
- Coordinates: `30.00575065612793`, `31.533998489379883`
- Size: `220 sqm`
- Bedrooms/bathrooms: `4 / 3`
- Amenities: `BA`, `SE`

## Journey Results

| Journey | Request path | Response path/status | Result | Notes |
| --- | --- | --- | --- | --- |
| A - Login -> Direct Valuation | `POST /v1/valuation/fair-price` | 200 | PASS WITH AUTH RISK | Direct valuation returned `85000 EGP`, confidence `High`, 49 comps. Browser login unavailable. |
| B - Login -> Direct Valuation -> Property Context Bridge | `POST /v1/copilot/workspaces`, `POST /v1/copilot/properties`, `POST /v1/copilot/tools/valuation` | 201, 201, 200 | PASS WITH AUTH RISK | Context-backed valuation persisted a snapshot. |
| C - Login -> Valuation -> What-if | `POST /v1/copilot/tools/what-if` | 200 | PASS WITH AUTH RISK | Scenario valuation returned with `High` confidence. |
| D - Login -> Valuation -> Scenario Save | `POST /v1/copilot/scenarios` | 201 | PASS WITH AUTH RISK | Scenario `349` created. |
| E - Login -> Scenario Restore | `DELETE /v1/copilot/scenarios/349`, `POST /v1/copilot/scenarios/349/restore` | 200, 200 | PASS WITH AUTH RISK | Deleted scenario restored successfully. |
| F - Login -> Negotiation Intelligence | `POST /v1/copilot/tools/negotiation` | 200 | PASS WITH AUTH RISK | Position: `Premium Justified`. |
| G - Login -> Investment Intelligence | `POST /v1/copilot/tools/investment` | 200 | PASS WITH AUTH RISK | Position: `Caution`. |
| H - Login -> Market Intelligence | `POST /v1/copilot/tools/market-insight` | 200 | PASS WITH AUTH RISK | Volume: `6` persisted valuations. |
| I - Login -> Copilot | `POST /v1/copilot/orchestrator/respond` | 200 | PASS WITH AUTH RISK | Intent: `INVESTMENT`; delivery: `DETERMINISTIC_FALLBACK`. |
| J - Login -> Broker Reason | `POST /v1/broker/reason` | 200 | PASS WITH AUTH RISK | Grounding passed; degraded mode false. |
| K - Login -> Broker Chat | `POST /v1/broker/chat` | 200 | PASS WITH AUTH RISK | Reused broker session; grounding passed. |
| L - Login -> Broker Stream | `POST /v1/broker/stream` | 200 | PASS WITH AUTH RISK | 46 SSE events; final response event present. |

## Blocking Conditions

Primary blocker:

- Docker production frontend login is disabled because Firebase web configuration is missing.
- Screenshot: `C:\Users\mh978\Downloads\mobile computing project\reports\sprint5_frontend_login_state.png`

Secondary conditions:

- Default host port `8000` was occupied by an unrelated Docker project. Certification used `BACKEND_PORT=18000`.

## E2E Certification Verdict

PASS WITH RISKS for protected API journeys.

FAIL for full browser E2E because Login -> Firebase cannot be completed from the current Docker frontend artifact.
