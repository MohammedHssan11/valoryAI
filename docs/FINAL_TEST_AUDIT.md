# Final Test Audit

Audit date: 2026-06-10

## Commands Run

| Area | Command | Result |
| --- | --- | --- |
| React typecheck | `npm run lint` in `pf_scraper/fair-price-eg/frontend` | Passed. |
| React tests, invalid flag | `npm test -- --runInBand` in `pf_scraper/fair-price-eg/frontend` | Failed because Vitest does not support Jest's `--runInBand` flag. |
| React tests | `npm test` in `pf_scraper/fair-price-eg/frontend` | Passed: 30 test files, 123 tests. |
| React production build | `npm run build` in `pf_scraper/fair-price-eg/frontend` | Passed. |
| Backend collection | `pytest --collect-only -q` in `pf_scraper/fair-price-eg/backend` | Failed during collection after reporting 204 collected tests and 3 errors. |
| Backend app tests subset | `pytest app/tests -q --ignore=app/tests/test_spatial_confidence.py` in `pf_scraper/fair-price-eg/backend` | 196 passed, 9 skipped, 8 failed. |
| Flutter analysis | `flutter analyze` in `flutter_valorai` | Passed: no issues found. |
| Flutter tests | `flutter test` in `flutter_valorai` | Passed: 11 tests. |

## Backend Test Failures

Collection failures:

| Failure | Root Cause |
| --- | --- |
| `app/tests/test_spatial_confidence.py` | Imports `_combine_confidence` from `app.api.routes.pricing`, but that symbol no longer exists. |
| `backend/test_flow.py` | Executes Postgres-specific SQL during collection against SQLite. |
| `backend/test_union.py` | Executes Postgres/PostGIS-style SQL during collection against SQLite, including unsupported syntax. |

App test failures after ignoring `test_spatial_confidence.py`:

| Failure Group | Root Cause |
| --- | --- |
| `test_api_contract.py`, `test_operational_contracts.py`, `test_valuation_regression.py` | Tests monkeypatch removed symbols such as `pricing_routes.nearest_area`; the pricing route implementation has moved on. |

## Test Quality Findings

1. React typecheck, tests, and build are green, but they do not catch the missing web auth layer.
2. Broker frontend tests encode the wrong payload contract, so they can pass while production requests 422.
3. Backend has broad coverage for Copilot/tools/memory/orchestrator paths, but the full suite is currently not green because stale tests fail collection and stale monkeypatches fail runtime.
4. Flutter has a small but useful verification set. It confirms valuation model mapping, workspace state, token exchange mapping, and Copilot request/response mapping.
5. Current test status is not acceptable for a final enterprise readiness claim because backend collection fails.

## Test Audit Verdict

Frontend and Flutter verification are green. Backend verification is materially blocked by test-suite drift. The platform should not be called fully production-ready until the backend suite collects cleanly and contract tests cover web auth plus broker request shape.
