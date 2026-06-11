# Final V2 Contract Audit

Audit date: 2026-06-11

## Contract Matrix

| Contract | Backend source truth | React source truth | Flutter source truth | Status |
| --- | --- | --- | --- | --- |
| Auth token exchange | `/v1/auth/token-exchange` verifies Firebase ID token, provisions user, returns ValorAI JWT. | `exchangeFirebaseToken` posts `{ firebase_id_token }`; session manager stores JWT and metadata. | Auth remote data source posts same shape. | Aligned. |
| Bearer auth | Protected routes use `HTTPBearer` and `get_authenticated_user`. | Axios interceptor adds `Authorization`; refreshes once after 401. Broker SSE adds bearer manually. | Dio interceptor adds bearer and renews on 401. | Aligned in source. |
| Protected routes | Broker, Copilot persistence, tools, and orchestrator depend on authenticated user. | App routes are under `ProtectedRoute`; unauthenticated users go to `/login`. | Mobile auth/session manager protects authenticated Dio usage. | Aligned. |
| Public valuation | `/v1/valuation/fair-price` returns `SuccessResponse[RentFairPriceResponse]`. | Valuation service accepts enveloped or raw response and sends auth when present. | Valuation data source expects success envelope `data`. | Aligned. |
| Broker request | Backend `BrokerChatRequest` and `BrokerReasonRequest` require `workspace_id`, `scenario_id`, and `message`. | Types and payload builder require/validate positive `workspace_id` and `scenario_id`. | Not primary. | Aligned. |
| Broker stream | Backend accepts POST SSE `BrokerReasonRequest`; protected. | `streamBrokerReason` POSTs aligned payload and bearer token. | Not primary. | Aligned. |
| Copilot tools | Backend request schemas require workspace/property/scenario as appropriate. | Services validate positive IDs and response shape. | No full parity. | Aligned for React. |
| Scenario contracts | Backend scenarios attach to property/workspace; lineage/tree endpoints exist. | Scenario history service/store validates IDs and synchronizes selected scenario into property context. | Not full parity. | Aligned for React. |
| Workspace/property contracts | Backend returns raw Pydantic response models, not success envelopes. | React services tolerate raw or success envelopes. | Flutter workspace data source expects raw lists/maps. | Aligned with current backend. |
| Copilot orchestrator | Backend request requires `workspace_id`, message, `tool_inputs`, optional scenario/broker session. | React validates and sends current workspace/scenario/tool inputs. | Flutter sends workspace context and tool inputs. | Aligned. |

## Fixed Since Final V1

- React authentication is now implemented: Firebase client, auth provider, session manager, token exchange, route guard, Axios bearer injection, 401 retry.
- Broker contract mismatch is fixed: React types and service payloads now include backend-required `workspace_id` and `scenario_id`.
- Backend default test contract drift is fixed: collection and runtime tests pass.

## Current Contract Risks

| Severity | Contract risk | Evidence |
| --- | --- | --- |
| P0 | Dockerized React auth config is incomplete. | React requires `VITE_FIREBASE_*` values in `src/core/config.ts` and rejects missing config in `src/auth/firebaseClient.ts`. `frontend/Dockerfile` declares only `VITE_API_BASE_URL` and `VITE_APP_ENV`; `docker-compose.yml` passes only those two build args. |
| P1 | Direct valuation does not issue a protected `valuation_id` or `ValuationSnapshot`. | Public valuation route returns `RentFairPriceResponse`; protected valuation snapshot creation happens only inside `CopilotToolsService.execute_valuation`. |
| P2 | Mixed response styles remain. | Pricing/health/broker use success envelopes; Copilot persistence, Copilot tools, and orchestrator return raw response models. React handles both, but generated-client safety is weaker. |
| P2 | Mobile workspace parsing expects current raw persistence shape only. | Flutter workspace data source reads raw lists/maps from `/v1/copilot/workspaces`; it would need updates if persistence endpoints move to envelopes. |

## Contract Verdict

Core source contracts are now aligned across backend, React, and Flutter for auth, broker, protected tools, and Copilot. The biggest remaining contract issue is deployment-time: the Docker frontend build contract does not provide the Firebase values required by the React auth contract.
