# Sprint 1 Auth Architecture

Date: 2026-06-10

## Target Architecture

```text
React
  -> Firebase Authentication
  -> POST /v1/auth/token-exchange
  -> ValorAI JWT
  -> Authorization: Bearer <jwt>
  -> Protected backend APIs
```

## Firebase Identity

React uses the Firebase web SDK from `frontend/src/auth/firebaseClient.ts`.

Required Vite environment keys:

- `VITE_FIREBASE_API_KEY`
- `VITE_FIREBASE_AUTH_DOMAIN`
- `VITE_FIREBASE_PROJECT_ID`
- `VITE_FIREBASE_APP_ID`
- Optional storage/messaging/measurement keys are also supported.

Email/password sign-in, sign-up, password reset, auth-state restoration, and Firebase sign-out are wired through the Firebase client.

## Token Exchange Endpoint

React exchanges Firebase ID tokens through `frontend/src/auth/tokenExchange.ts`.

Request:

```http
POST /v1/auth/token-exchange
Content-Type: application/json

{ "firebase_id_token": "<Firebase ID token>" }
```

Response:

```json
{
  "access_token": "<ValorAI JWT>",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "external_subject": "firebase-subject",
    "display_name": "User"
  }
}
```

## ValorAI JWT Lifecycle

`frontend/src/auth/authSessionManager.ts` owns the web session lifecycle.

- Stores ValorAI token, expiry, and backend user metadata in browser `sessionStorage`.
- Keeps the active session in memory for request injection.
- Restores unexpired browser-session JWTs on app bootstrap.
- If the stored JWT is expired but Firebase still has a current user, renews by forcing a fresh Firebase ID token and re-exchanging with the backend.
- Clears browser session data on logout and signs out from Firebase.

Browser note: unlike Flutter's secure storage, browsers cannot make a JavaScript-readable JWT fully XSS-proof without a backend-for-frontend/httpOnly-cookie design. Sprint 1 narrows persistence to `sessionStorage` and renews from Firebase rather than long-lived local storage.

## Expiration Handling

The session manager treats tokens inside a 60-second expiry window as not usable and renews them before protected calls.

Expiration paths:

- Expired stored JWT + Firebase user present: renew session.
- Expired stored JWT + no Firebase user: anonymous state.
- 401 from protected API after retry failure: expired-session state.

## Refresh Behavior

Refresh uses:

1. `FirebaseUser.getIdToken(true)`.
2. `POST /v1/auth/token-exchange`.
3. In-memory and `sessionStorage` replacement of the ValorAI JWT.

Concurrent refreshes are deduplicated by a single renewal promise.

## Logout Behavior

Logout:

- Removes `valorai_access_token`.
- Removes `valorai_access_token_expires_at`.
- Removes `valorai_user_metadata`.
- Calls Firebase sign-out.
- Returns React auth state to anonymous.

## Protected API Access

Axios path:

- `frontend/src/api/http.ts` attaches `Authorization: Bearer <jwt>` on every request when an authenticated ValorAI token exists.
- On 401, it renews once, updates the header, and retries the original request.
- On repeated 401, it expires the session.
- On 403, it marks access denied for the guard UX.

Fetch/SSE path:

- `frontend/src/services/brokerService.ts` attaches `Authorization: Bearer <jwt>` for `POST /v1/broker/stream`.
- It renews and retries once on 401.

## Route Protection

`frontend/src/features/auth/ProtectedRoute.tsx` protects the app shell and its Broker, Assets, Vault, Pulse/intelligence, Nexus, valuation, and Copilot drawer surfaces.

States:

- Loading session.
- Login/signup/reset.
- Logout.
- Session expired redirect to login.
- Access denied state.

## Architecture Verdict

React is now an authenticated first-class client for protected ValorAI backend APIs. The implementation mirrors Flutter's reference lifecycle while using browser-appropriate storage and React route guards.
