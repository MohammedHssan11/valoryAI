# Sprint 1 Auth Audit

Audit date: 2026-06-10

## Scope

Sprint 1 addresses P0-1 only: React authentication, token exchange, ValorAI JWT session lifecycle, bearer-header injection, route protection, and auth tests. Broker request-shape mismatch, backend business logic, Copilot behavior, market logic, negotiation logic, investment logic, and what-if logic remain outside this sprint by instruction.

## Current Backend Auth Flow

Backend route: `pf_scraper/fair-price-eg/backend/app/api/routes/auth.py`.

1. Client sends `POST /v1/auth/token-exchange` with JSON body `{ "firebase_id_token": "<Firebase ID token>" }`.
2. `FirebaseTokenVerifier.verify(...)` validates the Firebase token.
3. `provision_user(...)` creates or reuses a backend user keyed by Firebase subject.
4. `create_access_token(...)` mints a ValorAI HS256 JWT with `sub`, `iat`, `exp`, `iss`, and `aud`.
5. Response shape is `TokenExchangeResponse`: `access_token`, `token_type: bearer`, `expires_in`, and `user`.
6. Protected backend routes depend on `get_authenticated_user`, which requires `Authorization: Bearer <ValorAI JWT>`.

Protected API surfaces verified in source:

- Copilot persistence/workspaces/properties/scenarios/tool-events: `backend/app/api/routes/copilot.py`.
- Copilot tools: `backend/app/api/routes/copilot_tools.py`.
- Copilot orchestrator: `backend/app/api/routes/copilot_orchestrator.py`.
- Broker chat/reason/stream: `backend/app/api/routes/broker.py`.

## Current Flutter Auth Flow

Flutter reference files:

- `flutter_valorai/lib/features/auth/data/datasources/auth_remote_data_source.dart`
- `flutter_valorai/lib/features/auth/presentation/state/auth_session_manager.dart`
- `flutter_valorai/lib/core/network/auth_interceptor.dart`

Flutter flow:

1. Firebase sign-in creates a Firebase current user.
2. `AuthSessionManager.renewSession()` calls `firebaseUser.getIdToken(true)`.
3. `AuthRemoteDataSource.exchangeFirebaseToken(...)` posts to `/v1/auth/token-exchange`.
4. Flutter stores the ValorAI access token, expiry, and user metadata in secure storage.
5. `AuthInterceptor.onRequest` attaches `Authorization: Bearer <jwt>`.
6. On first 401, `AuthInterceptor.onError` renews the session and retries once.
7. Repeated 401 expires the session and logout clears storage plus Firebase state.

## React Auth Gaps Found Before Sprint 1

React frontend path: `pf_scraper/fair-price-eg/frontend`.

Before Sprint 1:

- No Firebase web SDK integration.
- No `/v1/auth/token-exchange` web client.
- No ValorAI JWT session manager.
- No persisted or restorable web auth session.
- `src/api/http.ts` set request/correlation IDs only and did not set `Authorization`.
- `src/services/brokerService.ts` streamed broker SSE with raw `fetch` and no bearer token.
- App routes were not protected.
- UX had no loading, login, logout, expired-session, or access-denied states.
- Tests covered business services but not token exchange, auth injection, 401 recovery, session restore, or route protection.

## Implemented React Auth Closure

Sprint 1 added:

- Firebase web auth client in `frontend/src/auth/firebaseClient.ts`.
- Backend token exchange client in `frontend/src/auth/tokenExchange.ts`.
- Flutter-modeled web session manager in `frontend/src/auth/authSessionManager.ts`.
- React auth provider in `frontend/src/auth/AuthProvider.tsx`.
- Minimal login/signup/reset screen in `frontend/src/features/auth/AuthScreen.tsx`.
- Protected route guard in `frontend/src/features/auth/ProtectedRoute.tsx`.
- Axios bearer injection and 401 retry in `frontend/src/api/http.ts`.
- Broker SSE bearer injection and 401 retry in `frontend/src/services/brokerService.ts`.
- Logout affordance and authenticated user initials in `frontend/src/components/layout/TopNav.tsx`.
- Firebase env documentation in `frontend/.env.example`.

## Audit Verdict

P0-1 is closed in the React code path. React now follows the same identity chain as Flutter:

React login -> Firebase ID token -> `/v1/auth/token-exchange` -> ValorAI JWT -> `Authorization: Bearer <jwt>` -> protected backend APIs.
