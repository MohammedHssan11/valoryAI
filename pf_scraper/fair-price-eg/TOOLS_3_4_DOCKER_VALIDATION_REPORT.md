# ValorAI Tools 3 + 4 Docker Validation Report

Report date: 2026-05-31  
Validator: `scripts/validate_copilot_tools_3_4.ps1`  
Decision: **GO**

## Validation Scope

Executed against:

```text
Real Docker Compose stack
Real PostgreSQL + PostGIS
Real JWT ownership layer
Real Router
Real CMT comparable pipeline
Real valuation snapshots
Real Tool Layer
```

Validated:

```text
Comparable Tool real evidence retrieval
Comparable Tool snapshot replay
Comparable Tool scenario retrieval
Fairness Tool below / within / above statuses
Fairness Tool scenario context
Tenant isolation
Tool event persistence
Backend restart recovery
PostgreSQL restart recovery
Migration checksum verification
No Tool Layer pricing logic
No fabricated comparable date
```

## Dedicated Validator Result

Command:

```powershell
.\scripts\validate_copilot_tools_3_4.ps1
```

Result:

```text
workspace_id:                          78
property_id:                           80
scenario_id:                           78
base_comparable_count:                 5
scenario_comparable_count:             5
comparable_source:                     TruthLayer
comparable_item_sources_valid:         true
comparable_ids_present:                true
comparable_reasons_present:            true
compound_name_field_present:           true
listing_date_field_absent:             true
below_fairness_status:                 Below Fair Value
within_fairness_status:                Within Fair Value
above_fairness_status:                 Above Fair Value
fairness_source:                       TruthLayer
scenario_comparable_router_size_sqm:   230.0
scenario_fairness_router_size_sqm:     230.0
fairness_router_target_price_egp:      85000
comparable_tenant_isolation_status:    404
fairness_tenant_isolation_status:      404
comparable_after_backend_restart:      true
tool_events_before_restart:            12
tool_events_after_postgres_restart:    13
comparable_events_before_restart:      2
fairness_events_before_restart:        4
forbidden_tool_logic_references:       0
fabricated_comparable_dates:           0
```

## PostgreSQL Tool Events Evidence

Persisted events for Docker workspace `78`:

```text
id  tool_name   property  scenario  router_size  router_target  valuation_id                             source
79  valuation   80        NULL      220.0        NULL           val_fb4af59ea5eb46f8842c09379b1172be     TruthLayer
80  comparable  80        NULL      NULL         NULL           val_fb4af59ea5eb46f8842c09379b1172be     TruthLayer
81  valuation   80        78        230.0        NULL           val_3595e99f57b0431ea8190639f33e3b76     TruthLayer
82  comparable  80        78        NULL         NULL           val_3595e99f57b0431ea8190639f33e3b76     TruthLayer
83  valuation   80        NULL      220.0        67999          val_1fbbeb2aaa9e4a258bb3ddff08acbc86     TruthLayer
84  fairness    80        NULL      NULL         NULL           val_1fbbeb2aaa9e4a258bb3ddff08acbc86     TruthLayer
85  valuation   80        NULL      220.0        85000          val_e679db289d104f839e20ee3677642e43     TruthLayer
86  fairness    80        NULL      NULL         NULL           val_e679db289d104f839e20ee3677642e43     TruthLayer
87  valuation   80        NULL      220.0        118001         val_f9c32967e4614463b6dc181051a73406     TruthLayer
88  fairness    80        NULL      NULL         NULL           val_f9c32967e4614463b6dc181051a73406     TruthLayer
89  valuation   80        78        230.0        85000          val_d2316e6a9e984d26a3596c4dc5220416     TruthLayer
90  fairness    80        78        NULL         NULL           val_d2316e6a9e984d26a3596c4dc5220416     TruthLayer
91  comparable  80        NULL      NULL         NULL           val_fb4af59ea5eb46f8842c09379b1172be     TruthLayer
```

Event `91` was appended after the backend restart by retrieving the existing
base valuation snapshot. All `13` rows remained available after PostgreSQL and
backend restart.

## Real PostGIS Tests

Command:

```powershell
$env:RUN_POSTGIS_INTEGRATION = "1"
$env:DATABASE_URL = "postgresql+psycopg://fairprice:fairprice@localhost:5432/fairprice"
python -m pytest app/tests/test_copilot_tools_3_4_postgis_integration.py app/tests/test_postgis_integration.py -q
```

Result:

```text
3 passed
```

The integration suite creates real workspace, property, and scenario rows;
routes requests through the live Router and PostGIS CMT pipeline; verifies real
comparable IDs and reason codes; and checks tenant rejection through the HTTP
API.

## Adjacent Docker Regressions

### Tools 1 + 2

```powershell
.\scripts\validate_copilot_tools.ps1
```

Result:

```text
PASS
base_engine:                          CMT
scenario_engine:                      CMT
scenario_router_size_sqm:             230.0
explainability_comparable_count:      5
ml_fallback_engine:                   ML
tenant_isolation_status:              404
explainability_after_backend_restart: true
```

### Broker Adapter

```powershell
.\scripts\validate_broker_adapter.ps1
```

Result:

```text
PASS
broker_valuation_grounding:      passed
broker_valuation_source:         TruthLayer
scenario_router_size_sqm:        230.0
tenant_isolation_status:         404
restart_session_retrieved:       true
direct_pricing_route_references: 0
```

### Persistence Recovery

```powershell
.\scripts\validate_copilot_recovery.ps1
```

Result:

```text
PASS
backend_restart_retrieved:                 true
docker_restart_retrieved:                  true
container_recreate_retrieved:              true
broker_backend_restart_retrieved:          true
broker_postgres_restart_retrieved:         true
broker_container_recreate_retrieved:       true
```

### Migration Replay

```text
python -m app.scripts.run_migrations --verify
PASS: migration_verify_success
```

### Staging Smoke

```powershell
docker compose --profile staging run --rm staging-smoke
```

Result:

```text
readiness:       PASS
openapi:         PASS
valuation:       PASS
invalid payload: PASS
metrics:         PASS
operational:     PASS
```

## Static Boundary Evidence

The dedicated validator scans `copilot_tools_service.py` for forbidden Tool
Layer pricing references:

```text
weighted_median
weighted_quantile
price_listing_cmt
price_listing_ml
synthetic compar
```

Result:

```text
forbidden_tool_logic_references: 0
```

The Router scan verifies that the previous fabricated date marker is absent:

```text
fabricated_comparable_dates: 0
```

## Canonical Stack

After validation:

```text
fair-price-eg-db-1             Up (healthy)
fair-price-eg-db-bootstrap-1   Exited (0)
fair-price-eg-backend-1        Up (healthy)
fair-price-eg-frontend-1       Up (healthy)
```

## Remaining Risks

1. Some real comparables have nullable compound metadata. The API preserves
   null rather than generating a substitute value.
2. Historical local pricing tests retain eight stale monkeypatch targets from
   the earlier pricing-service move.
3. Compose validation proves staging readiness for Tools 3 and 4, not blanket
   production promotion.

## GO / NO-GO

**GO for Tools 3 + 4 Docker validation.**

Comparable evidence is real, fairness remains TruthLayer-owned, tenant
isolation passes, and restart recovery passes.
