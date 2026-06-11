# Sprint 3 Integration Verification

Verification date: 2026-06-11

## Commands

Executed from:

- `pf_scraper/fair-price-eg/backend`

## Results

| Command | Result |
| --- | --- |
| `pytest --collect-only -q` | Passed. 207 tests collected. |
| `pytest -q` | Passed. 205 passed, 11 skipped. |
| `pytest app/tests -q` | Passed. 205 passed, 9 skipped. |
| `pytest app/tests/test_spatial_confidence.py test_flow.py test_union.py app/tests/test_api_contract.py app/tests/test_operational_contracts.py app/tests/test_valuation_regression.py -q` | Passed. 10 passed, 2 skipped. |
| `pytest -q -rs` | Passed. 205 passed, 11 skipped with explicit PostGIS skip reasons. |

## Backend Blocker Verification

| Blocker from `FINAL_TEST_AUDIT.md` | Verification |
| --- | --- |
| Stale `_combine_confidence` route import | Repaired; collection passes. |
| `test_flow.py` executes PostGIS SQL during collection | Repaired; collection passes and test is integration-gated. |
| `test_union.py` executes PostGIS SQL during collection | Repaired; collection passes and test is integration-gated. |
| Stale `pricing_routes.nearest_area` monkeypatches | Repaired; targeted suites pass. |
| Backend suite does not collect cleanly | Repaired; `pytest --collect-only -q` passes. |
| Backend suite does not execute cleanly | Repaired; `pytest -q` passes. |

## Skip Verification

Default full-suite skips:

- 9 existing app-level PostGIS integration tests.
- 2 root-level PostGIS probes repaired during Sprint 3.

All remaining skips require `RUN_POSTGIS_INTEGRATION=1` with seeded PostGIS data.

## Integration Verdict

Backend default test suite collection and execution are clean. P0-3 is verified closed for the default backend suite.
