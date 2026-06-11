# Sprint 1 Integration Verification

Verification date: 2026-06-10

## Protected Endpoint Coverage

React now uses shared authenticated transports for protected endpoints.

Axios-protected services:

- `GET /v1/copilot/workspaces`
- `POST /v1/copilot/workspaces`
- `GET /v1/copilot/workspaces/{workspace_id}/properties`
- `POST /v1/copilot/properties`
- `POST /v1/copilot/tool-events`
- Scenario history endpoints under `/v1/copilot/scenarios*`
- `POST /v1/copilot/tools/what-if`
- `POST /v1/copilot/tools/negotiation`
- `POST /v1/copilot/tools/investment`
- `POST /v1/copilot/tools/market-insight`
- `POST /v1/copilot/orchestrator/respond`
- `POST /v1/broker/reason`
- `POST /v1/broker/chat`

Fetch/SSE-protected service:

- `POST /v1/broker/stream`

## Required Endpoint Verification

| Endpoint | React caller | Auth result |
| --- | --- | --- |
| `GET /v1/copilot/workspaces` | `propertyContextService.ts` | Covered by Axios auth interceptor. |
| `POST /v1/copilot/tools/what-if` | `whatIfService.ts` | Covered by Axios auth interceptor. |
| `POST /v1/copilot/tools/negotiation` | `negotiationService.ts` | Covered by Axios auth interceptor. |
| `POST /v1/copilot/tools/investment` | `investmentService.ts` | Covered by Axios auth interceptor. |
| `POST /v1/copilot/tools/market-insight` | `marketInsightService.ts` | Covered by Axios auth interceptor. |
| `POST /v1/copilot/orchestrator/respond` | `copilotService.ts` | Covered by Axios auth interceptor. |
| Broker endpoints | `brokerService.ts` | `reason`/`chat` covered by Axios; `stream` covered by explicit fetch bearer injection. |

## Bearer Header Verification

Automated tests verify:

- Axios requests receive `Authorization: Bearer stored-jwt`.
- Axios retries a 401 with `Authorization: Bearer fresh-jwt`.
- Broker stream fetch receives `Authorization: Bearer stream-jwt`.

Test files:

- `frontend/src/api/httpAuth.test.ts`
- `frontend/src/services/brokerService.test.ts`

## Session Verification

Automated tests verify:

- Stored unexpired ValorAI JWT restores an authenticated session.
- Expired stored JWT renews through the active Firebase user.
- Sign-in stores the exchanged ValorAI session.
- Logout clears browser session storage and signs out from Firebase.
- Anonymous users are redirected to login.
- Restored authenticated users can enter protected routes.

Test files:

- `frontend/src/auth/authSessionManager.test.ts`
- `frontend/src/auth/tokenExchange.test.ts`
- `frontend/src/features/auth/ProtectedRoute.test.tsx`

## Commands Run

From `pf_scraper/fair-price-eg/frontend`:

```text
npm run lint
npm test
npm run build
```

Results:

- TypeScript typecheck: passed.
- Vitest suite: 34 test files passed, 134 tests passed.
- Vite production build: passed.
- Build warning: Vite reports one generated JS chunk larger than 500 kB after minification. This is a pre-existing bundle-size class of warning and does not block P0-1 auth closure.

## Browser Smoke

Local dev server:

```text
http://localhost:3000/
```

Smoke result:

- `/` redirected to `/login`.
- Login form rendered.
- Missing Firebase configuration state rendered when `VITE_FIREBASE_*` values are absent.
- Sign-in button was disabled until Firebase web configuration is supplied.

## Integration Verdict

No React service bypasses auth for protected APIs. All normal protected service calls go through the authenticated Axios client, and the only direct `fetch` protected path, broker SSE streaming, now injects the same ValorAI bearer token and performs the same one-time 401 recovery behavior.
