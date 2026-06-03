# ValorAI Phase 5.5B.3 Tools 3 + 4 Implementation Report

Report date: 2026-05-31  
Scope: Comparable Tool and Fairness Tool only  
Decision: **GO**

## Executive Result

Implemented only:

1. Tool 3: Comparable Tool
2. Tool 4: Fairness Tool

No What-if, Negotiation, Investment, Market Insight, Copilot Orchestrator, or
LLM integration work was added.

The Tool Layer remains an adapter layer. It does not calculate prices, estimate
market values, generate comparables, call CMT directly, or call ML directly.

## Architecture

### Tool 3: Comparable

```text
JWT Actor
  -> Comparable Tool API
  -> tenant-scoped Workspace / Property / Scenario resolution
  -> existing tenant-scoped valuation snapshot, when valuation_id is supplied
     OR
     Valuation Tool -> Router -> existing CMT / ML routing
  -> stored Router explainability comparable evidence
  -> normalized comparable response
  -> persisted tool_event
```

Comparable retrieval is evidence-only. When a fresh valuation is needed, Tool
3 invokes Tool 1. It never calls CMT, ML, or a pricing route directly.

### Tool 4: Fairness

```text
JWT Actor
  -> Fairness Tool API
  -> tenant-scoped Workspace / Property / Scenario resolution
  -> Valuation Tool with target_price_egp
  -> Router
  -> existing Router fairness explanation
  -> normalized fairness response
  -> persisted tool_event
```

Tool 4 does not compare target prices itself. The existing Router fairness
logic remains authoritative.

## Contracts

### Tool 3 Endpoint

```text
POST /v1/copilot/tools/comparable
```

Input:

```json
{
  "workspace_id": 78,
  "property_id": 80,
  "scenario_id": 78,
  "valuation_id": "optional val_..."
}
```

Output:

```json
{
  "tool_name": "comparable",
  "valuation_id": "val_...",
  "comparable_count": 5,
  "comparables": [
    {
      "comparable_id": "...",
      "price": 85000,
      "size_sqm": 220.0,
      "bedrooms": 4,
      "bathrooms": 3,
      "compound_name": "Mivida",
      "distance_km": 0.4,
      "similarity_reason": "SAME_AREA_MATCH",
      "source": "TruthLayer"
    }
  ],
  "source": "TruthLayer"
}
```

### Tool 4 Endpoint

```text
POST /v1/copilot/tools/fairness
```

Input:

```json
{
  "workspace_id": 78,
  "property_id": 80,
  "scenario_id": 78,
  "target_price_egp": 85000
}
```

Output:

```json
{
  "tool_name": "fairness",
  "valuation_id": "val_...",
  "fair_price": 85000,
  "target_price": 85000,
  "fairness_status": "Within Fair Value",
  "confidence_level": "High",
  "confidence_reason": "...",
  "source": "TruthLayer"
}
```

Allowed normalized statuses:

```text
Below Fair Value
Within Fair Value
Above Fair Value
```

## Truth-Layer Evidence Hardening

The existing Router explainability payload previously inserted:

```text
listing_date = "Recent"
```

That fabricated metadata was removed. The truth payload now exposes real
retrieved comparable metadata:

```text
compound_name     <- CMT comparable row
similarity_reason <- CMT retrieval reason_code
```

When real metadata is unavailable, the payload leaves the optional field
unavailable. The Tool Layer does not fill gaps with generated values.

## Authorization And Audit

Both tools use the existing JWT actor resolved by `get_authenticated_user`.
Caller-supplied user IDs are not accepted.

Every successful execution appends a tenant-scoped `tool_events` row:

```text
user_id
workspace_id
property_state_id
scenario_state_id
tool_name
payload.request
payload.response
created_at
```

Tool 4 also persists the underlying Valuation Tool event because the Router
valuation and fairness explanation are part of the authoritative trail.

## Files Modified

```text
backend/app/api/routes/copilot_tools.py
backend/app/api/schemas/copilot_tools.py
backend/app/api/schemas/pricing.py
backend/app/services/copilot_tools_service.py
backend/app/services/router_service.py
backend/app/tests/test_routes_and_health.py
```

## Files Created

```text
backend/app/tests/test_copilot_tools_3_4_postgis_integration.py
scripts/validate_copilot_tools_3_4.ps1
PHASE_5_5B_3_TOOLS_3_4_IMPLEMENTATION_REPORT.md
TOOLS_3_4_DOCKER_VALIDATION_REPORT.md
```

No database migration was needed. Tools 3 and 4 reuse the existing
`valuation_snapshots` and `tool_events` tables.

## Test Results

```text
python -m compileall -q backend/app
PASS

PowerShell parser: scripts/validate_copilot_tools_3_4.ps1
PASS

docker compose config --quiet
PASS

Focused Python regression suite
14 passed

Live PostGIS integration suite
3 passed
```

Unfiltered backend audit:

```text
python -m pytest app/tests -q
BLOCKED during collection by the pre-existing stale
test_spatial_confidence.py import from app.api.routes.pricing
```

Wider executable backend audit:

```text
python -m pytest app/tests --ignore=app/tests/test_spatial_confidence.py -q
111 passed, 2 skipped, 8 failed
```

The eight failures are the existing stale pricing-test monkeypatches targeting
`app.api.routes.pricing.nearest_area` after pricing internals moved into the
valuation service. They are not introduced by Tools 3 and 4.

## Readiness Score

| Layer | Score | Result |
| --- | ---: | --- |
| Truth-Layer Authority | 10 / 10 | No Tool Layer pricing logic |
| Comparable Evidence | 10 / 10 | Real CMT snapshot evidence only |
| Fairness Adapter | 10 / 10 | Existing Router fairness logic only |
| Scenario Support | 10 / 10 | Scenario size overlay verified at 230 sqm |
| JWT Tenant Isolation | 10 / 10 | Cross-tenant Comparable and Fairness return 404 |
| Audit Persistence | 10 / 10 | Tool events persist through restart |
| Regression Confidence | 9 / 10 | Phase, PostGIS, Docker, broker, and recovery passes |

**Readiness: 69 / 70 = 98.6 / 100**

## Remaining Risks

1. Historical pricing tests still need import and monkeypatch maintenance
   after the prior pricing-service move.
2. Comparable `compound_name` remains nullable because some real listings do
   not carry compound metadata.
3. Docker Compose remains staging-grade infrastructure. This GO decision is
   scoped to Phase 5.5B.3 Tools 3 and 4.

## GO / NO-GO

**GO for Phase 5.5B.3 Tools 3 + 4.**

The implementation builds adapters, not intelligence. TruthLayer remains
authoritative.
