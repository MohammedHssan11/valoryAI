# Sprint 5 Deployment Contract Audit

Date: 2026-06-11

## Backend Contract

| Requirement | Source | Provided by Compose | Result |
| --- | --- | --- | --- |
| `JWT_SECRET` | `backend/app/core/config.py` | `${JWT_SECRET:?JWT_SECRET must be configured}` | PASS |
| `DATABASE_URL` | `backend/app/core/config.py` | `postgresql+psycopg://...@db:5432/...` | PASS |
| `FIREBASE_PROJECT_ID` | `backend/app/core/config.py`, `firebase_auth.py` | `${FIREBASE_PROJECT_ID:?FIREBASE_PROJECT_ID must be configured}` | PASS |
| JWT issuer/audience | `backend/app/core/auth.py` | defaults or env | PASS |
| Narration settings | `backend/app/core/config.py` | optional env passthrough | PASS |

Backend production safety validators:

- `DEBUG` cannot be true in production.
- Default local `JWT_SECRET` is rejected in staging/production.
- Wildcard CORS is rejected in staging/production.
- Copilot narration requires explicit allowed intents, API key, and governance acknowledgement.

## Frontend Contract

| Requirement | Source | Provided by Compose/Dockerfile | Result |
| --- | --- | --- | --- |
| `VITE_API_BASE_URL` | `frontend/src/core/config.ts` | Compose build arg `"/"` | PASS |
| `VITE_FIREBASE_API_KEY` | `frontend/src/core/config.ts`, `firebaseClient.ts` | Not passed through Dockerfile or Compose | FAIL |
| `VITE_FIREBASE_AUTH_DOMAIN` | `frontend/src/core/config.ts`, `firebaseClient.ts` | Not passed through Dockerfile or Compose | FAIL |
| `VITE_FIREBASE_PROJECT_ID` | `frontend/src/core/config.ts`, `firebaseClient.ts` | Not passed through Dockerfile or Compose | FAIL |
| `VITE_FIREBASE_APP_ID` | `frontend/src/core/config.ts`, `firebaseClient.ts` | Not passed through Dockerfile or Compose | FAIL |

Observed browser evidence:

- URL redirected to `http://localhost:13000/login`.
- Login screen displayed: `Firebase web configuration is missing. Add the VITE_FIREBASE_* values before signing in.`
- `SIGN IN` button was disabled.
- Screenshot: `C:\Users\mh978\Downloads\mobile computing project\reports\sprint5_frontend_login_state.png`

## Environment File Findings

Root `.env` and `backend/.env` contain backend keys as set values.

Frontend `.env.example` documents Firebase web variables but leaves them empty:

- `VITE_FIREBASE_API_KEY=`
- `VITE_FIREBASE_AUTH_DOMAIN=`
- `VITE_FIREBASE_PROJECT_ID=`
- `VITE_FIREBASE_APP_ID=`

Root `.env.example` contains duplicate `FIREBASE_PROJECT_ID` entries, one placeholder and one concrete-looking value. This is not a runtime blocker because actual `.env` resolves to a set value, but it is a contract hygiene risk.

## Contract Verdict

FAIL.

The backend deployment contract is satisfied. The frontend deployment contract is not satisfied because required Firebase web values are not injected into the production Docker build. This blocks live React Login -> Firebase -> Token Exchange certification.
