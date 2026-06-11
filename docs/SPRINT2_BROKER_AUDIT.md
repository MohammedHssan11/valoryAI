# Sprint 2 Broker Contract Audit

Audit date: 2026-06-11

## Backend Contract Source

Authoritative backend files:

- `pf_scraper/fair-price-eg/backend/app/api/routes/broker.py`
- `pf_scraper/fair-price-eg/backend/app/broker/schemas/contracts.py`
- `pf_scraper/fair-price-eg/backend/app/broker/sessions/state.py`

## Protected Broker Routes

The active backend Broker routes are protected by `get_authenticated_user`.

| Route | Backend request model | Response shape | Sprint 2 status |
| --- | --- | --- | --- |
| `POST /v1/broker/reason` | `BrokerReasonRequest` | `SuccessResponse[BrokerOrchestrationResponse]` | Aligned from React |
| `POST /v1/broker/chat` | `BrokerChatRequest` | `SuccessResponse[BrokerOrchestrationResponse]` | Aligned from React |
| `POST /v1/broker/stream` | `BrokerReasonRequest` | SSE events plus raw final `BrokerOrchestrationResponse` | Aligned from React |

`POST /v1/broker/analyze`, `POST /v1/broker/intent`, and `GET /v1/broker/session/{session_id}` exist, but the Sprint 2 mismatch was on reason/chat/stream.

## Required Request Fields

`BrokerChatRequest` and `BrokerReasonRequest` require:

- `workspace_id`: integer, `gt=0`
- `scenario_id`: integer, `gt=0`
- `message`: string, `min_length=1`, `max_length=4000`

Optional fields:

- `session_id`: nullable string, `min_length=3`, `max_length=80`
- `valuation_request`: nullable `RentFairPriceRequest`
- `investor_preferences`: nullable object

`InvestorPreferences` forbids extra fields and validates:

- `risk_tolerance`: nullable string, max length 80
- `investment_horizon`: nullable string, max length 80
- `target_yield`: nullable float, `0 <= value <= 1`
- `budget_ceiling_egp`: nullable integer, `gt=0`
- `notes`: list of strings, max 20 items

## Runtime Requirements

The backend binds every Broker request to a user-scoped session through `session_store.get_or_create`.

Runtime requirements:

- Authenticated user must be present.
- `workspace_id` must belong to that user.
- `scenario_id` must belong to that workspace and user.
- Reused `session_id` must match the same user/workspace/scenario tuple.

## Frontend Alignment Implemented

Frontend files now enforce and provide the backend contract:

- `frontend/src/types/broker.ts`: `BrokerReasonRequest` and `BrokerChatRequest` require `workspace_id` and `scenario_id`.
- `frontend/src/services/brokerService.ts`: validates positive ids, message length, session id length, and serializes only backend-accepted request fields.
- `frontend/src/store/brokerStore.ts`: resolves active workspace/property/scenario and creates a baseline scenario through existing scenario APIs when none is active.
- `frontend/src/features/broker/BrokerScreen.tsx`: builds Broker payloads from resolved backend context before streaming or fallback reason execution.
- `frontend/src/store/scenarioHistoryStore.ts`: keeps selected/saved/restored scenarios synchronized into the active property context.

## Audit Verdict

P0-2 request-contract mismatch is closed in the React Broker paths covered by Sprint 2. Broker reason, chat, and stream payloads now include `workspace_id` and `scenario_id` and are validated before network execution.
