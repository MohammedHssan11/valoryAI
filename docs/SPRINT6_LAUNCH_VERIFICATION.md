# Sprint 6 Launch Verification

Date: 2026-06-11

All results below are from commands executed in Sprint 6. No guessed results are included.

## Backend

Command:

```powershell
pytest --collect-only -q
```

Result:

- Exit code: 0
- 208 tests collected in 6.50s

Command:

```powershell
pytest -q
```

Result:

- Exit code: 0
- 206 passed, 11 skipped in 65.23s

## Frontend

Command:

```powershell
npm run lint
```

Result:

- Exit code: 0
- `tsc --noEmit` completed.

Command:

```powershell
npm test
```

Result:

- Exit code: 0
- Test files: 35 passed
- Tests: 144 passed
- Duration: 23.18s

Command:

```powershell
npm run build
```

Result:

- Exit code: 0
- Vite build completed in 5.28s.
- Warning: main chunk `assets/index-CprzPckt.js` is 648.85 kB after minification, 159.92 kB gzip.

## Flutter

Command:

```powershell
flutter analyze
```

Result:

- Exit code: 0
- No issues found.
- Ran in 13.2s.

Command:

```powershell
flutter test
```

Result:

- Exit code: 0
- 11 tests passed.

## Docker

Command:

```powershell
docker compose --env-file .env.example config
```

Result:

- Exit code: 0
- Compose config rendered successfully.
- Frontend Firebase build args present.

Command:

```powershell
docker compose --env-file .env.example build
```

Result:

- Exit code: 0
- `fair-price-eg-backend` built.
- `fair-price-eg-db-bootstrap` built.
- `fair-price-eg-frontend` built.
- Frontend Docker build repeated Vite large chunk warning; build still succeeded.

## Disposable Deployment Smoke

Command:

```powershell
$env:BACKEND_PORT='18080'
$env:FRONTEND_PORT='13080'
$env:POSTGRES_PORT='15480'
docker compose --env-file .env.example -p valorai-sprint6 up -d --wait
```

Result:

- Exit code: 0
- DB healthy.
- DB bootstrap exited successfully.
- Backend healthy.
- Frontend healthy.

HTTP probes:

- Backend `/health`: success true, status ok.
- Backend `/health/ready`: success true, database ok.
- Nginx `/health`: success true, status ok.
- Nginx `/health/ready`: success true, database ok.
- First frontend-root probe using PowerShell `Invoke-WebRequest` failed with a client-side `System.NullReferenceException`.
- Nginx `/`: HTTP 200, content length 1662, security headers present.
- Nginx `/v1/copilot/users/me` with generated ValorAI JWT: HTTP 200, returned user subject `sprint6-smoke-user`.

Bootstrap log evidence:

- Migrations succeeded.
- Loaded staging rows: 62608.
- Upserted area nodes: 3104.
- Orphan area refs: 0.
- Planner statistics refreshed.

Staging smoke:

```powershell
docker compose --env-file .env.example -p valorai-sprint6 --profile staging run --rm staging-smoke
```

Result:

- Exit code: 0
- `ok: true`
- readiness 200
- openapi 200
- valuation 200
- invalid payload 422 with `INVALID_COORDINATES`
- metrics 200
- operational 200, status ok

PostGIS integration:

```powershell
$env:RUN_POSTGIS_INTEGRATION='1'
$env:DATABASE_URL='postgresql+psycopg://fairprice:fairprice@localhost:15480/fairprice'
pytest -q -m integration
```

Result:

- Exit code: 0
- 17 passed, 206 deselected in 19.41s

Cleanup:

```powershell
docker compose -p valorai-sprint6 down -v
```

Result:

- Exit code: 0
- Containers, network, and disposable volume removed.
- `docker compose -p valorai-sprint6 ps` showed no remaining services.

## Verification Summary

Launch verification result: PASS FOR PILOT.

Known caveats:

- Real Firebase browser login was not executed because no real production/staging Firebase credentials were supplied.
- React production bundle still has a large chunk warning.
- Full production observability requires external retention and alerting.
