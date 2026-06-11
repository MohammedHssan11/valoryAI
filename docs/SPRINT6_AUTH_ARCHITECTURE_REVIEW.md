# Sprint 6 Auth Architecture Review

Date: 2026-06-11

## Current Architecture

Current source uses:

1. Firebase client authentication in React and Flutter.
2. Backend `/v1/auth/token-exchange` verifies a Firebase ID token.
3. Backend issues a short-lived ValorAI JWT.
4. Frontend stores ValorAI JWT in React `sessionStorage`.
5. Axios/Dio interceptors attach `Authorization: Bearer`.
6. Backend provisions/loads the user by JWT `sub` and enforces tenant ownership.

## Strengths

- Keeps Firebase as identity provider without trusting client-supplied user ids.
- Backend owns the ValorAI authorization boundary.
- JWT verification includes issuer, audience, expiration, issued-at, and subject.
- Frontend retries once on 401 by renewing through Firebase.
- Flutter uses `flutter_secure_storage`, a stronger mobile token store than browser storage.
- Route/service ownership checks are strong in current source.

## Weaknesses

- React bearer JWT is readable by JavaScript because it is stored in `sessionStorage`.
- No HttpOnly cookie or CSRF-protected backend session exists.
- No BFF layer exists to keep access tokens out of the browser.
- Live Firebase production login was not executed with real production credentials in Sprint 6.

## Alternatives Reviewed

### Keep Current Approach

Benefits:

- Lowest risk.
- Existing React, Flutter, backend tests pass.
- No contract rewrite.
- Works for pilot deployments if XSS controls and environment secrets are managed carefully.

Costs:

- Browser token theft impact remains higher than an HttpOnly cookie design.
- Enterprise buyers may require a stricter posture.

### HttpOnly Cookie Architecture

Benefits:

- Removes ValorAI bearer token from JavaScript-readable storage.
- Better browser security posture.

Costs:

- Requires CSRF strategy, cookie domain/SameSite design, CORS/credential changes, and frontend auth flow changes.
- Higher regression risk late in final hardening.

### Backend-for-Frontend Architecture

Benefits:

- Strongest browser-token isolation.
- Better future centralization for Firebase/session controls.

Costs:

- Architectural change, new route boundaries, new deployment concerns.
- Not appropriate for this sprint scope.

## Decision

Keep the current Firebase token exchange plus ValorAI JWT architecture for pilot.

Do not implement an HttpOnly cookie or BFF rewrite in Sprint 6.

## Rationale

The current approach passes backend, frontend, Flutter, PostGIS integration, Docker build, Docker health, protected API, and staging smoke verification. A cookie/BFF rewrite would be high-disruption and outside the final hardening mandate.

## Required Production Follow-Up

Before full enterprise production, revisit:

- HttpOnly cookie or BFF session design.
- CSRF strategy if cookies are introduced.
- Token lifetime and revocation policy.
- External WAF/gateway rate limiting.
- Real Firebase staging/prod login smoke.

