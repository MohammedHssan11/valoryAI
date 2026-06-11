# Final V2 Tool Audit

Audit date: 2026-06-11

## Tool Status Matrix

| Tool | Backend status | React status | Flutter status | Current verdict |
| --- | --- | --- | --- | --- |
| Tool 1: Valuation | Implemented as public valuation and protected Copilot valuation. Protected tool creates `ValuationSnapshot`, `ToolEvent`, prediction log, and shadow pipeline records. | Direct valuation UI works behind protected React app. Protected valuation can be reached through Copilot/tool chains. | Direct valuation remote data source exists. | Ready for core use. |
| Tool 2: Explainability | Implemented against protected `ValuationSnapshot`. | Direct valuation has local explainability UI from valuation response. Copilot explainability tool input exists only after a protected tool has created a valuation id. | Response model maps explainability. | Backend ready; direct-to-Copilot continuity partial. |
| Tool 3: Comparables | Implemented; can self-run valuation if no valuation id is supplied. | Direct comparables panel and protected service flow exist. | Comparable explorer exists. | Ready with normal context. |
| Tool 4: Fairness | Implemented; self-runs valuation with target price. | Used through Copilot, negotiation, investment, and what-if chains. | No standalone mobile UX. | Backend/React ready; Flutter partial. |
| Tool 5: What-if | Implemented; creates base and sandbox protected valuations, explainability, comparables, fairness, and events. | UI/service/store/history integration exist and run when workspace/property context is ready. | No parity. | Ready in React after valuation bridge. |
| Tool 6: Negotiation | Implemented; orchestrates valuation, explainability, comparables, fairness, optional what-if. | UI/service/store exist and run on base, active scenario, or selected scenario. | No parity. | Ready in React after valuation bridge. |
| Tool 7: Investment | Implemented by composing negotiation plus investment position logic. | UI/service/store exist and run on base/scenario targets. | No parity. | Ready in React after valuation bridge. |
| Tool 8: Market Intelligence | Implemented as descriptive analytics over `ValuationSnapshot`, prediction logs, shadow logs, tool events, and workspace history. | Pulse panel exists and auto-runs when active workspace exists. | No parity. | Real, but sparse immediately after direct-only valuation. |
| Broker reasoning | Protected backend endpoints and SSE stream exist. | React request contract now sends `workspace_id` and `scenario_id`; stream fetch injects bearer token. | Not primary. | Source-aligned. |
| Copilot orchestrator | Real deterministic runtime: intent, plan, execute, compose, memory, optional narration. | Drawer/store/service exist with workspace/scenario/tool context. | Remote data source and repository exist. | Real, with direct-only explainability prerequisite gap. |

## Current Tool Truth

The protected backend tool layer is not a mock. `CopilotToolsService` executes real router-backed valuation and uses that output to compose explainability, comparables, fairness, what-if, negotiation, investment, and market insight. The higher-order tools reduce prerequisite fragility because they self-run valuation when needed.

Sprint 1 and Sprint 2 materially changed the earlier tool audit:

- React protected tool calls now receive bearer tokens through `src/api/http.ts`.
- Broker calls now include backend-required `workspace_id` and `scenario_id`.
- Broker streaming uses `fetch` with `Authorization: Bearer <token>`.

## Remaining Tool Gaps

| ID | Gap | Impact |
| --- | --- | --- |
| TOOL-G1 | Direct valuation bridge records a `ToolEvent` but does not create a `ValuationSnapshot`. | Market intelligence can show zero persisted TruthLayer valuations immediately after a direct valuation. Copilot explainability cannot reference the direct valuation until a protected tool has created a valuation id. |
| TOOL-G2 | Market intelligence is descriptive over persisted internal valuation history, not an external market feed or forecast engine. | Product claims must stay precise: "workspace pulse from persisted TruthLayer history", not live market forecasting. |
| TOOL-G3 | Flutter does not expose tools 5-8, broker, or market insight as full UX surfaces. | Mobile is useful but not feature-parity with React. |

## Tool Audit Verdict

Backend tool maturity is high and React product access is now substantially wired. The remaining tool-layer issue is not missing tool implementation; it is continuity from direct valuation into protected snapshot-backed intelligence, especially market insight and Copilot explainability.
