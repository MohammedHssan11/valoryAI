# ValorAI Phase 5.5B.5 Negotiation Tool Implementation Report

Report date: 2026-06-01  
Scope: Tool 6 Negotiation Tool only  
Decision: **GO**

## Executive Result

Implemented only:

```text
Tool 6: Negotiation Tool
```

No Investment Tool, Market Insight Tool, Copilot Orchestrator, LLM
integration, Flutter frontend, pricing engine, valuation estimator, direct
Router call, direct ML call, or direct CMT call was added.

The Negotiation Tool is a deterministic orchestration adapter. TruthLayer
remains authoritative.

## Architecture

```text
JWT Actor
  -> Negotiation Tool API
  -> tenant-scoped Workspace / Property / optional Scenario resolution
  -> Valuation Tool with asking_price_egp as TruthLayer target
  -> Explainability Tool for the same valuation snapshot
  -> Comparable Tool for the same valuation snapshot
  -> Fairness Tool for the same valuation snapshot
  -> optional What-if Tool sensitivity analysis
  -> TruthLayer-grounded negotiation package
  -> persisted negotiation tool_event
```

The Negotiation Tool invokes existing Tool Layer adapters only:

```text
execute_valuation
execute_explainability
execute_comparable
execute_fairness
execute_what_if, when what_if_modifications are supplied
```

## Contract

Endpoint:

```text
POST /v1/copilot/tools/negotiation
```

Input:

```json
{
  "workspace_id": 124,
  "property_id": 127,
  "scenario_id": 126,
  "asking_price_egp": 118001,
  "what_if_modifications": {
    "bathrooms": 4
  }
}
```

`scenario_id` and `what_if_modifications` are optional. Empty What-if
modifications are rejected.

Output:

```text
tool_name
valuation_id
asking_price
fair_price
fairness_status
price_gap
price_gap_percentage
confidence_level
confidence_reason
negotiation_position
negotiation_position_reason
negotiation_position_evidence
recommended_offer_band
broker_talking_points
evidence_summary
comparable_summary
risk_notes
what_if_analysis, when requested
timestamp
source = TruthLayer
```

## Position Rules

All five permitted positions are implemented through explicit evidence rules:

| TruthLayer evidence | Negotiation position |
| --- | --- |
| Fairness is `Below Fair Value` | `Strong Buy Opportunity` |
| Fairness is `Within Fair Value` and asking price does not exceed `fair_price` | `Fair Market Position` |
| Fairness is `Within Fair Value`, asking exceeds `fair_price`, and a returned comparable reaches the asking price | `Premium Justified` |
| Fairness is `Within Fair Value`, asking exceeds `fair_price`, and no returned comparable reaches the asking price | `Negotiation Recommended` |
| Fairness is `Above Fair Value` | `Overpriced` |

Every returned position includes a reason and evidence references.

## Offer Band Derivation

The recommended offer band uses only `fair_price`, `fairness_status`, and
returned comparable evidence:

| Fairness status | Offer band derivation |
| --- | --- |
| `Below Fair Value` | No numeric counter-offer band is emitted. |
| `Within Fair Value` | Both endpoints reuse authoritative `fair_price`. |
| `Above Fair Value` with lower comparable support | Low endpoint is the highest returned comparable price at or below `fair_price`; high endpoint is `fair_price`. |
| `Above Fair Value` without lower comparable support | Both endpoints reuse authoritative `fair_price`. |

No discounts, percentages, synthetic comparable prices, or hidden pricing
formulas are used.

## Evidence Traceability

Each broker talking point, risk note, position, and offer band includes
structured references to one or more of:

```text
valuation
explainability
comparable
fairness
what_if
```

The optional What-if result is sensitivity evidence only. It is disclosed in
the package but cannot introduce offer-band endpoints or replace the current
TruthLayer valuation snapshot.

## Audit Trail

No migration was required. The existing durable `tool_events` table stores:

```text
user_id
workspace_id
property_state_id
scenario_state_id
tool_name = negotiation
payload.request.asking_price_egp
payload.response.valuation_id
payload.response.fairness_status
payload.response.negotiation_position
created_at
```

