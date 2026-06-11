# Final V2 Workflow Audit

Audit date: 2026-06-11

## Required Journey Results

| Journey | Current status | Notes |
| --- | --- | --- |
| 1. Direct valuation | Complete, with deployment caveat. | React route is protected, form posts to `/v1/valuation/fair-price`, result renders explainability/comparables, and backend route is tested. Requires configured Firebase in the React runtime. |
| 2. Valuation -> What-if | Complete in source. | Direct valuation bridge creates workspace/property context; what-if runs when context is ready and modifications exist. Backend self-runs protected valuations and returns complete sensitivity output. |
| 3. Valuation -> Scenario -> Negotiation | Complete in source. | Scenario history can save/restore selections; negotiation runs against base, active, or selected scenario with protected tool evidence. |
| 4. Valuation -> Scenario -> Investment | Complete in source. | Investment runs against base, active, selected, or compared scenarios and composes negotiation-backed evidence. |
| 5. Workspace -> Market Intelligence | Partial. | UI and backend work, but meaningful output requires protected `ValuationSnapshot` history. Direct valuation bridge alone records a `ToolEvent`, not a snapshot, so first-run direct-only users can see sparse/no market evidence. |
| 6. Workspace -> Copilot | Partial to complete depending on prompt. | Copilot can run after workspace context exists. Valuation/fairness/negotiation/investment prompts have tool inputs. "Explain this valuation" can be blocked after direct-only valuation because no protected valuation id exists yet. |
| 7. Workspace -> Broker | Complete in source. | Broker resolves or creates scenario context, sends aligned request fields, authenticates, and supports reason/chat/stream backend paths. |

## Demo Reality

Safe to demo from source with configured Firebase:

- React login and protected app shell.
- Direct valuation, explainability panel, comparable panel.
- Direct valuation to property context bridge.
- What-if scenario analysis.
- Scenario save/restore flow.
- Negotiation and investment intelligence.
- Broker reasoning with aligned workspace/scenario context.
- Backend Copilot/tool behavior through authenticated API/tests.
- Flutter auth, valuation, workspace, and Copilot mappings.

Do not claim without caveat:

- Docker Compose React frontend is auth-ready out of the box. It is not, because Firebase web config is not passed into the frontend build.
- Market intelligence is an external live market feed. It is descriptive analytics over persisted TruthLayer history.
- Direct public valuation automatically creates a protected valuation snapshot. It currently does not.
- Flutter has React feature parity. It does not.

## Workflow Verdict

ValorAI is now source-level demo-ready for the main web decision workflows after Firebase configuration. It is not yet fully production-workflow-ready because the Docker deployment auth config and direct valuation snapshot continuity are incomplete.
