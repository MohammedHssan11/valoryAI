# Sprint 4 Firebase Deployment Fix

Date: 2026-06-11

## Changes

Implemented Firebase Web SDK configuration propagation for Docker-built React frontend images.

Modified:

- `pf_scraper/fair-price-eg/docker-compose.yml`
- `pf_scraper/fair-price-eg/frontend/Dockerfile`
- `pf_scraper/fair-price-eg/.env.example`
- `pf_scraper/fair-price-eg/frontend/.env.example`
- `pf_scraper/fair-price-eg/README.md`
- `pf_scraper/fair-price-eg/frontend/README.md`
- `pf_scraper/fair-price-eg/docs/STAGING_RUNBOOK.md`

## Compose Contract

The frontend build now receives:

- `VITE_FIREBASE_API_KEY`
- `VITE_FIREBASE_AUTH_DOMAIN`
- `VITE_FIREBASE_PROJECT_ID`
- `VITE_FIREBASE_APP_ID`
- `VITE_FIREBASE_STORAGE_BUCKET`
- `VITE_FIREBASE_MESSAGING_SENDER_ID`
- `VITE_FIREBASE_MEASUREMENT_ID`

Compose fails early if the four required Firebase Web SDK values are missing.

## Dockerfile Contract

`frontend/Dockerfile` now declares matching `ARG` values and exports them as `ENV` before `npm run build`, allowing Vite to embed them in the static assets.

## Runtime Notes

Vite does not read container runtime env after build for static assets. Changing Firebase Web SDK values requires rebuilding the frontend image.

## Verification

Commands run:

```powershell
npm run build
docker compose config
docker compose build frontend
docker run --rm fair-price-eg-frontend:latest sh -c "grep -R 'demo-project' -n /usr/share/nginx/html/assets >/tmp/firebase-grep && cat /tmp/firebase-grep"
```

Results:

- `npm run build` passed.
- `docker compose config` showed all Firebase build args under the frontend service.
- `docker compose build frontend` passed.
- Static bundle contained placeholder Firebase values supplied through Compose build args.
- Browser smoke against the built image rendered the auth screen and did not show `Firebase web configuration is missing`.

Known limitation:

- Real Firebase login requires real Firebase project credentials. This sprint verified the Docker build/configuration path and existing token-exchange tests, not a real third-party Firebase account login.

