# Sprint 3 Test Discovery

Discovery date: 2026-06-11

## Authoritative Inputs

Read and applied:

- `FINAL_TEST_AUDIT.md`
- `FINAL_GAP_REPORT.md`
- `FINAL_PRODUCT_REVIEW.md`
- `SPRINT1_COMPLETION_REPORT.md`
- `SPRINT2_COMPLETION_REPORT.md`

## Initial Collection Failures

Initial command:

- `pytest --collect-only -q`

Initial result:

- 204 tests reported before interruption.
- 3 collection errors.

Observed collection blockers:

| File | Failure | Root cause |
| --- | --- | --- |
| `app/tests/test_spatial_confidence.py` | `ImportError: cannot import name '_combine_confidence' from app.api.routes.pricing` | Test imported a helper from the old route module location. Current implementation lives in `app.services.valuation_service`. |
| `test_flow.py` | SQLite `OperationalError` during collection | Root-level PostGIS probe executed SQL at module import time. |
| `test_union.py` | SQLite `OperationalError` during collection | Root-level PostGIS probe executed SQL at module import time. |

## Skipped Groups Identified

Existing PostGIS integration tests are intentionally gated by `RUN_POSTGIS_INTEGRATION=1`.

The root-level PostGIS probes were converted to the same pattern:

- `test_flow.py`
- `test_union.py`

They no longer execute database work during collection.

## Stale Imports Identified

- `app/tests/test_spatial_confidence.py` used stale route import for `_combine_confidence`.

## Stale Monkeypatches Identified

The following tests monkeypatched symbols that no longer exist on `app.api.routes.pricing`:

- `app/tests/test_api_contract.py`
- `app/tests/test_operational_contracts.py`
- `app/tests/test_valuation_regression.py`

The current authoritative implementations are:

- Route endpoint wrapper: `app.api.routes.pricing.rent_fair_price`
- Router service boundary: `app.services.router_service.price_listing_router`
- CMT valuation implementation: `app.services.valuation_service.price_listing`
- CMT dependencies: `app.services.valuation_service.nearest_area`, `fetch_comps`, and pricing helpers

## Database Mismatch Identified

- App tests set SQLite test isolation through `app/tests/conftest.py`.
- Root `test_flow.py` and `test_union.py` were outside that scope and imported DB/session code directly at module import.
- Both files used Postgres/PostGIS SQL features unsupported by SQLite, including `ANY(:candidate_aliases)`, `::text`, and `ST_X/ST_Y`.

## Collection Repair Result

After collection repair:

- `pytest --collect-only -q` succeeded.
- 207 tests collected.

## Remaining Discovery Work

Next step is full runtime execution to identify failing groups after collection recovery.
