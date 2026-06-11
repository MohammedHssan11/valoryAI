# PX-5 Architecture Summary

Status: Completed
Date: 2026-06-10

## Architecture Impact

PX-5 adds a frontend Copilot Orchestrator Layer over the existing ValorAI workflow. It does not create a new backend tool, route, schema, migration, or valuation/negotiation/investment/market algorithm.

The layer is attached globally through `AppShell` but remains context-driven by the property workflow. It uses the active workspace, property, selected scenario, latest valuation, latest what-if run, latest negotiation run, latest investment run, and latest market insight state.

## Runtime Flow

1. User values a property.
2. Property Context Bridge binds the valuation to a backend workspace/property.
3. User runs optional scenario, negotiation, investment, or market intelligence surfaces.
4. Copilot drawer builds exact orchestrator request inputs from that workflow state.
5. Backend orchestrator runs intent, planning, execution, composer, memory, and narration/fallback.
6. Frontend renders structured answer, reasoning, evidence, citations, tool usage, confidence/status, and human-readable context.

## UI Components

- `CopilotDrawer`
- `CopilotPanel`
- `ContextSummaryBar`
- `EvidenceDrawer`
- `CitationViewer`
- `ToolExecutionTimeline`

## Business Impact

Users can ask a natural-language property question from the current workflow and see ValorAI intelligence composed across deterministic evidence surfaces. Copilot exposes valuation intelligence rather than replacing the valuation product.

## Limitations

- Runtime execution still depends on authenticated Copilot persistence endpoints.
- Full backend `MemoryContext` is not returned by the orchestrator response; the frontend renders memory ID/status plus local workflow context.
- Property comparison remains limited by available frontend property-B input collection.
