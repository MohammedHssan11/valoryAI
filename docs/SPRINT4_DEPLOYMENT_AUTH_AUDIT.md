# Sprint 4 Deployment Auth Audit

Date: 2026-06-11

## Scope

Audited the checked-in Docker deployment path for React Firebase authentication configuration.

Files reviewed:

- `pf_scraper/fair-price-eg/docker-compose.yml`
- `pf_scraper/fair-price-eg/frontend/Dockerfile`
- `pf_scraper/fair-price-eg/frontend/nginx.conf`
- `pf_scraper/fair-price-eg/.env.example`
- `pf_scraper/fair-price-eg/frontend/.env.example`
- `pf_scraper/fair-price-eg/README.md`
- `pf_scraper/fair-price-eg/frontend/README.md`
- `pf_scraper/fair-price-eg/docs/STAGING_RUNBOOK.md`
- `pf_scraper/fair-price-eg/frontend/src/core/config.ts`
- `pf_scraper/fair-price-eg/frontend/src/auth/firebaseClient.ts`
- `pf_scraper/fair-price-eg/frontend/src/auth/tokenExchange.ts`

## Finding

The React client reads Firebase Web SDK configuration through `import.meta.env` in `frontend/src/core/config.ts`.

Required frontend values:

- `VITE_FIREBASE_API_KEY`
- `VITE_FIREBASE_AUTH_DOMAIN`
- `VITE_FIREBASE_PROJECT_ID`
- `VITE_FIREBASE_APP_ID`

The source tree and local frontend env template already defined these variables, and the auth screen correctly blocks sign-in when they are absent. The Docker path did not pass them into the Vite build.

## Root Cause

`docker-compose.yml` only passed:

- `VITE_API_BASE_URL`
- `VITE_APP_ENV`

`frontend/Dockerfile` only declared and exported those same two build-time variables. Because Vite embeds `VITE_*` values during `npm run build`, a Docker-built frontend bundle had empty Firebase configuration even when runtime container environment variables existed.

## Nginx Audit

`frontend/nginx.conf` proxies `/v1/` to `backend:8000` and serves static React assets. It does not need to inject runtime Firebase values. No nginx change was required.

## Deployment Scripts

No separate deployment script was found in the active Docker path. Compose is the deployment contract for this sprint.

## Impact

Before the fix:

- Docker-built frontend could render the missing Firebase configuration state.
- Firebase sign-in could not initialize in the static bundle.
- Protected React workflows remained unavailable even if backend token exchange was configured.

After the fix:

- Compose requires the four mandatory Firebase Web SDK values before frontend image build.
- Dockerfile propagates the values into `npm run build`.
- The static bundle embeds configured Firebase values.

