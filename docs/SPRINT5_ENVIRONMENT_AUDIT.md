# Sprint 5 Environment Audit

Date: 2026-06-11

## Scope

Sprint 5 was executed as a production integration certification pass. No product features, UI redesign, agents, LLM features, or business logic changes were made.

## Deployment Architecture

ValorAI production-like deployment is defined by `pf_scraper/fair-price-eg/docker-compose.yml`.

Services:

| Service | Role | Image/build | Exposed host port |
| --- | --- | --- | --- |
| `db` | PostgreSQL/PostGIS datastore | `postgis/postgis:16-3.4` | `${POSTGRES_PORT:-5432}` |
| `db-bootstrap` | One-shot migration and seed/import job | `./backend` | none |
| `backend` | FastAPI API server | `./backend` | `${BACKEND_PORT:-8000}` |
| `frontend` | Vite React static build served by nginx | `./frontend` | `${FRONTEND_PORT:-3000}` |
| `staging-smoke` | Optional staging smoke runner | `./backend`, profile `staging` | none |

Observed production-like run:

| Item | Result |
| --- | --- |
| Compose syntax | PASS, `docker compose config --quiet` |
| Docker engine | PASS after Docker Desktop startup |
| Default backend host port | BLOCKED locally because another Docker project owned `8000` |
| Alternate smoke ports | PASS with `BACKEND_PORT=18000`, `FRONTEND_PORT=13000` |

## Dockerfiles

Backend Dockerfile:

- Base: `python:3.11-slim`
- Installs `requirements.txt`
- Copies `app` into `/app/app`
- Exposes `8000`
- Healthcheck: `GET http://127.0.0.1:8000/health/ready`
- Starts `uvicorn app.main:app --host 0.0.0.0 --port 8000`

Frontend Dockerfile:

- Base build stage: `node:22-alpine`
- Runtime stage: `nginx:1.27-alpine`
- Build args currently present: `VITE_API_BASE_URL`, `VITE_APP_ENV`
- Healthcheck: `GET http://127.0.0.1/`
- Finding: Firebase web build args are not passed through this Dockerfile.

## Nginx

`frontend/nginx.conf` serves the React app and proxies:

- `/v1/` to `http://backend:8000/v1/`
- `/health` to `http://backend:8000/health`
- `/health/ready` to `http://backend:8000/health/ready`

Security headers are configured:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: no-referrer`
- `Permissions-Policy: geolocation=(), microphone=(), camera=()`

## Startup Order

Compose dependency order:

1. `db` starts and must pass `pg_isready -h 127.0.0.1`.
2. `db-bootstrap` waits for healthy `db`, then runs migrations and CSV import.
3. `backend` waits for healthy `db` and successful `db-bootstrap`.
4. `frontend` waits for healthy `backend`.
5. Optional `staging-smoke` waits for healthy `backend`.

Observed bootstrap evidence:

- Migrations completed.
- Listings loaded: `62608`.
- Areas loaded: `3104`.
- Bootstrap exited `0`.

## Required Secrets And Environment Variables

Backend required:

- `JWT_SECRET`
- `DATABASE_URL`
- `FIREBASE_PROJECT_ID`

Backend optional or operational:

- `JWT_ISSUER`
- `JWT_AUDIENCE`
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`
- `CORS_ORIGINS`
- `API_REQUEST_TIMEOUT_SECONDS`
- `MAX_REQUEST_BODY_BYTES`
- `RATE_LIMIT_PER_MINUTE`
- `SLOW_QUERY_MS`
- `SLOW_REQUEST_MS`
- `API_LATENCY_SLO_MS`
- `VALUATION_LATENCY_SLO_MS`
- `COPILOT_NARRATION_ENABLED`
- `COPILOT_NARRATION_INTENTS`
- `COPILOT_GEMINI_API_KEY`
- `COPILOT_GEMINI_DATA_GOVERNANCE_ACKNOWLEDGED`

Frontend required for live Firebase login:

- `VITE_API_BASE_URL`
- `VITE_FIREBASE_API_KEY`
- `VITE_FIREBASE_AUTH_DOMAIN`
- `VITE_FIREBASE_PROJECT_ID`
- `VITE_FIREBASE_APP_ID`

Frontend optional:

- `VITE_FIREBASE_STORAGE_BUCKET`
- `VITE_FIREBASE_MESSAGING_SENDER_ID`
- `VITE_FIREBASE_MEASUREMENT_ID`

## Health Check Paths

- Backend container: `/health/ready`
- Frontend container: `/`
- API liveness: `/health`
- API readiness: `/health/ready`
- Runtime metrics: `/health/metrics`
- Operational SLO snapshot: `/health/operational`

## Deployment Assumptions

- A managed secret source injects `JWT_SECRET` and Firebase settings before production/staging build.
- Frontend Firebase web values must be available at build time because Vite embeds `VITE_*` values into static assets.
- The host must reserve ports or override `BACKEND_PORT` and `FRONTEND_PORT`.
- PostGIS volume is persistent via `db_data`.
- `./data` is mounted read-only for bootstrap import.

## Environment Audit Verdict

PASS WITH RISKS.

The runtime architecture is coherent and the stack can run. The major environment risk is that the current Docker frontend build path does not inject Firebase web configuration, which blocks browser login certification.
