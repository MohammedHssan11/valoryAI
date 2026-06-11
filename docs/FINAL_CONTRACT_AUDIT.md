# Final Contract Audit

Audit date: 2026-06-10

## Contract Summary

The backend has coherent internal schemas, but the active React frontend is not aligned with two critical runtime contracts: authentication and broker request shape.

## Endpoint Contract Matrix

| Contract | Backend | React Client | Status |
| --- | --- | --- | --- |
| Public valuation | `POST /v1/valuation/fair-price`, success envelope. Evidence: `backend/app/api/routes/pricing.py:17`. | Calls `/v1/valuation/fair-price`. | Aligned. |
| Copilot tools auth | Protected through `get_authenticated_user`. Evidence: `backend/app/api/routes/copilot_tools.py:24-36`. | Axios client only adds request/correlation IDs. Evidence: `frontend/src/api/http.ts:69-71`. | Not aligned. |
| Copilot persistence auth | Protected through `get_authenticated_user`. Evidence: `backend/app/api/routes/copilot.py:30,42,57`. | Property bridge uses these endpoints but no bearer token is available. | Not aligned. |
| Copilot orchestrator auth | Protected. Evidence: `backend/app/api/routes/copilot_orchestrator.py:35`. | Copilot service/store require workspace context but cannot authenticate from React. | Not aligned. |
| Broker auth | Protected. Evidence: `backend/app/api/routes/broker.py:63,81,93,109,124,224`. | Broker service uses same unauthenticated Axios client. | Not aligned. |
| Broker request shape | Requires `workspace_id` and `scenario_id`. Evidence: `backend/app/broker/schemas/contracts.py:97-108`. | `BrokerReasonRequest` has `session_id`, `message`, `valuation_request`, `investor_preferences` only. Evidence: `frontend/src/types/broker.ts:68-72`. | Not aligned. |
| Broker screen payload | Backend requires workspace/scenario. | `buildRequest` sends `session_id`, `message`, `valuation_request`. Evidence: `frontend/src/features/broker/BrokerScreen.tsx:676`. | Not aligned. |
| Mobile auth | Backend expects bearer JWT. | Flutter attaches bearer token and renews on auth errors. Evidence: `flutter_valorai/lib/core/network/auth_interceptor.dart:12-36`. | Aligned. |

## P0 Contract Failures

### P0-1: React Protected API Authentication Missing

Impact: Every protected React workflow will receive 401 in a real browser session unless another layer injects auth externally. This affects property context, scenario history, what-if, negotiation, investment, market insight, Copilot orchestrator, and broker.

Evidence:

- Backend protected tools import and depend on `get_authenticated_user`: `backend/app/api/routes/copilot_tools.py:24-36`.
- React HTTP client sets trace headers but no `Authorization`: `frontend/src/api/http.ts:69-71`.
- No React source path provides a token exchange/login flow comparable to Flutter.

Required fix:

Implement web authentication: Firebase sign-in or equivalent, `/v1/auth/token-exchange`, secure token storage, refresh/expiry handling, Axios `Authorization: Bearer <ValorAI JWT>` injection, route guards, and integration tests that hit protected endpoint contracts.

### P0-2: Broker React Payload Does Not Match Backend Schema

Impact: Broker `/v1/broker/stream` and `/v1/broker/reason` will 422 even after auth is fixed.

Evidence:

- Backend `BrokerChatRequest` requires `workspace_id` and `scenario_id`: `backend/app/broker/schemas/contracts.py:97-108`.
- Frontend `BrokerReasonRequest` omits both fields: `frontend/src/types/broker.ts:68-72`.
- Frontend `buildRequest` only sends `session_id`, `message`, and optional valuation request: `frontend/src/features/broker/BrokerScreen.tsx:676`.

Required fix:

Either align React with backend by creating/selecting workspace and scenario before broker execution, or relax the backend schema and have the broker create/bind context from valuation input. The current split is not runtime-compatible.

## P1 Contract Risks

| Risk | Impact | Fix |
| --- | --- | --- |
| Direct valuation does not persist `ValuationSnapshot` | Copilot explainability/market flows cannot reference direct valuation IDs. | Make direct valuation optionally persist under an authenticated workspace, or immediately run protected valuation tool after bridge succeeds. |
| Mixed raw responses and success envelopes | Clients need tolerant parsing and contract drift is easier. | Standardize tool endpoints to a documented envelope or generate typed clients from OpenAPI. |
| Frontend tests validate mocked contracts | Broker tests can pass while production payloads fail. | Add contract tests against generated backend schemas or OpenAPI snapshots. |
| Market insight requires protected-tool history | Direct valuation-only users see little or no market intelligence. | Unify valuation persistence and market data ingestion. |

## Contract Audit Verdict

Direct valuation is contract-aligned. Flutter authentication is contract-aligned. The active React intelligence product is not contract-complete because protected endpoints lack web auth and broker request schemas are mismatched.
