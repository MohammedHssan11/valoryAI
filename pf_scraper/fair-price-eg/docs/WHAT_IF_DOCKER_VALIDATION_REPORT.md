# ValorAI What-if Docker Validation Report

Report date: 2026-05-31  
Validator: `scripts/validate_copilot_what_if.ps1`  
Decision: **GO**

## Validation Scope

Executed against:

```text
Real Docker Compose stack
Real PostgreSQL + PostGIS
Real JWT ownership layer
Real Router
Real CMT and ML routing infrastructure
Real Valuation Tool
Real Explainability Tool
Real Comparable Tool
Real Fairness Tool
Real Tool Layer
```

Validated:

```text
Base property immutability
Ephemeral scenario sandbox
Size modification
Bedroom modification
Amenity modification
Scenario-on-scenario modification
TruthLayer-derived delta calculation
Fresh Comparable Tool evaluation
Fresh Fairness Tool evaluation
Assumptions disclosure
What-if audit persistence
JWT tenant isolation
Backend restart recovery
PostgreSQL restart recovery
Migration checksum verification
No Tool Layer pricing logic
```

## Dedicated Validator Result

Command:

```powershell
.\scripts\validate_copilot_what_if.ps1
```

Result:

```text
workspace_id:                         115
property_id:                          117
existing_scenario_id:                 116
base_valuation_id:                    val_055eb70cb54e4b458a2e93b364deb587
scenario_valuation_id:                val_bea86387ad8e410e8280b2e0b50d0bdb
fairness_valuation_id:                val_03b6e72be63f4181840d076a6d9ec2ef
base_valuation:                       85000
scenario_valuation:                   85000
delta_value:                          0
delta_calculation_valid:              true
source:                               TruthLayer
explainability_source:                TruthLayer
comparable_source:                    TruthLayer
comparable_count:                     5
comparable_refresh_valuation_id:      val_bea86387ad8e410e8280b2e0b50d0bdb
fairness_refresh_is_distinct:         true
base_router_size_sqm:                 230.0
bedroom_router_bedrooms:              3
amenity_router_has_parking:           true
fairness_router_target_price_egp:     85000
scenario_base_router_size_sqm:        225.0
scenario_router_size_sqm:             225.0
scenario_router_bathrooms:            4
scenario_router_has_gym:              true
scenario_fairness_router_has_gym:     true
base_property_area_unchanged:         true
base_property_bedrooms_unchanged:     true
base_property_amenities_unchanged:    true
existing_scenario_unchanged:          true
base_modified_features:               Size
bedroom_amenity_added_features:       Parking
bedroom_amenity_modified_features:    Bedrooms
scenario_added_features:              Gym
scenario_modified_features:           Bathrooms
assumptions_include_furnished_unknown:true
tenant_isolation_status:              404
what_if_events_before_restart:        3
what_if_events_after_postgres_restart:4
restart_what_if_source:               TruthLayer
forbidden_tool_logic_references:      0
```

The size-only case intentionally proves fresh comparable retrieval with real
evidence depth. Bedroom and amenity overlays are validated independently so a
sparse compounded scenario does not turn an evidence-depth limitation into a
false implementation failure.

## Scenario Sandbox Evidence

Persisted snapshots for Docker workspace `115`:

```text
valuation_id                          scenario  size  beds  baths  amenities          target
val_055eb70cb54e4b458a2e93b364deb587  NULL      220   4     3      BA, SE             NULL
val_bea86387ad8e410e8280b2e0b50d0bdb  NULL      230   4     3      BA, SE             NULL
val_03b6e72be63f4181840d076a6d9ec2ef  NULL      230   4     3      BA, SE             85000
val_069de7e909654863af19260057c1fb7f  NULL      220   4     3      BA, SE             NULL
val_f5194d766ada4634bacb68ba176c4dc9  NULL      220   3     3      BA, CP, SE         NULL
val_0cd0e0e2a2b34a7faebb783119d2894b  NULL      220   3     3      BA, CP, SE         85000
val_f64e7bcc9c8d4002b86cd7a3238dd65c  116       225   4     3      BA, SE             NULL
val_01984ace1a9e4556a8379145972d51fb  116       225   4     4      BA, SE, SY         NULL
val_d7e2fb30487442c3b2dce23c81e0b6df  116       225   4     4      BA, SE, SY         85000
```

This demonstrates:

