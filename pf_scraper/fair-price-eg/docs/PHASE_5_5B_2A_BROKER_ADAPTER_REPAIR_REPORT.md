# ValorAI Phase 5.5B.2A Broker Adapter Repair Report

Report date: 2026-05-31  
Scope: P0 legacy Broker Adapter repair only  
Decision: **GO**

## Root Cause

The legacy Broker Adapter called the pricing HTTP route as an internal Python
service:

```python
pricing_routes.rent_fair_price(tool_request.valuation_request, db)
```

The live route signature is:

```python
rent_fair_price(req, background_tasks, db=Depends(get_db))
```

The broker session was passed into the `background_tasks` slot and the real
database parameter remained a FastAPI dependency marker. More importantly,
this legacy boundary bypassed the Phase 5.5B.2 tenant-scoped Valuation Tool and
never called the Explainability Tool.

The pre-change trace and payload mismatch are documented in:

```text
BROKER_ADAPTER_ROOT_CAUSE.md
```

## Repaired Flow

```text
Broker Chat
  -> Broker Adapter
  -> tenant-scoped scenario resolution
  -> Copilot Valuation Tool
  -> Router
  -> CMT or ML
  -> Copilot Explainability Tool
  -> Broker Response Builder
  -> User
```

The broker registry now selects only:

```text
valuation_analysis
explainability
```

No Comparable Tool, Fairness Tool, What-if Tool, Negotiation Tool, or later
Copilot tool was added.

The response builder consumes only normalized TruthLayer Tool 1 and Tool 2
contracts. It does not invent CMT tier, retained comparable count, confidence
score, district resolution, or price flag values that those normalized
contracts intentionally do not expose.

## Files Modified

Created:

```text
BROKER_ADAPTER_ROOT_CAUSE.md
scripts/validate_broker_adapter.ps1
PHASE_5_5B_2A_BROKER_ADAPTER_REPAIR_REPORT.md
```

Broker Adapter path:

```text
backend/app/broker/tools/valuation.py
backend/app/broker/tools/evidence.py
backend/app/broker/tools/registry.py
backend/app/broker/orchestrator/core.py
backend/app/broker/context/assembler.py
backend/app/broker/services/formatter.py
backend/app/broker/schemas/contracts.py
backend/app/broker/validators/grounding.py
backend/app/broker/llm/runtime/narration.py
```

Focused regression coverage:

```text
backend/app/tests/test_broker_orchestration.py
```

Not modified:

```text
Router Logic
ML Engine
CMT Engine
Explainability Engine
Tool 1: Valuation Tool
Tool 2: Explainability Tool
```

## Validation Evidence

Static validation:

```text
python -m compileall -q app
PASS

PowerShell parser: scripts/validate_broker_adapter.ps1
PASS

docker compose config --quiet
PASS

Broker direct pricing scan
PASS: zero references to pricing_routes, rent_fair_price, direct valuation
routes, or price_listing_router under backend/app/broker
```

Focused real tests:

```text
python -m pytest \
  app/tests/test_broker_orchestration.py \
  app/tests/test_copilot_tools.py \
  app/tests/test_copilot_persistence_hardening.py -q

20 passed
```

Broad backend test audit:

```text
python -m pytest app/tests -q
BLOCKED during collection by the pre-existing stale
test_spatial_confidence.py import from app.api.routes.pricing

python -m pytest app/tests --ignore=app/tests/test_spatial_confidence.py -q
111 passed, 1 skipped, 8 failed
```

The eight executed failures are pre-existing stale pricing tests that still
monkeypatch `app.api.routes.pricing.nearest_area` after pricing internals moved
to the valuation service. The broker repair does not modify those modules.

## Docker Evidence

Dedicated broker validator:

```powershell
.\scripts\validate_broker_adapter.ps1
```

Result:

```text
broker_valuation_degraded:                false
broker_valuation_grounding:               passed
broker_valuation_source:                  TruthLayer
broker_valuation_tool_names:              valuation_analysis, explainability
broker_explainability_degraded:           false
broker_explainability_source:             TruthLayer
broker_explainability_summary_present:    true
scenario_valuation_degraded:              false
scenario_router_size_sqm:                 230.0
workspace_context_workspace_id:           44
tenant_isolation_status:                  404
restart_session_retrieved:                true
restart_broker_degraded:                  false
tool_events_before_restart:               6
tool_events_after_restart:                8
direct_pricing_route_references:          0
```

Persisted PostgreSQL tool events for Docker workspace `44`:

```text
id  tool_name       property  scenario  router_size_sqm  source
33  valuation       46        44        220.0            TruthLayer
34  explainability  46        44        NULL             TruthLayer
35  valuation       46        44        220.0            TruthLayer
36  explainability  46        44        NULL             TruthLayer
37  valuation       46        45        230.0            TruthLayer
38  explainability  46        45        NULL             TruthLayer
39  valuation       46        44        220.0            TruthLayer
40  explainability  46        44        NULL             TruthLayer
```

Adjacent Docker regressions:

```text
.\scripts\validate_copilot_tools.ps1
PASS

.\scripts\validate_copilot_recovery.ps1
PASS

docker compose exec -T backend python -m app.scripts.run_migrations --verify
PASS: migration_verify_success

docker compose --profile staging run --rm staging-smoke
PASS
```

Canonical stack after validation:

```text
fair-price-eg-db-1             Up (healthy)
fair-price-eg-db-bootstrap-1   Exited (0)
fair-price-eg-backend-1        Up (healthy)
fair-price-eg-frontend-1       Up (healthy)
```

## Remaining Risks

1. The frontend still needs JWT plus workspace/scenario attachment. This was
   already identified by the master-state rebuild and is outside this repair.
2. Broker requests still accept the legacy `valuation_request` payload as an
   explicit valuation trigger for compatibility. Persisted workspace and
   scenario state are authoritative.
3. Tool 1 and Tool 2 intentionally expose normalized contracts. Broker output
   now leaves unavailable legacy CMT-only fields unset instead of fabricating
   them.
4. The historical backend suite still contains one stale collector import and
   eight stale pricing monkeypatch tests.
5. Docker Compose remains staging-grade. This GO decision is scoped to the
   Broker Adapter repair, not blanket production promotion.

## GO / NO-GO

**GO for Phase 5.5B.2A Broker Adapter Repair.**

Success criteria met:

```text
Broker Chat -> Valuation works
Broker Chat -> Explainability works
No obsolete broker pricing route usage remains
No direct broker pricing route calls remain
Docker validation passes
Restart recovery passes
Tenant isolation passes
```
