# Sprint 6 Token Security Decision

Date: 2026-06-11

## Decision

Keep current token architecture with minimal hardening already present in source.

Final decision: No Sprint 6 token-storage rewrite.

## Current Token Controls

Backend ValorAI JWT:

- HS256 signed.
- Requires `sub`, `iat`, and `exp`.
- Validates `iss` and `aud`.
- Uses configurable expiration, defaulting to `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`.
- Production/staging reject default local JWT secret.

Firebase token exchange:

- Requires Firebase project id.
- Requires RS256 token header.
- Requires known certificate `kid`.
- Validates audience and issuer for the configured project.
- Requires valid subject.

Frontend storage:

- React stores ValorAI JWT and expiry in `sessionStorage`.
- React clears expired sessions and renews from Firebase.
- Flutter stores token using secure storage.

## Options Considered

| Option | Decision | Reason |
| --- | --- | --- |
| Keep current bearer JWT in browser sessionStorage | Selected for pilot | Verified, low disruption, current tests pass |
| Move to HttpOnly cookie | Rejected for Sprint 6 | Requires CSRF/CORS/session redesign |
| Add BFF session layer | Rejected for Sprint 6 | Architecture rewrite outside final hardening |
| Increase token lifetime | Rejected | Reduces security |
| Remove JWT exchange and trust Firebase on every API call | Rejected | More coupling and repeated external verification cost |

## Risk Acceptance

Accepted for pilot:

- XSS could expose React session token.
- Token revocation is bounded by token expiry plus Firebase renewal behavior.

Not accepted for full production without revisit:

- Enterprise-grade browser token posture.
- Formal key rotation and revocation runbook.
- Live Firebase production credential smoke.

## Verification

- `pytest -q`: 206 passed, 11 skipped.
- Auth exchange tests verify Firebase project/audience/issuer validation and usable ValorAI JWT issuance.
- Docker protected-route smoke generated a ValorAI JWT in the backend container and successfully called `/v1/copilot/users/me` through nginx.

## Final Token Verdict

Pilot acceptable. Not final enterprise-production posture.

