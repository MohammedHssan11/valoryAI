# Firebase Auth Root Cause Certification

Date: 2026-06-11

## Final Verdict

PASS

## Root Cause

The active root `.env` file did not define the frontend Firebase Web SDK build-time variables:

- `VITE_FIREBASE_API_KEY`
- `VITE_FIREBASE_AUTH_DOMAIN`
- `VITE_FIREBASE_PROJECT_ID`
- `VITE_FIREBASE_APP_ID`
- `VITE_FIREBASE_STORAGE_BUCKET`
- `VITE_FIREBASE_MESSAGING_SENDER_ID`
- `VITE_FIREBASE_MEASUREMENT_ID`

`docker-compose.yml` already required and forwarded these values into `frontend` build args, and `frontend/Dockerfile` already exposed those args as `ENV` before `npm run build`. The break was the active environment file, not the React auth code, Dockerfile propagation, or Vite config.

Before the fix, `docker compose config` failed at interpolation with:

```text
services.frontend.build.args.VITE_FIREBASE_API_KEY: required variable VITE_FIREBASE_API_KEY is missing a value
```

The running frontend container was also stale: it was serving a previously built image whose compiled Vite env object contained only `VITE_API_BASE_URL` and `VITE_APP_ENV`, with no Firebase values. That made `isFirebaseConfigured()` return `false`, which rendered:

```text
Firebase web configuration is missing. Add the `VITE_FIREBASE_*` values before signing in.
```

## Expected Path

```text
.env
  -> docker-compose.yml frontend build.args
  -> frontend/Dockerfile ARG
  -> frontend/Dockerfile ENV
  -> npm run build
  -> Vite embeds VITE_* values
  -> frontend/src/core/config.ts
  -> frontend/src/auth/firebaseClient.ts
  -> frontend/src/features/auth/AuthScreen.tsx
```

## Actual Path Before Fix

```text
.env
  -> missing VITE_FIREBASE_* values
  -> docker compose config failed for fresh builds
  -> existing frontend container kept serving a stale bundle
  -> compiled bundle had no Firebase env entries
  -> firebaseClient configuredFirebaseOptions() returned null
  -> AuthScreen rendered the missing configuration warning
```

## Break Point

Primary break:

```text
pf_scraper/fair-price-eg/.env
```

The file had backend `FIREBASE_PROJECT_ID=valorai-e25b8`, but no `VITE_FIREBASE_*` Web SDK values. This is a backend-vs-frontend naming distinction, not an interchangeable variable.

Secondary operational evidence:

- Correct compose project was running: `fair-price-eg`.
- Correct frontend container was serving traffic: `fair-price-eg-frontend-1` on `127.0.0.1:13000`.
- The container was stale and served an image SHA different from the current `fair-price-eg-frontend:latest` tag before rebuild.

## Affected Files

- `docker-compose.yml`: forwards all required `VITE_FIREBASE_*` build args.
- `frontend/Dockerfile`: declares matching `ARG` values and exports them as `ENV` before `npm run build`.
- `frontend/src/core/config.ts`: reads `import.meta.env` using the same `VITE_FIREBASE_*` names.
- `frontend/src/auth/firebaseClient.ts`: requires `apiKey`, `authDomain`, `projectId`, and `appId`.
- `frontend/src/features/auth/AuthScreen.tsx`: renders the visible warning when Firebase is not configured.
- `.env`: fixed in the active environment file with the missing Web SDK values. This file is tracked in the current git index, so review before committing.
- `flutter_valorai/lib/firebase_options.dart`: used as the authoritative existing generated Firebase web app config for project `valorai-e25b8`.

Note: `frontend/src/auth/sessionManager.ts` does not exist in this repository. The active session manager is `frontend/src/auth/authSessionManager.ts`, imported by `AuthProvider.tsx`.

## Fix Applied

Updated local `.env` with the existing generated Firebase web app values from `flutter_valorai/lib/firebase_options.dart`.

Recorded runtime status, redacted:

```text
API_KEY = present
AUTH_DOMAIN = present
PROJECT_ID = present
APP_ID = present
STORAGE_BUCKET = present
MESSAGING_SENDER_ID = present
MEASUREMENT_ID = present
```

Also added local `BACKEND_PORT=18000` and `FRONTEND_PORT=13000` to preserve the already-running compose stack's host ports during the exact `docker compose up -d` verification. This was an environment alignment for verification, not the Firebase auth root cause.

## Verification Commands

```powershell
docker compose config
docker compose build frontend --no-cache
docker compose up -d
docker compose ps
```

