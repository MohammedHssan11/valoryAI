# Environment Variables - ValoryAI (ValorAI)

This guide documents the configuration environment variables required to run the ValoryAI platform (FastAPI backend and React frontend).

---

## 1. Backend Environment Variables

Configure these variables inside a `.env` file in the `/backend` directory.

| Variable Name | Purpose | Required/Optional | Default / Example |
|:---|:---|:---:|:---|
| `ENV` | Dictates application execution mode (`dev`, `staging`, `prod`). | Optional | `dev` |
| `DEBUG` | Enables detailed stack traces and debug routing. | Optional | `false` |
| `LOG_LEVEL` | Logging verbosity level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). | Optional | `INFO` |
| `DATABASE_URL` | PostgreSQL connection URL including credentials and database name. | **Required** | `postgresql+psycopg://user:pass@localhost:5432/db` |
| `JWT_SECRET` | Secret key used to sign session authorization tokens. Must be $\ge 32$ bytes. | **Required** | `replace-with-a-random-secret-of-at-least-32-bytes` |
| `JWT_ISSUER` | Token issuer identifier. | Optional | `valorai` |
| `JWT_AUDIENCE` | Token audience validator. | Optional | `valorai-api` |
| `FIREBASE_PROJECT_ID` | Project ID validating Firebase Auth Bearer tokens. | **Required** | `valorai-e25b8` |
| `CORS_ORIGINS` | Semi-colon separated list of authorized frontend domains. | **Required** | `http://localhost:3000;http://localhost:5173` |
| `API_REQUEST_TIMEOUT_SECONDS` | Maximum timeout before request context gets cancelled. | Optional | `20` |
| `RATE_LIMIT_ENABLED` | Protects API endpoints using token-bucket rate limiting. | Optional | `true` |
| `RATE_LIMIT_PER_MINUTE` | Maximum allowed API requests per IP per minute. | Optional | `120` |
| `SLOW_QUERY_MS` | Threshold to trigger warning logs for database queries. | Optional | `250` |
| `ADDRESS_RESOLVER_VERSION` | Version reference for geocoder routing. | Optional | `3A.1b.1` |
| `AREA_AMBIGUITY_DISTANCE_M` | Buffer threshold in meters for spatial geofence overlaps. | Optional | `25` |

---

## 2. Frontend Web Environment Variables

Configure these variables inside a `.env` file in the `/frontend/web` directory.

| Variable Name | Purpose | Required/Optional | Default / Example |
|:---|:---|:---:|:---|
| `VITE_APP_ENV` | Mode for Vite bundling. | Optional | `dev` |
| `VITE_API_BASE_URL` | Endpoint URL pointing to the running FastAPI backend. | **Required** | `http://localhost:8000` |
| `VITE_API_TIMEOUT_MS` | Timeout for backend API requests. | Optional | `20000` |
| `VITE_FIREBASE_API_KEY` | Public API Key from Firebase console to initialize SDK. | **Required** | `replace-with-your-firebase-web-api-key` |
| `VITE_FIREBASE_AUTH_DOMAIN` | Firebase authorization domain target. | **Required** | `valorai-e25b8.firebaseapp.com` |
| `VITE_FIREBASE_PROJECT_ID` | Firebase project ID. | **Required** | `valorai-e25b8` |
| `VITE_FIREBASE_APP_ID` | Firebase application ID. | **Required** | `1:11968174472:web:41c15591513721751b023d` |
| `VITE_FIREBASE_STORAGE_BUCKET` | Optional storage bucket path. | Optional | `valorai-e25b8.firebasestorage.app` |
| `VITE_FIREBASE_MESSAGING_SENDER_ID` | Cloud messaging sender ID. | Optional | `11968174472` |
| `VITE_FIREBASE_MEASUREMENT_ID` | Google Analytics measurement ID. | Optional | `G-XE10J0F6KB` |

---

## 3. Environment Sanitization

> [!WARNING]
> Never commit real secrets (like private API keys or database passwords) to git history.
>
> 1. Use the templates in `backend/.env.example` and `frontend/web/.env.example`.
> 2. Ensure your actual `.env` files are excluded by the root `.gitignore`.
