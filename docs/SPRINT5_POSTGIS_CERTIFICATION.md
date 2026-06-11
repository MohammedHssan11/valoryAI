# Sprint 5 PostGIS Certification

Date: 2026-06-11

## Database Evidence

Live Docker database:

- Image: `postgis/postgis:16-3.4`
- PostGIS version: `3.4 USE_GEOS=1 USE_PROJ=1 USE_STATS=1`
- Listings: `62608`
- Areas: `3104`

Bootstrap:

- `db-bootstrap` exited `0`.
- Migration verification passed.
- Import QC found `0` orphan area refs.

## Integration Command

Executed with `RUN_POSTGIS_INTEGRATION=1`:

```text
python -m pytest -p no:cacheprovider
  app/tests/test_postgis_integration.py
  app/tests/test_tool_executor_postgis_integration.py
  app/tests/test_memory_integration_postgis_integration.py
  app/tests/test_copilot_tools_3_4_postgis_integration.py
  app/tests/test_copilot_what_if_postgis_integration.py
  app/tests/test_copilot_negotiation_postgis_integration.py
  app/tests/test_copilot_investment_postgis_integration.py
  app/tests/test_copilot_market_insight_postgis_integration.py
  app/tests/test_response_composer_postgis_integration.py
  test_flow.py
  test_union.py
```

Result:

- `17 passed in 14.41s`

## Required Areas

| Area | Result |
| --- | --- |
| Spatial confidence | PASS |
| Market intelligence | PASS |
| Negotiation | PASS |
| Investment | PASS |
| Memory integration | PASS |
| Tool execution | PASS |
| Response composer | PASS |
| Direct PostGIS valuation pipeline | PASS |

## PostGIS Certification Verdict

PASS.
