# ValorAI Investment Tool Docker Validation Report

Report date: 2026-06-01  
Validator: `scripts/validate_copilot_investment.ps1`  
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
Real What-if Tool
Real Negotiation Tool
Real Investment Tool
```

Validated:

```text
Strong Opportunity
Moderate Opportunity
Fairly Priced
Caution
High Risk
Scenario investment evaluation
Comparable grounding
Fairness grounding
Negotiation grounding
What-if integration
Insufficient Evidence without optional What-if input
Traceable strengths
Traceable risks
Traceable position rules
No forbidden metric fields
Audit persistence
JWT tenant isolation
Backend restart recovery
PostgreSQL restart recovery
Migration checksum verification
No Tool Layer pricing logic
```

## Dedicated Validator Result

Command:

```powershell
.\scripts\validate_copilot_investment.ps1
```

Result:

```text
workspace_id:                              145
property_id:                               157
sparse_property_id:                        158
scenario_id:                               147
strong_valuation_id:                       val_6dda57250c76480a987c1860a0c69912
moderate_valuation_id:                     val_7f6f3ab0b9464bd58190aa241916228d
fair_valuation_id:                         val_fca2767378ae4885a767c0e9d2173088
caution_valuation_id:                      val_39d3590263f04001983aea868a225fd7
high_risk_valuation_id:                    val_8814a74ef08f421db8df9b7360f8cc26
scenario_valuation_id:                     val_ee0dce1719c142fc91d0bcf3517c68e1
strong_position:                           Strong Opportunity
moderate_position:                         Moderate Opportunity
fair_position:                             Fairly Priced
caution_position:                          Caution
high_risk_position:                        High Risk
strong_confidence:                         High
strong_comparable_count:                   5
moderate_confidence:                       Low
moderate_comparable_count:                 0
high_risk_price_gap_valid:                 true
high_risk_offer_endpoints_grounded:        true
no_what_if_status:                         Insufficient Evidence
no_what_if_source:                         Insufficient Evidence
what_if_status:                            Available
what_if_source:                            TruthLayer
what_if_scenario_grounded:                 true
scenario_router_size_sqm:                  230
scenario_audit_state_id:                   147
all_strengths_traceable:                   true
all_risks_traceable:                       true
all_positions_traceable:                   true
forbidden_metric_fields:                   0
same_snapshot_child_tools:                 true
audit_asking_price_egp:                    118001
audit_investment_position:                 High Risk
tenant_isolation_status:                   404
investment_events_before_restart:          6
investment_events_after_postgres_restart:  7
restart_investment_source:                 TruthLayer
forbidden_tool_logic_references:           0
```

## Position Evidence

The real validator generated:

| Asking evidence | Confidence | Comparable count | Position |
| --- | --- | ---: | --- |
| Mivida asking below fair range | High | 5 | `Strong Opportunity` |
| Central Cairo asking below fair range | Low | 0 | `Moderate Opportunity` |
| Mivida asking equals `fair_price` | High | 5 | `Fairly Priced` |
| Mivida asking exceeds `fair_price` but remains within fair range | High | 5 | `Caution` |
| Mivida asking exceeds fair range | High | 5 | `High Risk` |

## PostgreSQL Audit Evidence

Persisted `investment` rows for workspace `145`:

```text
id   scenario  asking  valuation_id                          fairness           position
564  NULL      67999   val_6dda57250c76480a987c1860a0c69912 Below Fair Value   Strong Opportunity
570  NULL      33650   val_7f6f3ab0b9464bd58190aa241916228d Below Fair Value   Moderate Opportunity
576  NULL      85000   val_fca2767378ae4885a767c0e9d2173088 Within Fair Value  Fairly Priced
582  NULL      85001   val_39d3590263f04001983aea868a225fd7 Within Fair Value  Caution
588  NULL      118001  val_8814a74ef08f421db8df9b7360f8cc26 Above Fair Value   High Risk
601  147       118001  val_ee0dce1719c142fc91d0bcf3517c68e1 Above Fair Value   High Risk
607  NULL      85000   val_cf66bd8210f046a199e22a9e86748d4b Within Fair Value  Fairly Priced
```

Row `607` was appended after backend restart. All rows remained available
after PostgreSQL restart.

## What-if Evidence

The scenario-backed Investment request included:

```json
{
  "scenario_id": 147,
  "what_if_modifications": {
    "bathrooms": 4
  }
}
```

Persisted What-if audit row:

```text
id:                    599
scenario_state_id:     147
modifications:         {"bathrooms": 4}
base_valuation_id:     val_1df564b840504e46968f37b42687c85d
scenario_valuation_id: val_7eb66461c8954e988bf030a2f5813fdd
delta_value:           45000
```

The delta is returned by Tool 5 as sensitivity evidence. It is not converted
into ROI, yield, return, appreciation, or a future-price forecast.

## Live PostGIS Tests

Command:

```powershell
$env:RUN_POSTGIS_INTEGRATION = "1"
$env:DATABASE_URL = "postgresql+psycopg://fairprice:fairprice@localhost:5432/fairprice"
$env:JWT_SECRET = "valorai-local-docker-validation-secret-2026"
python -m pytest backend/app/tests/test_copilot_investment_postgis_integration.py backend/app/tests/test_copilot_negotiation_postgis_integration.py backend/app/tests/test_copilot_what_if_postgis_integration.py backend/app/tests/test_copilot_tools_3_4_postgis_integration.py backend/app/tests/test_postgis_integration.py -q
```

Result:

```text
9 passed
```

## Adjacent Docker Regressions

```text
Tools 1 + 2 validator:           PASS
Tools 3 + 4 validator:           PASS
Standalone What-if validator:   PASS
Negotiation validator:          PASS
Broker Adapter validator:       PASS
Persistence Recovery validator: PASS
Migration checksum verification:PASS
Staging smoke:                  PASS
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

It also recursively scans Investment responses for forbidden metric fields:

```text
roi
irr
cagr
appreciation_forecast
future_price_prediction
rental_yield
investment_returns
```

Result:

```text
forbidden_tool_logic_references: 0
forbidden_metric_fields:         0
```

## Canonical Stack

After validation:

```text
fair-price-eg-db-1        Up (healthy)
fair-price-eg-backend-1   Up (healthy)
fair-price-eg-frontend-1  Up (healthy)
```

## Broader Backend Audit

Focused local suite:

```text
16 passed
```

Executable backend remainder:

```text
114 passed, 5 skipped, 8 failed
```

The eight failures are existing stale monkeypatches targeting members moved
out of `app.api.routes.pricing` before this phase.

Unfiltered backend suite:

```text
BLOCKED during collection
test_spatial_confidence.py imports stale app.api.routes.pricing._combine_confidence
```

## Remaining Risks

1. Sparse TruthLayer evidence remains sparse. Tool 7 returns explicit risk
   disclosure and does not invent comparable replacements.
2. Optional What-if output remains sensitivity evidence only.
3. Historical pricing-route tests still need import and monkeypatch
   maintenance.
4. Compose validation proves phase readiness, not blanket production
   promotion.

## GO / NO-GO

**GO for Investment Tool Docker validation.**

Investment guidance is evidence-backed, tenant isolation passes, audit rows
persist through restart, forbidden financial metrics remain absent, and
TruthLayer remains authoritative.
