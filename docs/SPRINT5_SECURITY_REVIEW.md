# Sprint 5 Security Review

Date: 2026-06-11

## Scope

Review only. No security behavior or product code was modified.

## JWT Handling

Result: PASS.

Evidence:

- Backend uses HS256 with configured `JWT_SECRET`.
- JWT decode requires `sub`, `iat`, and `exp`.
- Issuer and audience are enforced.
- Compose requires `JWT_SECRET` for backend and bootstrap.
- Staging/production reject the default local secret.

Live checks:

- Missing bearer returned 401.
- Invalid bearer returned 401.
- Valid ValorAI JWT returned 200 on `GET /v1/copilot/users/me`.

## Session Lifecycle

Result: PASS WITH RISKS.

Evidence:

- Frontend session manager stores ValorAI token, expiry, and user metadata in `sessionStorage`.
- It clears stored session on logout and expiration.
- It refreshes through Firebase current user when possible.
- Unit tests cover restore, expiration, and logout behavior.

Risk:

- SPA token storage is not HttpOnly cookie based. If the app later has an XSS flaw, a browser token could be exposed. This is an architectural tradeoff, not a Sprint 5 regression.

## Protected Routes

Result: PASS.

Evidence:

- Frontend `ProtectedRoute` redirects unauthenticated users to `/login`.
- Expired sessions redirect to `/login?reason=expired`.
- Backend protected routes use `get_authenticated_user`.

Live browser evidence:

- Unauthenticated production frontend redirected to `/login`.

## Authorization Enforcement

Result: PASS WITH RISKS.

Live cross-tenant checks using a second JWT:

| Path | Status | Result |
| --- | --- | --- |
| `GET /v1/copilot/workspaces/533` | 404 | PASS |
| `GET /v1/copilot/properties/606` | 404 | PASS |
| `GET /v1/copilot/scenarios/349` | 404 | PASS |
| `POST /v1/copilot/tools/valuation` with foreign workspace/property/scenario | 404 | PASS |
| `POST /v1/broker/reason` with foreign workspace/scenario | 400 | PASS WITH RISK |

Broker risk:

- Broker cross-tenant workspace access did not expose data, but it returned 400 with `Workspace not found` instead of the 404 shape used by other protected resource boundaries.
- Recommended follow-up: align broker missing/foreign workspace responses to 404.

## Workspace Ownership Validation

Result: PASS.

Evidence:

- Copilot service queries scope workspace by `Workspace.user_id == actor_user_id`.
- Live foreign workspace access returned 404.

## Scenario Ownership Validation

Result: PASS.

Evidence:

- Scenario routes resolve scenario by actor user.
- Tool service validates `scenario.workspace_id` and `scenario.property_state_id`.
- Live foreign scenario access returned 404.

## Broker Authorization

Result: PASS WITH RISKS.

Evidence:

- Broker endpoints require `get_authenticated_user`.
- Broker session binding receives actor user id.
- Foreign workspace/scenario request did not execute reasoning and did not expose tenant data.

Risk:

- Error status differs from other authorization boundaries: 400 instead of 404.

## Security Review Verdict

PASS WITH RISKS.

No data exposure was observed. The two main risks are frontend token storage design and broker error-status consistency. The largest auth/security blocker remains deployment-level: live Firebase browser auth is disabled by missing frontend Firebase config.
