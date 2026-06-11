# ValorAI Phase 5.5B.2A Broker Adapter Root Cause

Audit date: 2026-05-31  
Scope: legacy Broker Adapter only  
Status at audit start: **FAIL**

## Execution Path Traced

### Broker valuation-backed path before repair

```text
POST /v1/broker/chat
  -> app.api.routes.broker.broker_chat
  -> app.broker.orchestrator.core.BrokerOrchestrator.chat
  -> BrokerOrchestrator._run
  -> BrokerOrchestrator._execute_tool_plan
  -> app.broker.tools.registry.BrokerToolRegistry.execute
  -> app.broker.tools.valuation.ValuationAnalysisTool.execute
  -> app.api.routes.pricing.rent_fair_price
  -> app.services.router_service.price_listing_router
  -> CMT or ML
```

The direct valuation API and Phase 5.5B.2 Copilot Tool API are separate
operational paths:

```text
POST /v1/valuation/fair-price
  -> pricing route
  -> Router
  -> CMT or ML

POST /v1/copilot/tools/valuation
  -> CopilotToolsService.execute_valuation
  -> tenant-scoped workspace/property/scenario adapter
  -> Router
  -> CMT or ML
  -> valuation snapshot
  -> tool event

POST /v1/copilot/tools/explainability
  -> CopilotToolsService.execute_explainability
  -> tenant-scoped valuation snapshot
  -> TruthLayer explainability payload
  -> tool event
```

## Exact Failing Call

File:

```text
backend/app/broker/tools/valuation.py
```

Pre-repair call:

```python
envelope = pricing_routes.rent_fair_price(tool_request.valuation_request, db)
```

## Exact Obsolete Signature

The Broker Adapter still assumes the historical positional boundary:

```python
rent_fair_price(req, db)
```

The live pricing route signature is:

```python
rent_fair_price(
    req: RentFairPriceRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
)
```

The Broker Adapter therefore binds its SQLAlchemy `db` session to
`background_tasks`. The route's actual `db` parameter remains the FastAPI
dependency marker because the route function is being called directly instead
of through FastAPI dependency injection.

## Exact Contract Mismatch

The legacy Broker Adapter treats an HTTP route handler as an internal pricing
service. That is no longer a supported call boundary.

The implemented Phase 5.5B.2 contract is:

```text
Broker Adapter
  -> CopilotToolsService.execute_valuation(
       user_id,
       ValuationToolRequest(
         workspace_id,
         property_id,
         scenario_id,
       ),
     )
  -> CopilotToolsService.execute_explainability(
       user_id,
       ExplainabilityToolRequest(
         workspace_id,
         valuation_id,
       ),
     )
  -> Response Builder
```

The Broker Adapter must not invoke pricing routes directly and must not bypass
either Tool 1 or Tool 2.

## Exact Payload Mismatch

The legacy broker payload passed into the pricing route is:

```text
RentFairPriceRequest
```

The required Tool 1 payload is:

```text
ValuationToolRequest
  workspace_id
  property_id
  scenario_id
```

Tool 1 resolves the router-ready `RentFairPriceRequest` from persisted,
tenant-scoped workspace state and applies scenario lineage before invoking the
Router.

The required Tool 2 payload is:

```text
ExplainabilityToolRequest
  workspace_id
  valuation_id
```

The legacy Broker Adapter never calls Tool 2. It instead packages explanation
fields from the direct pricing response locally.

## Production Impact

For valuation-backed broker turns:

```text
valuation_analysis -> failed
downstream broker evidence tools -> skipped
broker response -> degraded deterministic-safety fallback
```

The same property remains operational through the direct valuation route and
the Copilot Tool valuation route. The defect is isolated to the legacy Broker
Adapter.

## Repair Boundary

The repair is limited to the Broker Adapter path:

```text
Broker Chat
  -> Broker Adapter
  -> Valuation Tool
  -> Explainability Tool
  -> Response Builder
  -> User
```

The Router, ML engine, CMT engine, explainability engine, Tool 1, and Tool 2
must remain unchanged.
