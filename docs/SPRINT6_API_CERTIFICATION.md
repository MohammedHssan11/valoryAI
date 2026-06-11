# Sprint 6 API Certification

Date: 2026-06-11

## Certified API Families

| Family | Routes | Auth | Success Contract | Certification |
| --- | --- | --- | --- | --- |
| Health | `/health`, `/health/ready`, `/health/metrics`, `/health/operational` | Public | Envelope | PASS |
| Auth | `/v1/auth/token-exchange` | Firebase token | Raw | PASS |
| Pricing | `/v1/rent/fair-price`, `/v1/valuation/fair-price` | Public | Envelope | PASS WITH POLICY RISK |
| Broker | `/v1/broker/analyze`, `/chat`, `/intent`, `/reason`, `/session/{id}` | ValorAI JWT | Envelope | PASS |
| Broker Stream | `/v1/broker/stream` | ValorAI JWT | SSE | PASS |
| Copilot Persistence | `/v1/copilot/*` | ValorAI JWT | Raw | PASS |
| Copilot Tools | `/v1/copilot/tools/*` | ValorAI JWT | Raw | PASS |
| Copilot Orchestrator | `/v1/copilot/orchestrator/respond` | ValorAI JWT | Raw | PASS |

## Runtime Certification Evidence

Default backend:

- `pytest --collect-only -q`: 208 tests collected in 6.50s.
- `pytest -q`: 206 passed, 11 skipped in 65.23s.

PostGIS integration:

- `pytest -q -m integration`: 17 passed, 206 deselected in 19.41s.

Frontend:

- `npm run lint`: passed (`tsc --noEmit`).
- `npm test`: 35 files passed, 144 tests passed.
- `npm run build`: passed in 5.28s with large chunk warning.

Flutter:

- `flutter analyze`: No issues found.
- `flutter test`: 11 tests passed.

Docker live smoke:

- Backend `/health`: success true, status ok.
- Backend `/health/ready`: success true, database ok.
- Nginx `/health`: success true, status ok.
- Nginx `/health/ready`: success true, database ok.
- Nginx `/`: HTTP 200, content length 1662, security headers present.
- Nginx `/v1/copilot/users/me` with generated ValorAI JWT: HTTP 200 and returned `external_subject = sprint6-smoke-user`.
- Staging smoke: `ok: true`.

## Known API Risks

| Risk | Severity | Status |
| --- | --- | --- |
| Mixed success contract families | Medium | Documented and accepted for pilot |
| Public pricing compute endpoint | Medium | Accepted for pilot with rate/body limits |
| Broker stream not covered by browser Playwright in Sprint 6 | Low | Backend and frontend tests cover stream parsing/service behavior |
| Real Firebase login not executed with production credentials | Medium | Environment credential smoke still required |

## API Certification Result

PASS FOR PILOT.

Not certified as fully production-complete until live Firebase login and long-running external observability are validated in the target environment.

