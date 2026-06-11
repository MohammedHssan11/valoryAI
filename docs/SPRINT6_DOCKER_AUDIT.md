# Sprint 6 Docker Audit

Date: 2026-06-11

## Backend Dockerfile

Status: PASS.

Current behavior:

- Uses `python:3.11-slim`.
- Installs pinned backend requirements.
- Copies backend app.
- Exposes port 8000.
- Healthchecks `/health/ready`.
- Runs uvicorn on `0.0.0.0:8000`.

Risk:

- No non-root runtime user configured.
- No image vulnerability scan executed in Sprint 6.

## Frontend Dockerfile

Status: PASS.

Current behavior:

- Uses `node:22-alpine` build stage.
- Runs `npm ci`.
- Accepts Vite build args for API base URL, app env, and Firebase web config.
- Uses `nginx:1.27-alpine` runtime stage.
- Healthchecks nginx root.

Verified improvement:

- Firebase web args are now present and wired through Docker build.

Risk:

- Vite bundle emits known large chunk warning.
- Real Firebase values are environment-supplied; placeholder `.env.example` cannot prove real login.

## Nginx

Status: PASS.

Current behavior:

- Serves SPA root with `try_files`.
- Proxies `/v1/` to backend.
- Proxies `/health` and `/health/ready`.
- Sets security headers:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Referrer-Policy: no-referrer`
  - `Permissions-Policy: geolocation=(), microphone=(), camera=()`
- Sets request/correlation headers through proxy.
- Limits client body to 64k.

## Compose

Status: PASS.

Current behavior:

- DB health-gated.
- Bootstrap waits on DB.
- Backend waits on DB and bootstrap.
- Frontend waits on backend health.
- Required secrets/build args use `${VAR:?message}` for fail-fast behavior.
- Staging smoke profile exists.

## Verification Results

- `docker compose --env-file .env.example config`: pass.
- `docker compose --env-file .env.example build`: pass.
- `docker compose --env-file .env.example -p valorai-sprint6 up -d --wait`: pass.
- `docker compose --env-file .env.example -p valorai-sprint6 --profile staging run --rm staging-smoke`: pass, `ok: true`.
- `docker compose -p valorai-sprint6 down -v`: pass.

## Docker Certification

Docker certification: PASS FOR PILOT.

Production hardening follow-ups:

- Run container image vulnerability scan.
- Consider non-root users in backend/frontend runtime images.
- Add external log/metrics shipping in deployment environment.