The route resolves the JWT actor through the existing ownership layer. No
caller-supplied user ID is accepted.

## Files Modified

```text
backend/app/api/schemas/copilot_tools.py
backend/app/services/copilot_tools_service.py
backend/app/tests/test_copilot_tools.py
backend/app/tests/test_copilot_negotiation_postgis_integration.py
scripts/validate_copilot_negotiation.ps1
```

## Files Created

```text
PHASE_5_5B_5_NEGOTIATION_TOOL_IMPLEMENTATION_REPORT.md
NEGOTIATION_TOOL_DOCKER_VALIDATION_REPORT.md
```

## Docker Evidence

Dedicated validator:

```powershell
.\scripts\validate_copilot_negotiation.ps1
```

Result:

```text
workspace_id:                         124
property_id:                          127
scenario_id:                          126
below_fairness_status:                Below Fair Value
within_fairness_status:               Within Fair Value
above_fairness_status:                Above Fair Value
below_negotiation_position:           Strong Buy Opportunity
within_negotiation_position:          Fair Market Position
above_negotiation_position:           Overpriced
above_offer_low:                      75000
above_offer_high:                     85000
above_offer_endpoints_grounded:       true
above_comparable_count:               5
all_talking_points_traceable:         true
all_risk_notes_traceable:             true
all_positions_traceable:              true
same_snapshot_child_tools:            true
what_if_source:                       TruthLayer
what_if_scenario_grounded:            true
what_if_negotiation_integrated:       true
tenant_isolation_status:              404
negotiation_events_before_restart:    4
negotiation_events_after_restart:     5
restart_negotiation_source:           TruthLayer
forbidden_tool_logic_references:      0
```

## Test Results

```text
python -m compileall -q backend/app
PASS

PowerShell parser: scripts/validate_copilot_negotiation.ps1
PASS

docker compose config --quiet
PASS

Focused local suite
7 passed

Live seeded PostGIS suite
7 passed

Dedicated Negotiation Docker validator
PASS

Tools 1 + 2 Docker validator
PASS

Tools 3 + 4 Docker validator
PASS

Standalone What-if Docker validator
PASS

Broker Adapter Docker validator
PASS

Persistence Recovery Docker validator
PASS

Migration checksum verification
PASS

Staging smoke
PASS
```

Broader backend audit:

```text
Unfiltered suite: blocked during collection by the pre-existing stale
test_spatial_confidence.py import from app.api.routes.pricing.

Executable remainder:
113 passed, 4 skipped, 8 failed
```

The eight executable failures are the previously documented stale pricing
route monkeypatch targets. They are not introduced by Tool 6.

## Remaining Risks

1. Sparse TruthLayer comparable results intentionally produce sparse
   negotiation evidence. The Tool does not invent replacements.
2. Optional What-if output is sensitivity evidence, not an alternate source
   of offer prices.
3. Historical pricing tests still need maintenance after the earlier
   pricing-service extraction.
4. Docker Compose validation proves phase readiness, not blanket production
   promotion.

## Readiness Score

| Layer | Score | Result |
| --- | ---: | --- |
| TruthLayer authority | 10 / 10 | No Tool 6 pricing, ML, CMT, or Router shortcut |
| Offer-band grounding | 10 / 10 | Endpoints reuse fair price and returned comparable prices only |
| Evidence traceability | 10 / 10 | Positions, talking points, risks, and bands carry references |
| Scenario support | 10 / 10 | Persisted scenario state verified |
| Optional What-if integration | 10 / 10 | Nested sensitivity analysis verified |
| JWT tenant isolation | 10 / 10 | Cross-tenant negotiation returns 404 |
| Audit and recovery | 10 / 10 | Durable events survive backend and PostgreSQL restart |
| Regression confidence | 9 / 10 | Dedicated, adjacent, PostGIS, and smoke validations pass |

**Readiness: 79 / 80 = 98.75 / 100**

## GO / NO-GO

**GO for Phase 5.5B.5 Negotiation Tool.**

The implementation builds evidence-backed negotiation guidance, not
valuation. TruthLayer remains authoritative.
