# ValorAI Staging Runbook

This runbook is for operating the staging-grade ValorAI stack with Docker Compose, seeded PostgreSQL/PostGIS data, deterministic valuation APIs, frontend integration, and lightweight observability.

## Environment Setup

1. Create a staging env file from the example:

```powershell
Copy-Item .env.staging.example .env
```

2. Set shared-staging secrets before using a non-local environment:

```text
POSTGRES_PASSWORD
CORS_ORIGINS
```

Use `APP_ENV=staging`, `DEBUG=false`, and `LOG_JSON=true` for staging. Do not use wildcard CORS origins in staging or production.

## Startup Sequence

The normal startup order is:

1. `db` starts PostgreSQL/PostGIS.
2. `db` healthcheck waits for `pg_isready`.
3. `db-bootstrap` loads deterministic seed data from `./data`.
4. `backend` waits for DB and completed bootstrap.
5. `frontend` waits for backend readiness.

Start the stack:

```powershell
docker compose up --build -d
```

Run the staging smoke profile:

```powershell
docker compose --profile staging up --build staging-smoke
```

Stop the stack:

```powershell
docker compose down
```

Reset seeded data from scratch:

```powershell
docker compose down -v
docker compose up --build -d
```

## Health Checks

Backend liveness:

```powershell
curl.exe -s http://localhost:8000/health
```

Backend readiness, including DB reachability:

```powershell
curl.exe -s http://localhost:8000/health/ready
```

Lightweight metrics snapshot:

```powershell
curl.exe -s http://localhost:8000/health/metrics
```

Operational SLO summary:

```powershell
curl.exe -s http://localhost:8000/health/operational
```

OpenAPI:

```powershell
curl.exe -s http://localhost:8000/openapi.json
```

## Integration Tests

Run the normal backend suite:

```powershell
cd backend
python -m pytest app\tests
```

Run seeded PostGIS integration tests against the Compose database:

```powershell
$env:RUN_POSTGIS_INTEGRATION='1'
$env:DATABASE_URL='postgresql+psycopg://fairprice:fairprice@localhost:5432/fairprice'
python -m pytest app\tests\test_postgis_integration.py
```

Run frontend checks:

```powershell
cd frontend
npm run lint
npm test
npm run build
npm run clean
```

## Performance Baseline

Collect backend and proxied frontend latency baselines:

```powershell
cd backend
python -m app.scripts.performance_baseline --base-url http://localhost:8000 --frontend-url http://localhost:3000 --iterations 30 --concurrency 4 --max-p95-ms 1500
```

The report includes:

- valuation endpoint roundtrip p50, p95, p99
- deterministic response fingerprint consistency
- frontend HTML and proxied API timing
- runtime metric histograms
- operational SLO checks

## Query Plan Audit

Audit PostGIS comparable retrieval plans:

```powershell
cd backend
$env:DATABASE_URL='postgresql+psycopg://fairprice:fairprice@localhost:5432/fairprice'
python -m app.scripts.query_plan_audit
```

Review `execution_time_ms`, `indexes`, and `node_types`. The expected healthy path uses the existing area/listing indexes and PostGIS geography checks without changing tier ordering.

## Failure Recovery

DB unavailable:

- `/health/ready` returns `503` with `DATABASE_UNAVAILABLE`.
- Backend startup retries according to `DB_STARTUP_RETRIES` and `DB_STARTUP_RETRY_SECONDS`.
- Recovery: restart DB, then restart backend if it exhausted retries.

Backend restart:

- Frontend requests should retry or render a traceable API error.
- Recovery: `docker compose restart backend`.

Frontend reconnect:

- React Query uses online network mode and refetch-on-reconnect for queries.
- Valuation mutations are cancellable and surface request IDs on errors.

Timeouts:

- Requests beyond `API_REQUEST_TIMEOUT_SECONDS` return `504 REQUEST_TIMEOUT`.
- Slow requests appear in `/health/operational`.

Oversized requests:

- Requests above `MAX_REQUEST_BODY_BYTES` return `413 REQUEST_TOO_LARGE`.

Invalid payloads:

- Validation errors return the standard error envelope and preserve `X-Request-ID`.

Rate limiting:

- Protected paths return `429 RATE_LIMIT_EXCEEDED` with `Retry-After`.
- This is in-process by design for staging and single-instance deployments.

## Debugging Workflow

1. Capture the frontend-displayed request ID or trace header.
2. Check backend logs for the same `request_id` or `correlation_id`.
3. Read `/health/operational` for recent valuation, slow request, and slow query summaries.
4. Read `/health/metrics` for raw latency histograms and confidence/tier counters.
5. Run `staging_smoke.py` to verify envelopes, valuation, invalid payload handling, metrics, and OpenAPI.
6. Run `query_plan_audit.py` if comparable retrieval latency regresses.

## Staging SLO Defaults

Default staging thresholds:

- API endpoint p95: `API_LATENCY_SLO_MS=1200`
- Valuation p95: `VALUATION_LATENCY_SLO_MS=1500`
- Slow request event: `SLOW_REQUEST_MS=1500`
- Slow DB query warning: `SLOW_QUERY_MS=250`

These are operational guardrails, not hard product promises. Adjust them after collecting representative staging baselines.
