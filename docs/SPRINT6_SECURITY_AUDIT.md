# Sprint 6 Security Audit

Date: 2026-06-11

## Scope

Audited current source code as authoritative for backend auth, JWT lifecycle, token validation, token expiration, authorization boundaries, workspace ownership, property ownership, scenario ownership, broker ownership, Copilot ownership, protected tool ownership, and cross-tenant isolation.

Primary source areas reviewed:

- `pf_scraper/fair-price-eg/backend/app/core/auth.py`
- `pf_scraper/fair-price-eg/backend/app/core/firebase_auth.py`
- `pf_scraper/fair-price-eg/backend/app/core/config.py`
- `pf_scraper/fair-price-eg/backend/app/api/routes/*.py`
- `pf_scraper/fair-price-eg/backend/app/services/copilot_service.py`
- `pf_scraper/fair-price-eg/backend/app/services/copilot_tools_service.py`
- `pf_scraper/fair-price-eg/backend/app/broker/sessions/state.py`
- `pf_scraper/fair-price-eg/backend/app/copilot/orchestrator/memory/integration.py`
- `pf_scraper/fair-price-eg/backend/app/copilot/orchestrator/llm/gate.py`

## Findings

### Authentication

Status: PASS WITH RESIDUAL RISK.

- ValorAI bearer JWTs are verified with HS256, issuer, audience, and required `sub`, `iat`, and `exp` claims.
- Invalid or missing bearer credentials return 401 with `WWW-Authenticate: Bearer`.
- Firebase ID tokens are verified as RS256, project-bound by issuer and audience, certificate-keyed by `kid`, and subject-bounded.
- Production/staging settings reject the default local JWT secret and production debug mode.

Residual risk:

- ValorAI browser tokens are stored in React `sessionStorage`. This is acceptable for a pilot MVP with strong XSS hygiene, but it is not the strongest enterprise posture.
- No refresh token exists in ValorAI itself; renewal depends on Firebase session state.

### Authorization And Tenant Isolation

Status: PASS.

- Copilot persistence routes bind user identity from `get_authenticated_user`; caller-supplied user ids are not trusted.
- `CopilotService` scopes workspace, chat, message, property, scenario, assumption, tool event, decision, and direct valuation snapshot operations by authenticated `user_id`.
- Copilot Tool Layer checks workspace, property, scenario, and valuation snapshot ownership before reading or composing evidence.
- Broker session creation validates workspace and scenario ownership. Existing broker sessions reject ownership mismatches.
- Copilot memory integration validates workspace, scenario, broker session, property context, and tenant before building or persisting memory. Inaccessible scope returns `ACCESS_DENIED`.
- Narration admission gate validates workspace, scenario, broker session, and citation binding before provider-visible narration.

### Public Surface

Status: ACCEPTED PILOT RISK.

- Health endpoints are public.
- Pricing endpoints `/v1/rent/fair-price` and `/v1/valuation/fair-price` are public by current contract. They do not expose tenant-persisted data and are rate/body limited, but they can consume compute.
- Protected Copilot, Broker, Tool, and Orchestrator surfaces require bearer auth.

### Security Controls

Status: PASS.

- Request body size limit is enforced.
- In-process rate limiting applies to configured pricing and broker prefixes.
- API request timeout is enforced.
- Response security headers include `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, and `Permissions-Policy`.
- CORS rejects wildcard origins in staging/production and rejects wildcard with credentials.

## Cross-Tenant Verification Evidence

Executed during Sprint 6:

- `pytest --collect-only -q`: 208 tests collected.
- `pytest -q`: 206 passed, 11 skipped.
- `RUN_POSTGIS_INTEGRATION=1 pytest -q -m integration`: 17 passed, 206 deselected.

Covered tests include:

- `test_copilot_rejects_caller_supplied_user_id_without_bearer_token`
- `test_user_and_workspace_isolation_with_multiple_properties`
- `test_soft_delete_restore_and_tool_event_tenant_safety`
- `test_database_constraints_reject_cross_tenant_workspace_pair`
- `test_valuation_and_explainability_tools_apply_scenario_state_and_persist_audit_events`
- `test_direct_valuation_tool_event_persists_snapshot_for_market_and_explainability`
- `test_runtime_access_denial_redacts_scope_dependent_delivery_metadata`
- `test_memory_fails_closed_for_tenants_deleted_scenarios_and_runtime_mismatch`
- PostGIS integration tests for cross-tenant tool, market insight, executor, memory, and response-composer paths.

## Vulnerabilities Found

No source-level cross-tenant data access vulnerability was found in current code.

No Sprint 6 code fix was applied. Current source already contains fixes for direct valuation snapshot persistence, Firebase Docker build args, and ownership-bound persistence/tool access.

## Residual Security Risks

| Risk | Severity | Disposition |
| --- | --- | --- |
| Browser `sessionStorage` bearer token posture | Medium | Accept for pilot; revisit with HttpOnly cookie/BFF before enterprise production. |
| Public pricing compute endpoint | Medium | Accept for pilot with rate/body limits; consider auth-gating for commercial production. |
| In-process rate limits and metrics reset on restart | Low/Medium | Accept for pilot; external gateway/APM recommended for production scale. |
| Live Firebase browser login not executed with real production credentials in Sprint 6 | Medium | Deployment contract verified; environment credential smoke still required per target staging environment. |

## Security Certification

Security certification status: PASS FOR PILOT.

Production security status: NOT FULLY PRODUCTION-CERTIFIED because token storage posture and live Firebase credential smoke remain environment and architecture follow-ups.