Additional served-runtime checks:

```powershell
Invoke-WebRequest http://127.0.0.1:13000/
Invoke-WebRequest http://127.0.0.1:13000/assets/index-lCv52Txf.js
```

Browser check:

```text
Open http://127.0.0.1:13000/login and inspect visible auth state.
```

## Verification Results

`docker compose config`:

```text
PASS
VITE_FIREBASE_API_KEY = present
VITE_FIREBASE_AUTH_DOMAIN = present
VITE_FIREBASE_PROJECT_ID = present
VITE_FIREBASE_APP_ID = present
VITE_FIREBASE_STORAGE_BUCKET = present
VITE_FIREBASE_MESSAGING_SENDER_ID = present
VITE_FIREBASE_MEASUREMENT_ID = present
FRONTEND_PORT = 13000
BACKEND_PORT = 18000
```

`docker compose build frontend --no-cache`:

```text
PASS
npm ci completed with 0 vulnerabilities
npm run build completed
fresh frontend asset emitted: index-lCv52Txf.js
```

`docker compose up -d`:

```text
PASS
db healthy
db-bootstrap completed
backend recreated and healthy
frontend recreated and started
```

`docker compose ps`:

```text
fair-price-eg-backend-1: Up, healthy, 127.0.0.1:18000 -> 8000
fair-price-eg-db-1: Up, healthy, 127.0.0.1:5432 -> 5432
fair-price-eg-frontend-1: Up, healthy, 127.0.0.1:13000 -> 80
```

Fresh served bundle:

```text
asset = index-lCv52Txf.js
API_KEY = present
AUTH_DOMAIN = present
PROJECT_ID = present
APP_ID = present
STORAGE_BUCKET = present
MESSAGING_SENDER_ID = present
MEASUREMENT_ID = present
```

Browser runtime on `/login`:

```json
{
  "url": "http://127.0.0.1:13000/login",
  "title": "VALORAI - Intelligent OS",
  "bodyIncludesWelcome": true,
  "warningVisible": false,
  "signInButtonDisabled": false
}
```

## Naming Audit

No frontend naming mismatch was found.

- Compose uses `VITE_FIREBASE_PROJECT_ID` for frontend and `FIREBASE_PROJECT_ID` for backend.
- Dockerfile ARG names match compose build args.
- Dockerfile ENV names match Vite's `VITE_*` exposure requirement.
- `config.ts` names match the Docker/Vite names.
- `firebaseClient.ts` maps `apiKey`, `authDomain`, `projectId`, and `appId` correctly into `FirebaseOptions`.
- No `APP_ID` vs `API_KEY` swap was found.

## Environment Decision Matrix

| Hypothesis | Result | Evidence |
| --- | --- | --- |
| A) Code is wrong | No | Runtime guard is correct; it fails only when required values are empty. |
| B) Dockerfile is wrong | No | ARG and ENV declarations are present before `npm run build`. |
| C) Compose is wrong | No | Build args are present and required; config failed only because `.env` lacked values. |
| D) Running container uses stale image | Yes | Existing container served a bundle without Firebase values before rebuild. |
| E) Frontend was not rebuilt | Yes | Fresh no-cache build emitted `index-lCv52Txf.js` with values present. |
| F) `.env` is missing values | Yes | Primary root cause. |
| G) Wrong compose project is running | No | `fair-price-eg` project uses the expected compose file. |
| H) Wrong frontend container is serving traffic | No | `fair-price-eg-frontend-1` served `127.0.0.1:13000`; it was correct but stale. |

## Risk Assessment

- Firebase Web SDK config is now embedded in the static frontend bundle as expected. This is normal for Firebase web apps, but the API key must still be restricted in Firebase/Google Cloud settings.
- The active `.env` file is tracked in this repository despite the workspace ignore rule. If this environment-specific config should not be committed, keep the `.env` diff local or move runtime values into an untracked deployment env file and invoke Compose with that env file.
- The visible missing-config failure is fixed and verified.
- A real email/password sign-in was not executed because no test credentials were provided.
- The local `.env` still contains a placeholder-style `JWT_SECRET`; that is unrelated to this Firebase frontend failure but must be replaced before production release.

## Certification

The Firebase auth configuration failure was caused by missing local build-time `VITE_FIREBASE_*` values plus a stale frontend container image. The configuration chain now passes compose interpolation, the frontend image rebuild embeds the Firebase values, the container is healthy, and `/login` no longer renders the missing Firebase configuration warning.

Final Verdict: PASS
