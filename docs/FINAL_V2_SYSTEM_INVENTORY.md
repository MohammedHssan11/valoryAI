# Final V2 System Inventory

Audit date: 2026-06-11
Workspace: `C:\Users\mh978\Downloads\mobile computing project`

## Authority

This inventory was rebuilt from current source code after Sprint 1, Sprint 2, and Sprint 3. Earlier `FINAL_*` reports are treated as historical context only. Source code wins where documents disagree.

## Current System Map

| Area | Location | Current status | Production path |
| --- | --- | --- | --- |
| Backend API | `pf_scraper/fair-price-eg/backend` | Active FastAPI service. Routers are registered in `app/main.py`: health, auth, pricing, broker, Copilot persistence, Copilot tools, and Copilot orchestrator. | Yes |
| React frontend | `pf_scraper/fair-price-eg/frontend` | Active Vite/React client. Now includes Firebase auth, token exchange, protected routes, valuation, property-context bridge, what-if, negotiation, investment, market intelligence, broker, and Copilot drawer. | Yes, but deployment config gap remains |
| Flutter frontend | `flutter_valorai` | Active Flutter client with Firebase auth exchange, bearer interceptor, valuation, workspace, home, and Copilot paths. It is narrower than React. | Partial/mobile path |
| Copilot | `backend/app/copilot/orchestrator` plus React/Flutter clients | Real deterministic orchestrator: intent engine, planner, executor, composer, memory, optional governed narration. | Yes |
| Broker | `backend/app/broker`, `frontend/src/features/broker` | Backend and React broker request contracts are now aligned on `workspace_id` and `scenario_id`. | Yes |
| Tool layer | `backend/app/api/routes/copilot_tools.py`, `backend/app/services/copilot_tools_service.py` | Tools 1-8 implemented and protected. Higher-order tools self-run valuation/explainability/comparables/fairness where needed. | Yes |
| Persistence | `backend/app/models/copilot.py`, migrations, `CopilotService` | Users, workspaces, chats, messages, properties, scenarios, assumptions, tool events, valuation snapshots, decisions, broker sessions, prediction logs, and shadow logs exist. | Yes |
| Auth | Backend `auth.py`/`core/auth.py`, React `src/auth`, Flutter auth manager | Firebase ID token exchange to ValorAI JWT exists across backend, React, and Flutter. Bearer injection exists in React Axios/fetch paths and Flutter Dio. | Source yes; Docker frontend config incomplete |
| Deployment | `docker-compose.yml`, backend/frontend Dockerfiles, Nginx | PostGIS, backend, bootstrap, frontend, health checks, and Nginx `/v1/` proxy exist. | Partial because frontend Docker build omits Firebase build args |
| Testing | Backend pytest, React Vitest/tsc/build, Flutter analyze/test | Current default suites pass. PostGIS integration tests are skipped unless `RUN_POSTGIS_INTEGRATION=1`. | Good local baseline; live integration not fully certified |

## Active Versus Legacy

Active canonical paths:

- Backend: `pf_scraper/fair-price-eg/backend`
- React: `pf_scraper/fair-price-eg/frontend`
- Flutter: `flutter_valorai`
- Deployment: `pf_scraper/fair-price-eg/docker-compose.yml`

Legacy or non-canonical paths:

- `react valorai`
- `pf_scraper/fair-price-eg/frontend old`
- Many phase reports under `docs` and `pf_scraper/fair-price-eg/docs`

## Backend Inventory

The backend is a substantial production-style FastAPI service. `app/main.py` registers all active routers. Pricing exposes public valuation through `/v1/valuation/fair-price`; auth exposes `/v1/auth/token-exchange`; broker, Copilot persistence, Copilot tools, and Copilot orchestrator are protected by `get_authenticated_user`.

Key implementation areas:

- Auth: `app/api/routes/auth.py`, `app/core/auth.py`, `app/core/firebase_auth.py`
- Valuation: `app/api/routes/pricing.py`, `app/services/router_service.py`, `app/services/valuation_service.py`
- Tool layer: `app/api/routes/copilot_tools.py`, `app/services/copilot_tools_service.py`
- Broker: `app/api/routes/broker.py`, `app/broker/**`
- Copilot orchestration: `app/copilot/orchestrator/**`
- Persistence: `app/models/copilot.py`, `app/services/copilot_service.py`
- Deployment safety: request IDs, correlation IDs, rate limiting, request-size cap, standard errors, health/readiness, Docker health checks

## React Frontend Inventory

Current routes:

- `/login`
- Protected shell routes: `/nexus`, `/broker`, `/valuation`, `/pulse`, `/assets`, `/vault`

Current production-path capabilities:

- Firebase email/password sign-in, sign-up, password reset, session restoration, token exchange, bearer injection, one retry after 401, access denied state.
- Direct valuation via `/v1/valuation/fair-price`.
- Direct valuation property-context bridge: lists/creates workspace, lists/creates property, records direct valuation `ToolEvent`.
- What-if, negotiation, investment, market insight services/stores/panels.
- Broker service, stream parser, screen, and context resolver aligned with backend `workspace_id`/`scenario_id`.
- Copilot drawer/panel/store/service sends workspace, scenario, broker session, and tool input context.

Important limitation:

- React source can authenticate, but Docker Compose currently builds the frontend with only `VITE_API_BASE_URL` and `VITE_APP_ENV`. The frontend auth code requires `VITE_FIREBASE_API_KEY`, `VITE_FIREBASE_AUTH_DOMAIN`, `VITE_FIREBASE_PROJECT_ID`, and `VITE_FIREBASE_APP_ID`. A Compose-built production frontend will therefore render auth as unconfigured unless deployment injects those build-time values outside the current source.

## Flutter Inventory

Flutter is an active but narrower client:

- Auth: Firebase user -> `/v1/auth/token-exchange` -> secure stored ValorAI JWT.
- Network: Dio bearer header injection and 401 renewal.
- Valuation: `/v1/valuation/fair-price`.
- Workspace: `/v1/copilot/workspaces` and workspace properties.
- Copilot: `/v1/copilot/orchestrator/respond` with workspace context.

Flutter does not yet have React parity for what-if, negotiation, investment, broker, or market intelligence. Its valuation result UI still says saving becomes available when workspace persistence is connected.

## Inventory Verdict

ValorAI is no longer blocked by the earlier React-auth, broker-contract, or backend-test-suite failures. The current system is a real multi-client valuation and decision-intelligence platform. The main remaining inventory-level caveat is deployment: source-level React auth exists, but the checked-in Docker frontend build does not inject the Firebase web config required to use it.
