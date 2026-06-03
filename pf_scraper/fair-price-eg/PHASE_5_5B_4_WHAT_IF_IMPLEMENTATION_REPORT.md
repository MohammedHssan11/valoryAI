# ValorAI Phase 5.5B.4 What-if Tool Implementation Report

Report date: 2026-05-31  
Scope: Tool 5 What-if Tool only  
Decision: **GO**

## Executive Result

Implemented only:

```text
Tool 5: What-if Tool
```

No Negotiation Tool, Investment Tool, Market Insight Tool, Copilot
Orchestrator, or LLM integration was added.

The What-if Tool is a deterministic orchestration adapter. It does not
calculate a valuation, estimate market value, invent comparables, infer
fairness, call CMT directly, call ML directly, or call the Router directly.

## Architecture

```text
JWT Actor
  -> What-if Tool API
  -> tenant-scoped Workspace / Property / optional Scenario resolution
  -> fresh Valuation Tool call for current state
  -> ephemeral scenario overlay in memory
  -> fresh Valuation Tool call for sandbox state
  -> Explainability Tool for sandbox valuation snapshot
  -> Comparable Tool for sandbox valuation snapshot
  -> Fairness Tool for sandbox state
  -> TruthLayer-derived delta aggregation
  -> persisted what_if tool_event
```

Existing scenario support is compositional:

```text
Base Property
  -> persisted Scenario lineage, when scenario_id is supplied
  -> ephemeral What-if overlay
  -> sandbox Router request
  -> TruthLayer re-evaluation
```

The original `property_states` row and any referenced `scenario_states` row
remain unchanged.

## TruthLayer Boundary

The What-if Tool calls the existing adapters:

```text
execute_valuation
execute_explainability
execute_comparable
execute_fairness
```

Only these calculations occur in the new aggregation path:

```text
delta_value      = scenario_valuation - base_valuation
delta_percentage = delta_value / base_valuation * 100
```

Both operands come from authoritative Valuation Tool responses. This is the
allowed delta calculation from the phase contract.

Fairness semantics are explicit: the Fairness Tool re-evaluates the sandbox
state using the base TruthLayer valuation as its target price. The returned
status therefore answers whether the original fair price is below, within, or
above the re-evaluated sandbox fair-value band.

## Contract

Endpoint:

```text
POST /v1/copilot/tools/what-if
```

Input:

```json
{
  "workspace_id": 115,
  "property_id": 117,
  "scenario_id": 116,
  "modifications": {
    "bathrooms": 4,
    "gym": true
  }
}
```

Supported normalized scenario inputs include:

```text
size_sqm / size / area
bedrooms
bathrooms
furnished / furnishing / furnishing_status
finishing / building_quality
parking
gym
clubhouse
amenities
amenities_added
amenities_removed
floor_number
compound_name
view_type
governed location fields
property_type
property_category
```

Output:

```text
tool_name
base_valuation
scenario_valuation
base_valuation_id
scenario_valuation_id
fairness_valuation_id
delta_value
delta_percentage
fairness_status
confidence_level
assumptions_used
feature_changes
explainability
comparables
timestamp
source = TruthLayer
```

Unsupported modifications return `422`. The What-if Tool also rejects a
caller-supplied `target_price_egp`; fairness target selection belongs to its
orchestration contract.

## Scenario Sandbox Design

The sandbox is an in-memory request overlay. It is never written into the base
property or an existing scenario.

Broker-friendly amenity toggles are normalized conservatively:

```text
parking   -> CP
gym       -> SY
clubhouse -> CH
```

Furnishing and finishing aliases normalize to governed Router inputs:

```text
furnished / furnishing -> furnishing_status
finishing               -> building_quality
```

The feature summary separates:

```text
added
removed
modified
```

For example, Docker evidence returned:

```text
Size:      220 -> 230 sqm
Bedrooms:  4 -> 3
Parking:   added
Gym:       added
Bathrooms: 3 -> 4
```

## Assumptions Engine

