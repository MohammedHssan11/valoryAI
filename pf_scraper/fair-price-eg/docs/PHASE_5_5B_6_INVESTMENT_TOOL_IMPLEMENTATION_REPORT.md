# ValorAI Phase 5.5B.6 Investment Tool Implementation Report

Report date: 2026-06-01  
Scope: Tool 7 Investment Tool only  
Decision: **GO**

## Executive Result

Implemented only:

```text
Tool 7: Investment Tool
```

No Market Insight Tool, Copilot Orchestrator, LLM integration, frontend,
pricing engine, valuation estimator, forecast engine, direct Router call,
direct ML call, or direct CMT call was added.

The Investment Tool is an evidence-backed orchestration adapter. TruthLayer
remains authoritative.

## Architecture

```text
JWT Actor
  -> Investment Tool API
  -> tenant-scoped Workspace / Property / optional Scenario resolution
  -> Negotiation Tool
  -> Valuation Tool
  -> Explainability Tool
  -> Comparable Tool
  -> Fairness Tool
  -> optional What-if Tool sensitivity analysis
  -> evidence-backed investment package
  -> persisted investment tool_event
```

Tool 7 invokes the existing Tool 6 adapter. Tool 6 supplies the governed
Tools 1-5 evidence chain. Tool 7 does not call TruthLayer Router, ML, or CMT
directly.

## Contract

Endpoint:

```text
POST /v1/copilot/tools/investment
```

Input:

```json
{
  "workspace_id": 145,
  "property_id": 157,
  "scenario_id": 147,
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
investment_position
investment_position_reason
investment_position_evidence
confidence_level
confidence_reason
investment_summary
strengths
risks
evidence_summary
comparable_summary
negotiation_summary
what_if_summary
timestamp
source = TruthLayer
```

When no optional What-if request is supplied:

```text
what_if_summary.status = Insufficient Evidence
what_if_summary.source = Insufficient Evidence
```

## Position Rules

All five permitted positions use explicit evidence rules:

| TruthLayer evidence | Investment position |
| --- | --- |
| `Below Fair Value`, `High` confidence, and returned comparable support | `Strong Opportunity` |
| `Below Fair Value` with limited confidence or comparable support | `Moderate Opportunity` |
| `Within Fair Value` and asking price does not exceed `fair_price` | `Fairly Priced` |
| `Within Fair Value` and asking price exceeds `fair_price` | `Caution` |
| `Above Fair Value` | `High Risk` |

No synthetic investment score or hidden formula is used.

## Evidence Traceability

Every position, strength, and risk carries structured references to one or
more permitted evidence sources:

```text
valuation
explainability
comparable
fairness
negotiation
what_if
```

The package reuses Tool 6 evidence summaries, comparable summaries, grounded
offer bands, and broker talking points. Optional What-if output remains
sensitivity evidence only.

## Forbidden Outputs

Tool 7 does not generate:

```text
ROI
IRR
CAGR
appreciation forecasts
future-price predictions
rental-yield estimates
investment returns
```

The response states the limitation and uses `Insufficient Evidence` when
optional What-if evidence is unavailable.

## Audit Trail

No migration was required. Existing durable `tool_events` persistence stores:

```text
user_id
workspace_id
property_state_id
scenario_state_id
tool_name = investment
payload.request.asking_price_egp
payload.response.valuation_id
payload.response.investment_position
created_at
```

The route resolves the JWT actor through the existing ownership layer. No
caller-supplied user ID is accepted.

## Files Modified

```text
backend/app/api/schemas/copilot_tools.py
backend/app/api/routes/copilot_tools.py
backend/app/services/copilot_tools_service.py
backend/app/tests/test_copilot_tools.py
PROJECT_MASTER_STATE.md
PROJECT_MASTER_STATE_V2.md
```

## Files Created

```text
backend/app/tests/test_copilot_investment_postgis_integration.py
scripts/validate_copilot_investment.ps1
PHASE_5_5B_6_INVESTMENT_TOOL_IMPLEMENTATION_REPORT.md
INVESTMENT_TOOL_DOCKER_VALIDATION_REPORT.md
```

## Docker Evidence

Dedicated validator:

```powershell
.\scripts\validate_copilot_investment.ps1
```

Result:

```text
workspace_id:                              145
property_id:                               157
sparse_property_id:                        158
scenario_id:                               147
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
what_if_status:                            Available
what_if_source:                            TruthLayer
what_if_scenario_grounded:                 true
scenario_router_size_sqm:                  230
all_strengths_traceable:                   true
all_risks_traceable:                       true
all_positions_traceable:                   true
forbidden_metric_fields:                   0
same_snapshot_child_tools:                 true
tenant_isolation_status:                   404
investment_events_before_restart:          6
investment_events_after_postgres_restart:  7
restart_investment_source:                 TruthLayer
forbidden_tool_logic_references:           0
```

## Test Results

```text
python -m compileall -q backend/app
PASS

PowerShell parser: scripts/validate_copilot_investment.ps1
PASS

docker compose config --quiet
PASS

Focused local persistence and Tool Layer suite
16 passed

Live seeded PostGIS Investment plus adjacent integration suite
9 passed

Dedicated Investment Docker validator
PASS

Tools 1 + 2 Docker validator
PASS

Tools 3 + 4 Docker validator
PASS

Standalone What-if Docker validator
PASS

Negotiation Docker validator
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
114 passed, 5 skipped, 8 failed
```

The eight executable failures remain the previously documented stale pricing
route monkeypatch targets. They are not introduced by Tool 7.

## Remaining Risks

1. Sparse TruthLayer comparable evidence intentionally produces a
   `Moderate Opportunity` result with explicit risks. Tool 7 does not invent
   replacements.
2. Optional What-if output is sensitivity evidence, not a return forecast.
3. Historical pricing tests still need maintenance after the earlier
   pricing-service extraction.
4. Docker Compose validation proves phase readiness, not blanket production
   promotion.

## Readiness Score

| Layer | Score | Result |
| --- | ---: | --- |
| TruthLayer authority | 10 / 10 | No Tool 7 pricing, Router, ML, or CMT shortcut |
| Forbidden-output boundary | 10 / 10 | Zero ROI, IRR, CAGR, yield, return, or forecast fields |
| Evidence traceability | 10 / 10 | Positions, strengths, and risks carry references |
| Position coverage | 10 / 10 | All five positions live Docker-validated |
| Scenario support | 10 / 10 | Persisted scenario state verified |
| Optional What-if integration | 10 / 10 | Available and Insufficient Evidence paths verified |
| JWT tenant isolation | 10 / 10 | Cross-tenant investment returns 404 |
| Audit and recovery | 10 / 10 | Durable events survive backend and PostgreSQL restart |
| Regression confidence | 9 / 10 | Dedicated, adjacent, PostGIS, and smoke validations pass |

**Readiness: 89 / 90 = 98.89 / 100**

## GO / NO-GO

**GO for Phase 5.5B.6 Investment Tool.**

The implementation builds evidence-backed opportunity analysis, not
financial forecasting. TruthLayer remains authoritative.
