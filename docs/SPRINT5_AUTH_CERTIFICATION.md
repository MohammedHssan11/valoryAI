# Sprint 5 Authentication Certification

Date: 2026-06-11

## Scope

Required flow:

React Login -> Firebase -> Token Exchange -> ValorAI JWT -> Protected API

## Backend Auth Evidence

Backend implementation:

- Token exchange: `POST /v1/auth/token-exchange`
- Firebase verifier: `backend/app/core/firebase_auth.py`
- ValorAI JWT creation and verification: `backend/app/core/auth.py`
- Protected route dependency: `get_authenticated_user`

Automated test evidence:

- Backend suite: `205 passed, 9 skipped`
- Includes auth exchange and protected API tests.

Live protected API evidence:

| Check | Path | Status | Result |
| --- | --- | --- | --- |
| Missing bearer | `GET /v1/copilot/users/me` | 401 | PASS |
| Invalid bearer | `GET /v1/copilot/users/me` | 401 | PASS |
| Valid ValorAI JWT | `GET /v1/copilot/users/me` | 200 | PASS |

Malformed Firebase token exchange timing:

- `POST /v1/auth/token-exchange`
- Statuses: `401, 401, 401`
- Average: `17.15 ms`

## Frontend Auth Evidence

Frontend implementation:

- `frontend/src/auth/firebaseClient.ts`
- `frontend/src/auth/authSessionManager.ts`
- `frontend/src/auth/tokenExchange.ts`
- `frontend/src/auth/AuthProvider.tsx`
- `frontend/src/features/auth/ProtectedRoute.tsx`

Frontend tests:

- `npm run lint`: PASS
- `npm test -- --run`: PASS, `35` files and `144` tests

Browser production artifact evidence:

- Docker-served frontend opened at `http://localhost:13000`.
- App redirected to `http://localhost:13000/login`.
- Login screen displayed: `Firebase web configuration is missing. Add the VITE_FIREBASE_* values before signing in.`
- `SIGN IN` button was disabled.
- Screenshot: `C:\Users\mh978\Downloads\mobile computing project\reports\sprint5_frontend_login_state.png`

## Required Auth Behaviors

| Behavior | Result |
| --- | --- |
| Login | FAIL in Docker production frontend because Firebase web config is missing |
| Firebase ID token verification | PASS in backend tests; not live-certified without real Firebase web credentials |
| Token exchange | PASS in tests; malformed token returns 401 live |
| ValorAI JWT protected API | PASS live |
| Session restore | PASS in frontend unit tests; not live-certified due disabled login |
| Logout | PASS in frontend unit tests; not live-certified due disabled login |
| 401 recovery | PASS in frontend HTTP/auth tests and live protected API 401 checks |
| Protected route access | PASS by redirect to login when unauthenticated; authenticated browser access not live-certified |

## Auth Certification Verdict

FAIL.

Backend authorization works and protected APIs enforce JWTs. The complete required browser auth chain cannot be certified because the production Docker frontend does not receive Firebase web configuration.
