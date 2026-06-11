# Sprint 6 Deployment Certification

Date: 2026-06-11

## Deployment Surface

Reviewed:

- `pf_scraper/fair-price-eg/docker-compose.yml`
- `pf_scraper/fair-price-eg/backend/Dockerfile`
- `pf_scraper/fair-price-eg/frontend/Dockerfile`
- `pf_scraper/fair-price-eg/frontend/nginx.conf`
- `pf_scraper/fair-price-eg/.env.example`
- `pf_scraper/fair-price-eg/frontend/.env.example`
- Migration/bootstrap scripts under `backend/app/scripts`

## Compose Contract

`docker compose --env-file .env.example config` passed.

Confirmed resolved configuration includes:

- PostGIS image `postgis/postgis:16-3.4`.
- `db` healthcheck via `pg_isready`.
- `db-bootstrap` waits for healthy DB and runs migrations plus CSV load.
- `backend` waits for DB and bootstrap, then healthchecks `/health/ready`.
- `frontend` waits for backend health.
- Frontend build args include required Firebase web values:
  - `VITE_FIREBASE_API_KEY`
  - `VITE_FIREBASE_AUTH_DOMAIN`
  - `VITE_FIREBASE_PROJECT_ID`
  - `VITE_FIREBASE_APP_ID`
  - optional storage/messaging/measurement values.

## Build Certification

Command:

```powershell
docker compose --env-file .env.example build
```

Result:

- `fair-price-eg-backend` built.
- `fair-price-eg-db-bootstrap` built.
- `fair-price-eg-frontend` built.
- Frontend Vite build completed with the known chunk warning.

## Fresh Stack Smoke

Disposable project:

- Compose project: `valorai-sprint6`
- Backend port: `18080`
- Frontend/nginx port: `13080`
- Postgres port: `15480`

Command:

```powershell
docker compose --env-file .env.example -p valorai-sprint6 up -d --wait
```

Result:

- DB container healthy.
- DB bootstrap container exited successfully.
- Backend container healthy.
- Frontend container healthy.

Bootstrap evidence:

- Migrations applied successfully.
- Loaded staging rows: 62608.
- Upserted area nodes: 3104.
- Orphan area refs: 0.
- Planner statistics refreshed.
- DONE.

HTTP smoke:

- `http://127.0.0.1:18080/health`: success true, status ok.
- `http://127.0.0.1:18080/health/ready`: success true, database ok.
- `http://127.0.0.1:13080/health`: success true, status ok.
- `http://127.0.0.1:13080/health/ready`: success true, database ok.
- `http://127.0.0.1:13080/`: HTTP 200, content length 1662, nginx security headers present.
- `http://127.0.0.1:13080/v1/copilot/users/me`: HTTP 200 with generated ValorAI JWT.

Staging smoke:

```powershell
docker compose --env-file .env.example -p valorai-sprint6 --profile staging run --rm staging-smoke
```

Result: `ok: true`.

Checks passed:

- readiness: 200
- openapi: 200
- valuation: 200
- invalid payload: 422 with `INVALID_COORDINATES`
- metrics: 200
- operational: 200, status ok

## Teardown

Command:

```powershell
docker compose -p valorai-sprint6 down -v
```

Result:

- Containers removed.
- Network removed.
- Disposable volume removed.
- `docker compose -p valorai-sprint6 ps` showed no remaining services.

## Deployment Certification Result

PASS FOR PILOT.

Production caveat: real Firebase production/staging credentials must be supplied by the deployment environment and live browser Firebase login should be smoke-tested there.

