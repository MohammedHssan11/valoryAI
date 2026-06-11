# Sprint 3 Test Audit

Audit date: 2026-06-11

## Scope

Sprint 3 was limited to backend test suite recovery.

No product features, frontend code, Flutter code, API schemas, endpoints, database schema, Copilot product logic, Broker product logic, or auth product logic were changed.

## Repaired Tests

| File | Repair |
| --- | --- |
| `pf_scraper/fair-price-eg/backend/app/tests/test_spatial_confidence.py` | Replaced stale import from `app.api.routes.pricing` with current `_combine_confidence` implementation in `app.services.valuation_service`. |
| `pf_scraper/fair-price-eg/backend/test_flow.py` | Removed collection-time PostGIS execution; converted script into an integration test gated by `RUN_POSTGIS_INTEGRATION=1`. |
| `pf_scraper/fair-price-eg/backend/test_union.py` | Removed collection-time PostGIS execution; converted script into an integration test gated by `RUN_POSTGIS_INTEGRATION=1`. |
| `pf_scraper/fair-price-eg/backend/app/tests/test_api_contract.py` | Replaced removed route-internal monkeypatches with a route-boundary `price_listing_router` fixture. |
| `pf_scraper/fair-price-eg/backend/app/tests/test_operational_contracts.py` | Replaced removed route-internal monkeypatches with a route-boundary `price_listing_router` fixture. |
| `pf_scraper/fair-price-eg/backend/app/tests/test_valuation_regression.py` | Moved stale route monkeypatches to current `app.services.valuation_service` dependencies and executed the current valuation service directly. |

## Skipped Tests

Remaining skips are explicit PostGIS integration gates.

Full backend suite skip list:

- `app/tests/test_copilot_investment_postgis_integration.py`
- `app/tests/test_copilot_market_insight_postgis_integration.py`
- `app/tests/test_copilot_negotiation_postgis_integration.py`
- `app/tests/test_copilot_tools_3_4_postgis_integration.py`
- `app/tests/test_copilot_what_if_postgis_integration.py`
- `app/tests/test_memory_integration_postgis_integration.py`
- `app/tests/test_postgis_integration.py`
- `app/tests/test_response_composer_postgis_integration.py`
- `app/tests/test_tool_executor_postgis_integration.py`
- `test_flow.py`
- `test_union.py`

Skip condition:

- `RUN_POSTGIS_INTEGRATION=1` must be set with a seeded PostGIS database.

## Stale Imports

Resolved:

- `_combine_confidence` is no longer imported from `app.api.routes.pricing`.

No stale `_combine_confidence` route import remains.

## Stale Monkeypatches

Resolved:

- Tests no longer monkeypatch removed symbols such as `pricing_routes.nearest_area`.
- Route contract tests patch the current `pricing_routes.price_listing_router` endpoint boundary.
- Valuation regression tests patch current `valuation_service.nearest_area` and `valuation_service.fetch_comps` dependencies.

## Database Isolation

Resolved:

- Root PostGIS probes no longer create sessions or execute SQL at module import time.
- SQLite collection is clean.
- PostGIS-only SQL remains behind explicit integration gates.

## Environment Requirements

Default local backend test environment:

- SQLite in-memory app test database via `app/tests/conftest.py`.
- `ENV=test`.
- No PostGIS service required for default suite.

Optional integration environment:

- `RUN_POSTGIS_INTEGRATION=1`
- Seeded PostgreSQL/PostGIS database reachable through `DATABASE_URL`.

## Test Audit Verdict

P0-3 test-suite drift is repaired. Backend collection and default backend execution are clean. Remaining skips are explicit environment-gated PostGIS integration tests, not hidden failures.