The response reports missing tracked scenario facts rather than silently
claiming they are known:

```text
Furnished = Unknown
Parking = Unknown
Gym = Unknown
Clubhouse = Unknown
Finishing = Unknown
```

Facts explicitly present in the property, persisted scenario lineage, or
ephemeral overlay are removed from the unknown list.

## Authorization And Audit

The route uses the existing JWT actor resolved by `get_authenticated_user`.
Caller-supplied user IDs are not accepted.

Each successful What-if call appends a durable tenant-scoped `tool_events`
row containing:

```text
user_id
workspace_id
property_state_id
scenario_state_id
tool_name = what_if
payload.request.modifications
payload.request.sandbox_modifications
payload.response.base_valuation_id
payload.response.scenario_valuation_id
payload.response.delta_value
created_at
```

The orchestrated child Tool events and valuation snapshots are also durable.

## Files Modified

```text
backend/app/api/routes/copilot_tools.py
backend/app/api/schemas/copilot_tools.py
backend/app/services/copilot_tools_service.py
backend/app/tests/test_copilot_tools.py
backend/app/tests/test_routes_and_health.py
```

## Files Created

```text
backend/app/tests/test_copilot_what_if_postgis_integration.py
scripts/validate_copilot_what_if.ps1
PHASE_5_5B_4_WHAT_IF_IMPLEMENTATION_REPORT.md
WHAT_IF_DOCKER_VALIDATION_REPORT.md
```

No database migration was needed. The existing `tool_events`,
`valuation_snapshots`, `property_states`, and `scenario_states` tables already
provide the required durable substrate.

## Test Results

```text
python -m compileall -q backend/app
PASS

PowerShell parser: scripts/validate_copilot_what_if.ps1
PASS

docker compose config --quiet
PASS

Focused local suite
6 passed

Live seeded PostGIS suite
5 passed

Dedicated What-if Docker validator
PASS
```

Adjacent Docker regressions:

```text
Tools 1 + 2 validator: PASS
Tools 3 + 4 validator: PASS
Broker adapter validator: PASS
Persistence recovery validator: PASS
Staging smoke: PASS
```

Unfiltered backend audit remains blocked during collection by the pre-existing
stale `test_spatial_confidence.py` import from `app.api.routes.pricing`.

Wider executable backend audit:

```text
112 passed, 3 skipped, 8 failed
```

The eight failures are the previously documented stale pricing-route
monkeypatch targets. They are not introduced by Tool 5.

## Remaining Risks

1. Some compounded overlays can truthfully yield zero retained comparables.
   The Tool preserves that sparse evidence result instead of inventing
   comparables.
2. Missing tracked facts are disclosed as unknown, but the Router still
   evaluates the conservative available-input state.
3. Historical pricing tests still need import and monkeypatch maintenance
   after the earlier pricing-service move.
4. Docker Compose validation proves phase readiness, not blanket production
   promotion.

## Readiness Score

| Layer | Score | Result |
| --- | ---: | --- |
| TruthLayer Authority | 10 / 10 | No Tool 5 pricing, ML, CMT, or Router shortcut |
| Sandbox Immutability | 10 / 10 | Base property and existing scenario unchanged |
| Scenario Composition | 10 / 10 | Scenario-on-scenario overlay verified |
| Fresh Evidence | 10 / 10 | Fresh Comparable and Fairness evaluations verified |
| Assumptions | 9 / 10 | Missing tracked facts disclosed conservatively |
| JWT Tenant Isolation | 10 / 10 | Cross-tenant What-if returns 404 |
| Audit And Recovery | 10 / 10 | Tool events persist through backend and PostgreSQL restart |
| Regression Confidence | 9 / 10 | Dedicated, PostGIS, adjacent, and smoke validations pass |

**Readiness: 78 / 80 = 97.5 / 100**

## GO / NO-GO

**GO for Phase 5.5B.4 What-if Tool.**

The implementation builds orchestration, not intelligence. TruthLayer remains
authoritative.
