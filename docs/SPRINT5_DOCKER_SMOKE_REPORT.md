# Sprint 5 Docker Smoke Report

Date: 2026-06-11

## Commands Executed

- `docker --version`
- `docker compose version`
- `docker compose config --quiet`
- `docker compose up -d --build`
- `BACKEND_PORT=18000 FRONTEND_PORT=13000 docker compose up -d --build backend frontend`
- `docker compose ps -a`
- `docker compose exec -T backend python -m app.scripts.run_migrations --verify`
- `docker compose --profile staging run --rm staging-smoke`
- `docker compose exec -T db psql -U fairprice -d fairprice -tAc "SELECT PostGIS_Version(); SELECT COUNT(*) FROM listings; SELECT COUNT(*) FROM areas;"`

## Docker Availability

| Check | Result |
| --- | --- |
| Docker CLI | PASS, Docker `28.5.1` |
| Compose CLI | PASS, Docker Compose `v2.40.0-desktop.1` |
| Docker daemon | Initially unavailable, PASS after Docker Desktop startup |
| Compose config | PASS |

## Startup Result

Default `docker compose up -d --build` built all images and completed bootstrap, but backend host bind failed:

- `Bind for 0.0.0.0:8000 failed: port is already allocated`
- Owning Docker container: `college-decision-support-system-backend-1`

Certification stack was rerun without stopping unrelated user containers:

- `BACKEND_PORT=18000`
- `FRONTEND_PORT=13000`

## Container Health

| Container | Status |
| --- | --- |
| `fair-price-eg-db-1` | Up, healthy |
| `fair-price-eg-db-bootstrap-1` | Exited `0` |
| `fair-price-eg-backend-1` | Up, healthy, `18000->8000` |
| `fair-price-eg-frontend-1` | Up, healthy, `13000->80` |

## Bootstrap Evidence

`db-bootstrap` output:

- Migrations completed.
- Staging rows loaded: `62608`.
- Area nodes upserted: `3104`.
- Listing category counts:
  - buy sale: `19915`
  - commercial buy sale: `8776`
  - commercial rent monthly: `13938`
  - rent monthly: `19979`
- Orphan area refs: `0`
- Planner statistics refreshed.

## Health Endpoint Evidence

| URL | Status | Time |
| --- | --- | --- |
| `http://localhost:18000/health` | 200 | 210.22 ms |
| `http://localhost:18000/health/ready` | 200 | 31.49 ms |
| `http://localhost:13000/health` | 200 | 37.25 ms |
| `http://localhost:13000/health/ready` | 200 | 32.73 ms |
| `http://localhost:13000/` | 200 | 25.74 ms |

## Staging Smoke

`docker compose --profile staging run --rm staging-smoke` returned:

- `ok: true`
- readiness: 200
- openapi: 200
- valuation: 200
- invalid payload: 422 with `INVALID_COORDINATES`
- metrics: 200
- operational status: `ok`

## Migration And PostGIS Checks

- Migration verification: PASS.
- PostGIS version: `3.4 USE_GEOS=1 USE_PROJ=1 USE_STATS=1`.
- Listings count: `62608`.
- Areas count: `3104`.

## Docker Smoke Verdict

PASS WITH RISKS.

The full stack runs and health checks pass. The only Docker smoke risk is local host port collision on `8000`; alternate host ports were required for this workstation.
