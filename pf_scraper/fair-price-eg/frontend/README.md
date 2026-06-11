# ValorAI Frontend

Production React/Vite client for the ValorAI real estate intelligence operating system.

## Local Development

1. Install dependencies:
   `npm install`
2. Configure `.env.local` from `.env.example`.
3. Start the frontend:
   `npm run dev`

The client expects the FastAPI backend at `VITE_API_BASE_URL`, defaulting to `http://localhost:8000`.

## Docker Build Auth Configuration

Firebase Web SDK values are build-time inputs for Vite. A Docker-built frontend must receive:

```bash
VITE_FIREBASE_API_KEY
VITE_FIREBASE_AUTH_DOMAIN
VITE_FIREBASE_PROJECT_ID
VITE_FIREBASE_APP_ID
```

When using the root `docker-compose.yml`, set these values in the Compose env file before `docker compose up --build`. Changing them later requires rebuilding the frontend image.

## SPA routing safety

Routes are centralized in `src/navigation/routes.ts`. Do not add top-level SPA routes that overlap with production static directories or server-owned paths such as `/assets`, `/static`, `/images`, `/fonts`, `/icons`, `/media`, `/uploads`, `/chunks`, `/build`, `/vendor`, `/v1`, `/api`, or `/health`.

Run `npm run check:routes` to print the route inventory and collision table. `npm run test` also runs this guard.