```text
Base Property            220 sqm, 4 beds, 3 baths, BA + SE
Size Sandbox             230 sqm
Bedroom + Parking Sandbox 3 beds, BA + CP + SE
Existing Scenario        225 sqm
Scenario-on-Scenario     225 sqm, 4 baths, BA + SE + SY
```

The persisted base property remained:

```text
area:      220
bedrooms:  4
amenities: BA, SE
```

The persisted existing scenario remained:

```json
{
  "size_sqm": 225
}
```

## PostgreSQL Audit Evidence

Selected `what_if` rows for Docker workspace `115`:

```text
id   scenario  sandbox_modifications              base_valuation_id                     scenario_valuation_id                 delta
160  NULL      {"size_sqm": 230}                  val_055eb70cb54e4b458a2e93b364deb587  val_bea86387ad8e410e8280b2e0b50d0bdb  0
167  NULL      {"parking": true, "bedrooms": 3}   val_069de7e909654863af19260057c1fb7f  val_f5194d766ada4634bacb68ba176c4dc9  -291
174  116       {"gym": true, "bathrooms": 4}      val_f64e7bcc9c8d4002b86cd7a3238dd65c  val_01984ace1a9e4556a8379145972d51fb  45000
181  116       {"bathrooms": 4}                   val_9f08d31657cd4d858f66a57d7e44cc8a  val_d1fe2fddecdd4e2d87f350c1c6124fb0  45000
```

Rows `154..181` also contain the orchestrated child events:

```text
valuation
valuation
explainability
comparable
valuation
fairness
what_if
```

Row `181` was appended after backend restart. All four `what_if` rows remained
available after PostgreSQL and backend restart.

## Live PostGIS Tests

Command:

```powershell
$env:RUN_POSTGIS_INTEGRATION = "1"
$env:DATABASE_URL = "postgresql+psycopg://fairprice:fairprice@localhost:5432/fairprice"
$env:JWT_SECRET = "valorai-local-docker-validation-secret-2026"
python -m pytest app/tests/test_copilot_what_if_postgis_integration.py app/tests/test_copilot_tools_3_4_postgis_integration.py app/tests/test_postgis_integration.py -q
```

Result:

```text
5 passed
```

The suite creates real workspace, property, and scenario rows; routes through
the live Router and PostGIS pipeline; verifies fresh valuation IDs; verifies
the real comparable snapshot; checks scenario-on-scenario input propagation;
checks immutable persisted state; and rejects a cross-tenant HTTP request.

## Adjacent Docker Regressions

### Tools 1 + 2

```powershell
.\scripts\validate_copilot_tools.ps1
```

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

### Tools 3 + 4

```powershell
.\scripts\validate_copilot_tools_3_4.ps1
```

```text
PASS
base_comparable_count:                 5
scenario_comparable_count:             5
below_fairness_status:                 Below Fair Value
within_fairness_status:                Within Fair Value
above_fairness_status:                 Above Fair Value
comparable_tenant_isolation_status:    404
fairness_tenant_isolation_status:      404
tool_events_after_postgres_restart:    13
fabricated_comparable_dates:           0
```

### Broker Adapter

```powershell
.\scripts\validate_broker_adapter.ps1
```

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

```text
PASS
readiness
openapi
valuation
invalid payload
metrics
operational
```

## Backend Regression Audit

Focused local suite:

```text
6 passed
```

Wider executable suite:

```text
112 passed, 3 skipped, 8 failed
```

The eight failures are existing stale monkeypatches targeting members that
moved out of `app.api.routes.pricing` before this phase.

Unfiltered suite:

```text
BLOCKED during collection
test_spatial_confidence.py imports stale app.api.routes.pricing._combine_confidence
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

## Canonical Stack

After validation:

```text
fair-price-eg-db-1             Up (healthy)
fair-price-eg-db-bootstrap-1   Exited (0)
fair-price-eg-backend-1        Up (healthy)
fair-price-eg-frontend-1       Up (healthy)
```

## Remaining Risks

1. Feature-rich compounded scenarios can produce sparse or zero retained
   comparable evidence. The API truthfully returns the evidence depth.
2. Historical pricing tests retain stale imports and monkeypatch targets from
   the earlier pricing-service extraction.
3. Compose validation proves staging-grade phase readiness, not full
   production promotion.

## GO / NO-GO

**GO for What-if Docker validation.**

The sandbox is ephemeral, TruthLayer is authoritative, comparable and fairness
refreshes are real, tenant isolation passes, and audit events persist through
restart.
