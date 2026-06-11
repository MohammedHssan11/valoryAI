# Final V2 Gap Report

Audit date: 2026-06-11

This report lists only gaps verified in the current source. Historical P0s for React auth, broker request shape, and backend test collection are closed.

## P0 Gaps

| ID | Gap | Impact | Complexity | Risk |
| --- | --- | --- | --- | --- |
| P0-1 | Docker Compose frontend build does not inject required Firebase web config. | A production frontend built from current `docker-compose.yml` cannot sign in because React auth requires `VITE_FIREBASE_API_KEY`, `VITE_FIREBASE_AUTH_DOMAIN`, `VITE_FIREBASE_PROJECT_ID`, and `VITE_FIREBASE_APP_ID`. Since all main React routes are protected, this blocks the Docker production web product. | Low | High |

## P1 Gaps

| ID | Gap | Impact | Complexity | Risk |
| --- | --- | --- | --- | --- |
| P1-1 | Direct valuation bridge records a `ToolEvent` but not a protected `ValuationSnapshot`. | Market insight over a direct-only workspace can be empty, and Copilot explainability cannot reference the direct valuation until a protected valuation/tool run creates a valuation id. | Medium | Medium |
| P1-2 | PostGIS integration tests and staging smoke were not executed in this audit. | Local default tests are green, but seeded spatial/database production paths remain unrecertified. | Medium | Medium |
| P1-3 | React auth stores ValorAI access tokens in browser `sessionStorage`. | Acceptable for local/demo MVP, but enterprise security review may require an httpOnly cookie/BFF or stricter token handling. | Medium | Medium |

## P2 Gaps

| ID | Gap | Impact | Complexity | Risk |
| --- | --- | --- | --- | --- |
| P2-1 | Mixed response envelope strategy remains. | Pricing/health/broker use success envelopes; persistence/tools/orchestrator return raw models. Clients are tolerant, but contract generation and drift detection are weaker. | Medium | Medium |
| P2-2 | Market intelligence is internal descriptive analytics, not external market data or forecasting. | Product language can overstate capability if not kept precise. | Low | Medium |
| P2-3 | Flutter lacks parity with React intelligence workflows. | Mobile does not expose what-if, negotiation, investment, market insight, or broker as full UX surfaces. | High | Medium |
| P2-4 | Mobile valuation result persistence is not connected. | Flutter valuation can analyze, but result saving/workspace continuity is still not fully wired. | Medium | Medium |
| P2-5 | React production bundle has a large chunk warning. | Not functionally blocking, but performance optimization is needed before high-scale production polish. | Low | Low |

## P3 Gaps

| ID | Gap | Impact | Complexity | Risk |
| --- | --- | --- | --- | --- |
| P3-1 | Large legacy/moved/untracked documentation and old frontend folders remain. | Reviewers can confuse historical phase artifacts with current truth. | Low | Low |
| P3-2 | Root `.env.example` contains duplicate `FIREBASE_PROJECT_ID` entries. | Minor configuration confusion. | Low | Low |
| P3-3 | Build/test caches and generated artifacts are noisy in git status. | Review noise can hide meaningful changes. | Low | Low |

## Closed Historical P0s

| Historical blocker | Current status |
| --- | --- |
| React protected API auth missing | Closed in source. |
| React broker payload missing `workspace_id` and `scenario_id` | Closed in source. |
| Backend pytest collection/runtime failures | Closed in default local suite. |

## Gap Verdict

The system is much closer to launch quality than Final V1, but it is not fully production-ready. The most urgent current blocker is deployment auth configuration for the React Docker frontend. The most important product-continuity gap is direct valuation snapshot persistence.
