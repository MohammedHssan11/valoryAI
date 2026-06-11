# ValorAI Negotiation Tool Docker Validation Report

Report date: 2026-06-01  
Validator: `scripts/validate_copilot_negotiation.ps1`  
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
```

Validated:

```text
Below Fair Value negotiation
Within Fair Value negotiation
Above Fair Value negotiation
Scenario-backed negotiation
Comparable-backed offer band
Fairness grounding
What-if-backed negotiation
Traceable broker talking points
Traceable risk notes
Traceable position rules
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
.\scripts\validate_copilot_negotiation.ps1
```

Result:

```text
workspace_id:                         124
property_id:                          127
scenario_id:                          126
below_valuation_id:                   val_7476bfa917544d058024d146c0e65da5
within_valuation_id:                  val_40ce15e3b8f345178e3c20e286107c24
above_valuation_id:                   val_45eff17be47343919b0c7b30343652fa
scenario_valuation_id:                val_8d1dda42c9474fdcaee29a12a2e062ea
below_fairness_status:                Below Fair Value
within_fairness_status:               Within Fair Value
above_fairness_status:                Above Fair Value
below_negotiation_position:           Strong Buy Opportunity
within_negotiation_position:          Fair Market Position
above_negotiation_position:           Overpriced
below_offer_band_is_empty:            true
within_offer_band_reuses_fair_price:  true
above_offer_low:                      75000
above_offer_high:                     85000
above_offer_endpoints_grounded:       true
above_comparable_count:               5
above_price_gap_valid:                true
all_talking_points_traceable:         true
all_risk_notes_traceable:             true
all_positions_traceable:              true
same_snapshot_child_tools:            true
above_router_target_price_egp:        118001
above_fairness_reuses_valuation_id:   true
audit_asking_price_egp:               118001
audit_fairness_status:                Above Fair Value
audit_negotiation_position:           Overpriced
scenario_router_size_sqm:             230
what_if_source:                       TruthLayer
what_if_scenario_grounded:            true
what_if_negotiation_integrated:       true
tenant_isolation_status:              404
negotiation_events_before_restart:    4
negotiation_events_after_restart:     5
restart_negotiation_source:           TruthLayer
forbidden_tool_logic_references:      0
```

## Offer-Band Evidence

The real Above Fair Value package returned:

```text
asking_price:              118001 EGP
fair_price:                85000 EGP
returned comparable count: 5
offer_band.low:            75000 EGP
offer_band.high:           85000 EGP
```

The low endpoint is a returned comparable price at or below `fair_price`.
The high endpoint is the authoritative TruthLayer `fair_price`. The
validator asserts both endpoints are members of:

```text
{ fair_price } union { returned comparable prices }
```

## What-if Evidence

The scenario-backed negotiation request included:

```json
{
  "scenario_id": 126,
  "what_if_modifications": {
    "bathrooms": 4
  }
}
```

Persisted What-if audit row:

```text
id:                    271
scenario_state_id:     126
modifications:         {"bathrooms": 4}
base_valuation_id:     val_eb4cb4e42c124f998b5be420ac6aa4ed
scenario_valuation_id: val_a49485a0a1ab4fe790770d164f9f95bc
delta_value:           45000
```

The delta is returned by Tool 5 as sensitivity evidence. It is not used to
invent offer-band endpoints.

## PostgreSQL Audit Evidence

Persisted `negotiation` rows for workspace `124`:

```text
id   scenario  asking  valuation_id                          fairness           position
250  NULL      67999   val_7476bfa917544d058024d146c0e65da5 Below Fair Value   Strong Buy Opportunity
255  NULL      85000   val_40ce15e3b8f345178e3c20e286107c24 Within Fair Value  Fair Market Position
260  NULL      118001  val_45eff17be47343919b0c7b30343652fa Above Fair Value   Overpriced
272  126       118001  val_8d1dda42c9474fdcaee29a12a2e062ea Above Fair Value   Overpriced
277  NULL      85000   val_1d8d734d580e459da56e73e416815c73 Within Fair Value  Fair Market Position
```

Row `277` was appended after backend restart. All rows remained available
after PostgreSQL restart.

## Live PostGIS Tests

Command:

```powershell
$env:RUN_POSTGIS_INTEGRATION = "1"
$env:DATABASE_URL = "postgresql+psycopg://fairprice:fairprice@localhost:5432/fairprice"
$env:JWT_SECRET = "valorai-local-docker-validation-secret-2026"
python -m pytest backend/app/tests/test_copilot_negotiation_postgis_integration.py backend/app/tests/test_copilot_what_if_postgis_integration.py backend/app/tests/test_copilot_tools_3_4_postgis_integration.py backend/app/tests/test_postgis_integration.py -q
```

Result:

```text
7 passed
```

## Adjacent Docker Regressions

```text
Tools 1 + 2 validator:          PASS
Tools 3 + 4 validator:          PASS
Standalone What-if validator:  PASS
Broker Adapter validator:      PASS
Persistence Recovery validator:PASS
Migration replay:              PASS
Staging smoke:                 PASS
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

## Broader Backend Audit

Focused local suite:

```text
7 passed
```

Executable backend remainder:

```text
113 passed, 4 skipped, 8 failed
```

The eight failures are existing stale monkeypatches targeting members moved
out of `app.api.routes.pricing` before this phase.

Unfiltered backend suite:

```text
BLOCKED during collection
test_spatial_confidence.py imports stale app.api.routes.pricing._combine_confidence
```

## Remaining Risks

1. Sparse TruthLayer comparables remain sparse. The Negotiation Tool does not
   invent comparable replacements.
2. Optional What-if results are sensitivity disclosures, not alternate offer
   prices.
3. Historical pricing-route tests still need import and monkeypatch
   maintenance.
4. Compose validation proves phase readiness, not blanket production
   promotion.

## GO / NO-GO

**GO for Negotiation Tool Docker validation.**

Negotiation guidance is evidence-backed, offer endpoints are grounded, JWT
tenant isolation passes, audit rows persist through restart, and TruthLayer
remains authoritative.
