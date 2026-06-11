# Final V2 Integration Audit

Audit date: 2026-06-11

## Integration Chain Matrix

| Chain | Current runtime path | Status |
| --- | --- | --- |
| Valuation -> Property Context | React valuation success calls `bridgeValuationToPropertyContext`, which lists/creates workspace, lists/creates property, and records a direct valuation tool event through protected Copilot persistence endpoints. | Complete in source; requires valid Firebase config at runtime. |
| Property Context -> Scenario | What-if panel loads scenario history for active property, can save scenario state, restore scenario, and synchronize selected scenario into active context. | Complete in React source. |
| Scenario -> What-if | What-if panel sends `workspace_id`, `property_id`, optional `scenario_id`, and modifications to `/v1/copilot/tools/what-if`; backend creates base/sandbox valuation snapshots and returns explainability/comparables/fairness. | Complete. |
| Scenario -> Negotiation | Negotiation panel selects base/active/restored scenario and sends aligned request to `/v1/copilot/tools/negotiation`; backend composes valuation, explainability, comparable, and fairness evidence. | Complete. |
| Scenario -> Investment | Investment panel selects base/active/restored/compared scenario and sends aligned request to `/v1/copilot/tools/investment`; backend composes negotiation and investment position. | Complete. |
| Workspace -> Market Intelligence | Pulse panel sends workspace filters to `/v1/copilot/tools/market-insight`; backend analyzes persisted `ValuationSnapshot` records. | Complete after protected valuation/tool history exists; sparse after direct-only valuation. |
| Workspace -> Copilot | Copilot drawer/store builds workspace, scenario, broker session, and tool inputs; backend orchestrator executes deterministic pipeline. | Complete in source; direct-only explainability input can be missing. |
| Workspace -> Broker | Broker store resolves/creates scenario context; Broker screen sends aligned protected request and can stream SSE. | Complete in source. |
| Flutter auth -> backend | Firebase token exchange, secure stored JWT, Dio bearer injection. | Complete. |
| Flutter valuation -> workspace/Copilot | Flutter valuation and Copilot calls exist, but mobile valuation result save says workspace persistence is not connected. | Partial. |

## Deployment Integration

Present:

- Compose stack includes PostGIS, bootstrap migrations/data load, backend, frontend, health checks, and optional staging smoke profile.
- Nginx proxies `/v1/`, `/health`, and `/health/ready` to backend and adds basic security headers.
- Backend production env requires `JWT_SECRET` and `FIREBASE_PROJECT_ID`.

Blocked or unverified:

- Compose frontend build does not pass Firebase web config build args, so the React login screen is disabled in the checked-in Docker production path.
- Staging smoke was not run in this audit because no seeded Docker/PostGIS/Firebase runtime was started.
- PostGIS integration tests are present but skipped by default unless `RUN_POSTGIS_INTEGRATION=1`.

## Integration Verdict

The source-level integration chain is much stronger than Final V1. React auth, broker, and backend tests are now repaired. The remaining integration risk is concentrated in deployment configuration and snapshot continuity: a direct valuation binds workspace/property state, but market and Copilot explainability depend on protected `ValuationSnapshot` history that direct valuation does not create.
