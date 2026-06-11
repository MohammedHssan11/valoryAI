# Final System Inventory

Audit date: 2026-06-10
Workspace: `C:\Users\mh978\Downloads\mobile computing project`

## Scope And Authority

This inventory is based on source code, tests, deployment files, and the existing report archive. Source code is treated as authoritative where docs and implementation disagree.

## Active Product Areas

| Area | Location | Status |
| --- | --- | --- |
| Backend API | `pf_scraper/fair-price-eg/backend` | Active FastAPI service with valuation, broker, Copilot persistence, Copilot tools, and orchestrator routes. |
| React web app | `pf_scraper/fair-price-eg/frontend` | Active Vite/React client with valuation, what-if, negotiation, investment, market, broker, and Copilot UI surfaces. |
| Flutter mobile app | `flutter_valorai` | Active mobile client with Firebase auth, backend JWT exchange, valuation, workspace, and Copilot access. |
| Legacy/old clients | `react valorai`, `pf_scraper/fair-price-eg/frontend old` | Non-canonical or historical. Do not use for readiness claims. |
| Docs and audit archive | `docs`, `pf_scraper/fair-price-eg/docs`, root markdown files | Extensive phase reports and architecture docs; several are moved/untracked in git. |
| Data and scraper assets | root scraper/data folders, `pf_scraper` | Supporting data collection and valuation inputs. |

## Backend Inventory

Main app registration is in `pf_scraper/fair-price-eg/backend/app/main.py:62-68`.

Registered route groups:

| Router | Evidence | Purpose |
| --- | --- | --- |
| Health | `backend/app/api/routes/health.py` | Health, readiness, staging observability. |
| Auth | `backend/app/api/routes/auth.py:20` | Firebase token exchange to internal ValorAI JWT. |
| Pricing | `backend/app/api/routes/pricing.py:17` | Public direct valuation endpoint `/v1/valuation/fair-price`; legacy `/v1/rent/fair-price`. |
| Broker | `backend/app/api/routes/broker.py:31` | Protected broker analysis, chat, intent, reason, stream, session state. |
| Copilot persistence | `backend/app/api/routes/copilot.py` | Protected workspaces, chats, messages, properties, scenarios, assumptions, events, decisions. |
| Copilot tools | `backend/app/api/routes/copilot_tools.py:24-36` | Protected valuation, explainability, comparable, fairness, what-if, negotiation, investment, market insight tools. |
| Copilot orchestrator | `backend/app/api/routes/copilot_orchestrator.py` | Protected `/v1/copilot/orchestrator/respond`. |

Backend model inventory:

| Model | Evidence | Purpose |
| --- | --- | --- |
| User | `backend/app/models/copilot.py:46` | Authenticated user identity. |
| Workspace | `backend/app/models/copilot.py:56` | Tenant/user workspace. |
| PropertyState | `backend/app/models/copilot.py:123` | Persisted property context. |
| ScenarioState | `backend/app/models/copilot.py:168` | What-if/scenario state. |
| ToolEvent | `backend/app/models/copilot.py:265` | Auditable tool usage. |
| ValuationSnapshot | `backend/app/models/copilot.py:310` | Persisted protected-tool valuation output. |
| PredictionLog | `backend/app/models/copilot.py:346` | Prediction monitoring. |
| ShadowLog | `backend/app/models/copilot.py:369` | Shadow/model monitoring. |
| DecisionHistory | `backend/app/models/copilot.py:393` | Copilot memory/decision record. |
| BrokerSession | `backend/app/models/copilot.py:473` | Broker continuity state. |

Backend service inventory:

| Service/System | Status |
| --- | --- |
| Direct valuation router | Real deterministic category-aware valuation pipeline through `price_listing_router`. |
| Copilot tools service | Real implementation in `backend/app/services/copilot_tools_service.py`; persists snapshots/events and composes higher-order tools. |
| Copilot orchestrator | Real deterministic runtime: intent engine, planner, executor, composer, memory, optional narration. |
| Broker orchestrator | Real broker pipeline with session binding, reasoning, streaming, and governed response. |
| Auth | JWT-protected internal endpoints; Firebase token exchange for client auth. |
| Error handling | Standard error envelope in backend core error handlers. |
| Deployment | Docker Compose plus Nginx proxy for frontend-to-backend `/v1/` traffic. |

## React Frontend Inventory

Routes observed in the active React app:

| Route | Product Surface |
| --- | --- |
| `/nexus` | Main dashboard/intelligence hub. |
| `/valuation` | Direct valuation workflow and results. |
| `/pulse` | Market/intelligence surface. |
| `/broker` | Broker reasoning UI. |
| `/assets` | Asset/workspace surface. |
| `/vault` | Vault/history surface. |

Shell inventory:

| Component | Evidence | Purpose |
| --- | --- | --- |
| `TopNav` | `frontend/src/layouts/AppShell.tsx:4,21` | Desktop navigation. |
| `BottomNav` | `frontend/src/layouts/AppShell.tsx:4,22` | Mobile navigation. |
| `CopilotDrawer` | `frontend/src/layouts/AppShell.tsx:6,30` | Global Copilot assistant UI. |

Frontend service/store inventory:

| Area | Status |
| --- | --- |
| HTTP client | Axios base client adds request/correlation IDs, but no Authorization bearer token injection. Evidence: `frontend/src/api/http.ts:69-71`. |
| Direct valuation | Calls `/v1/valuation/fair-price`; this is the only major web workflow that can work without auth. |
| Property context bridge | Attempts workspace/property/tool-event persistence after valuation. Blocked by missing web auth. |
| What-if | UI, services, store, tests exist; requires active workspace/property context. |
| Negotiation | UI, services, store, tests exist; requires active workspace/property context. |
| Investment | UI, services, store, tests exist; requires active workspace/property context. |
| Market insight | UI, services, store, tests exist; requires protected workspace and persisted snapshots/events. |
| Copilot | Drawer/store/services/tests exist; requires active workspace and protected orchestrator endpoint. |
| Broker | UI/services/tests exist, but frontend request contract omits backend-required context. |

## Flutter Mobile Inventory

Flutter is not just a mock shell. It has:

| Area | Evidence | Status |
| --- | --- | --- |
| Auth interceptor | `flutter_valorai/lib/core/network/auth_interceptor.dart:12-14` | Adds `Authorization: Bearer <token>`. |
| JWT exchange | `flutter_valorai/lib/features/auth/data/datasources/auth_remote_data_source.dart:16` | Calls `/v1/auth/token-exchange`. |
| Session manager | `flutter_valorai/lib/features/auth/presentation/state/auth_session_manager.dart:102-124` | Gets Firebase ID token, exchanges, stores ValorAI JWT. |
| Valuation | `flutter_valorai/lib/features/valuation/data/datasources/valuation_remote_data_source.dart` | Calls backend valuation API. |
| Copilot | `flutter_valorai/lib/features/copilot/data/datasources/copilot_remote_data_source.dart` | Calls protected orchestrator with workspace context. |

Flutter is auth-aligned with the backend, but it is feature-thinner than the React app.

## Inventory Verdict

The repository contains a substantial real backend and two active clients. The backend implementation is deeper than a demo stub. The React frontend has broad UI coverage but is not wired for authenticated protected workflows. The Flutter app has better auth integration but narrower product coverage. Existing docs describe many mature phases, but the source shows the final product is not fully integrated end to end.
