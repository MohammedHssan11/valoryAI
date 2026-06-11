# Final Gap Report

Audit date: 2026-06-10

## P0 Gaps

| ID | Gap | Impact | Smallest Fix |
| --- | --- | --- | --- |
| P0-1 | React has no backend authentication/token exchange/header injection. | Protected workflows 401: property context, scenarios, Copilot tools, Copilot orchestrator, broker. | Add web auth: Firebase login, `/v1/auth/token-exchange`, secure token storage, Axios bearer header, refresh/expiry, route guards, protected endpoint tests. |
| P0-2 | React broker payload omits backend-required `workspace_id` and `scenario_id`. | Broker reasoning/streaming 422 even after auth. | Align TypeScript contract and `BrokerScreen.buildRequest` with backend, or change backend to create/bind context from valuation input. |
| P0-3 | Backend pytest suite does not collect cleanly. | Cannot claim final enterprise readiness or stable regression safety. | Update/remove stale `_combine_confidence` import and isolate Postgres-only root tests from SQLite collection. |

## P1 Gaps

| ID | Gap | Impact | Fix |
| --- | --- | --- | --- |
| P1-1 | Direct valuation does not create a protected `ValuationSnapshot`. | Explainability/Copilot/market flows cannot reliably continue from the first valuation. | Persist direct valuation under authenticated workspace, or immediately run protected valuation tool after bridge. |
| P1-2 | React property context bridge depends on protected persistence but no auth state exists. | What-if/negotiation/investment UI stays blocked or stale. | Fix P0-1 and add visible auth/context failure states. |
| P1-3 | Market insight is only historical/descriptive from protected workspace records. | Users may expect external market intelligence and see sparse output. | Label clearly, seed from valuation snapshots, or add external market data ingestion. |
| P1-4 | Tests mock invalid broker contract. | Green frontend tests can mask production 422. | Add OpenAPI/schema-derived contract tests. |
| P1-5 | Backend valuation regression tests target removed internals. | Core valuation safety is under-verified despite many passing tests. | Rewrite tests around public service/router contracts. |

## P2 Gaps

| ID | Gap | Impact | Fix |
| --- | --- | --- | --- |
| P2-1 | Mixed success envelopes and raw response models. | Clients need tolerant parsing; drift risk increases. | Standardize response envelope or document raw-tool exception and generate clients. |
| P2-2 | Copilot prerequisite handling is brittle for direct-only users. | Prompts like "explain this valuation" may fail without a protected valuation id. | Add preflight tool input repair or prerequisite valuation execution. |
| P2-3 | React and Flutter are not feature-parity clients. | Product narrative can become confusing. | Choose canonical demo/client scope and document parity roadmap. |
| P2-4 | Scenario deltas and metadata need careful consistency checks. | Stored decision state can become harder to audit. | Add scenario persistence invariant tests. |

## P3 Gaps

| ID | Gap | Impact | Fix |
| --- | --- | --- | --- |
| P3-1 | Large moved/untracked doc archive and legacy clients. | Reviewers may confuse current truth with historical artifacts. | Mark canonical source/docs and archive old copies. |
| P3-2 | Build/test caches and pyc files appear modified in git status. | Noise makes real changes harder to review. | Clean ignored artifacts through `.gitignore` and housekeeping. |
| P3-3 | Some docs overstate completion relative to integration reality. | Demo/business claims risk credibility. | Update master state after P0/P1 fixes. |

## Recommended Repair Sequence

1. Fix React auth and bearer header injection.
2. Fix broker request contract.
3. Make direct valuation create or trigger protected workspace valuation snapshots.
4. Repair backend test collection and stale valuation tests.
5. Add cross-client contract tests from backend schemas/OpenAPI.
6. Re-run full backend, React, Flutter, and Docker smoke verification.

## Gap Verdict

The remaining gaps are concentrated and fixable. They are also fundamental: until P0-1 and P0-2 are closed, the React intelligence platform is a strong UI over protected APIs it cannot actually use.
