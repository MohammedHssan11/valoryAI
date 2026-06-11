# ValorAI Market Insight Tool Docker Validation Report

Report date: 2026-06-01  
Validator: `scripts/validate_copilot_market_insight.ps1`  
Decision: **GO**

## Validation Scope

Executed against:

```text
Real Docker Compose stack
Real PostgreSQL + PostGIS
Real JWT ownership layer
Real Router
Real CMT and ML routing infrastructure
Real Prediction Logs
Real Shadow Logs
Real Historical Valuation Snapshots
Real Comparable Evidence
Real Tool Events
Real Workspace History
Real Market Insight Tool
```

Validated:

```text
Market summary generation
Compound insight
H3 area insight
Property-type insight
Historical 30-day retrieval
Confidence distribution
Fair-value distribution
Comparable density
Empty-evidence handling
Statement traceability
Audit persistence
JWT tenant isolation
Backend restart recovery
PostgreSQL restart recovery
Migration checksum verification
Analytics index verification
No forecasting fields
No future or synthetic summary language
```

## Dedicated Validator Result

Command:

```powershell
.\scripts\validate_copilot_market_insight.ps1
```

Result:

```text
workspace_id:                          176
mivida_apartment_property_id:          187
mivida_villa_property_id:              188
cairo_apartment_property_id:           189
mivida_apartment_valuation_id:         val_4ec3ed5dc2004851a6a7ac90d09263e2
mivida_villa_valuation_id:             val_a03f13aa9bd94e65a90919e023fa9169
cairo_apartment_valuation_id:          val_d2cac4fa777a457380d25fc5831b051f
h3_res9:                               893e62ba837ffff
overall_valuation_volume:              3
overall_prediction_log_count:          3
overall_shadow_log_count:              3
overall_snapshot_count:                3
overall_confidence_count:              3
overall_comparable_density:            High
most_active_compound:                  Mivida
most_active_compound_volume:           2
active_area_count:                     2
compound_filter_volume:                2
h3_filter_volume:                      2
property_type_filter_volume:           1
history_30d_volume:                    3
empty_filter_volume:                   0
empty_filter_density:                  Insufficient Evidence
required_sources_used:                 true
all_statements_traceable:              true
forbidden_metric_fields:               0
forbidden_summary_language:            0
audit_filters_persisted:               true
audit_sources_persisted:               true
market_events_before_restart:          6
market_events_after_postgres_restart:  8
backend_restart_volume:                3
postgres_restart_volume:               3
tenant_isolation_status:               404
analytics_index_count:                 2
```

## Persisted Monitoring Evidence

Joined rows from `prediction_logs` and `shadow_logs`:

```text
request_id                            compound  property_type  h3_res9          comparable_count  engine
val_4ec3ed5dc2004851a6a7ac90d09263e2 Mivida    Apartment      893e62ba837ffff  91                ML
val_a03f13aa9bd94e65a90919e023fa9169 Mivida    Villa          893e62ba837ffff  13                CMT
val_d2cac4fa777a457380d25fc5831b051f           Apartment                        0                 ML
```

The Market Insight response uses persisted history only. No Router, ML, or
CMT execution occurs inside Tool 8.

## PostgreSQL Audit Evidence

Persisted `market_insight` rows for workspace `176`:

```text
id   filters                                                        valuation_volume
703  workspace_id=176, time_window=all                              3
704  workspace_id=176, compound_name=Mivida, time_window=all        2
705  workspace_id=176, h3_res9=893e62ba837ffff, time_window=all     2
706  workspace_id=176, property_type=Villa, time_window=all         1
707  workspace_id=176, time_window=30d                              3
708  workspace_id=176, compound_name=No Persisted Compound          0
709  workspace_id=176, time_window=all                              3
710  workspace_id=176, time_window=all                              3
```

Rows `709` and `710` were appended after backend and PostgreSQL restarts.

## Migration Evidence

Applied migration:

```text
008_market_insight_analytics_indexes.sql
applied_at: 2026-05-31 22:58:52.816297+00
```

Verified indexes:

```text
ix_prediction_logs_market_filters
ix_shadow_logs_market_filters
```

## Live PostGIS Tests

Command:

```powershell
$env:RUN_POSTGIS_INTEGRATION = "1"
$env:DATABASE_URL = "postgresql+psycopg://fairprice:fairprice@localhost:5432/fairprice"
$env:JWT_SECRET = "valorai-local-docker-validation-secret-2026"
python -m pytest `
  backend/app/tests/test_copilot_market_insight_postgis_integration.py `
  backend/app/tests/test_copilot_investment_postgis_integration.py `
  backend/app/tests/test_copilot_negotiation_postgis_integration.py `
  backend/app/tests/test_copilot_what_if_postgis_integration.py `
  backend/app/tests/test_copilot_tools_3_4_postgis_integration.py `
  backend/app/tests/test_postgis_integration.py -q
```

Result:

```text
10 passed
```

## Adjacent Docker Regressions

```text
Tools 1 + 2 validator:           PASS
Tools 3 + 4 validator:           PASS
Standalone What-if validator:   PASS
Negotiation validator:          PASS
Investment validator:           PASS
Broker Adapter validator:       PASS
Persistence Recovery validator: PASS
Migration checksum verification:PASS
Staging smoke:                  PASS
```

## Static Boundary Evidence

The dedicated validator recursively scans Market Insight responses for
forbidden output fields:

```text
forecast
future_price
expected_appreciation
predicted_inflation
predicted_return
synthetic_trend
```

It also scans generated summaries for:

```text
forecast
future
predict
appreciation
expected return
trend
```

Result:

```text
forbidden_metric_fields:     0
forbidden_summary_language:  0
```

## Canonical Stack

After validation:

```text
fair-price-eg-db-1        Up (healthy)
fair-price-eg-backend-1   Up (healthy)
fair-price-eg-frontend-1  Up (healthy)
```

## Broader Backend Audit

Focused local suites:

```text
23 passed
```

Executable backend remainder:

```text
114 passed, 6 skipped, 8 failed
```

The eight failures are existing stale monkeypatches targeting members moved
out of `app.api.routes.pricing` before this phase.

Unfiltered backend suite:

```text
BLOCKED during collection
test_spatial_confidence.py imports stale app.api.routes.pricing._combine_confidence
```

## Remaining Risks

1. Immediate Tool Layer monitoring persistence adds synchronous valuation
   latency so Tool 8 can read complete historical records immediately.
2. Sparse observations remain sparse and are reported as such.
3. Historical pricing-route tests still need import and monkeypatch
   maintenance.
4. Compose validation proves phase readiness, not blanket production
   promotion.

## GO / NO-GO

**GO for Market Insight Tool Docker validation.**

Market summaries are persisted-data observations only, tenant isolation
passes, audit rows survive restart, and no forecasting output exists.
