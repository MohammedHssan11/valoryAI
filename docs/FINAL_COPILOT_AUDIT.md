# Final Copilot Audit

Audit date: 2026-06-10

## Backend Copilot Architecture

The Copilot backend is a real orchestrator, not just a chat endpoint.

Runtime sequence in `backend/app/copilot/orchestrator/runtime.py`:

1. Classify intent with the rule-based intent engine. Evidence: `runtime.py:136`.
2. Build deterministic execution plan. Evidence: `runtime.py:147`.
3. Execute tools through deterministic executor. Evidence: `runtime.py:159`.
4. Compose response with evidence/citations. Evidence: `runtime.py:180`.
5. Record memory/decision context. Evidence: `runtime.py:191`.
6. Optionally narrate through gated LLM integration. Evidence: `runtime.py:218-248`.

## Copilot Components

| Component | Source | Status |
| --- | --- | --- |
| Intent engine | `backend/app/copilot/orchestrator/intents/engine.py` | Rule-based, deterministic, governed intent classification. |
| Planner | `backend/app/copilot/orchestrator/planner/planner.py` | Maps intents to approved tool calls; handles clarification/general cases. |
| Executor | `backend/app/copilot/orchestrator/executor/executor.py` | Invokes tool service with isolated execution behavior and structured failures. |
| Composer | `backend/app/copilot/orchestrator/composer/composer.py` | Compresses/normalizes evidence, citations, sparse evidence, conflicts, property comparison. |
| Memory | `backend/app/copilot/orchestrator/memory/integration.py` | Persists decision context and builds scoped memory from workspace/history/tool state. |
| LLM/narration | `backend/app/copilot/orchestrator/llm/*` | Optional, admission-gated, citation-grounded, default-off unless enabled by settings. |

## Copilot Product Integration

| Client | Finding |
| --- | --- |
| React | Drawer/store/service exist, but `copilotStore` requires `activeWorkspaceId`, builds tool inputs from local state, and calls a protected orchestrator endpoint through an unauthenticated Axios client. |
| Flutter | Uses authenticated Dio and sends workspace context to `/v1/copilot/orchestrator/respond`; integration test covers live response mapping. |

## Important Copilot Constraints

1. The Copilot orchestrator is deterministic-first. It should be represented as a governed decision assistant, not an unconstrained chat bot.
2. Narration is default-off. When off, responses use deterministic fallback delivery rather than provider-generated prose.
3. Explainability depends on a persisted protected-tool `valuation_id`; direct public valuation does not automatically satisfy that prerequisite.
4. Market insight depends on accumulated protected-tool snapshots/events in the workspace.
5. React Copilot cannot become usable until web auth and property-context continuity are fixed.

## Copilot Verdict

Backend Copilot qualifies as a real decision-intelligence orchestrator. The complete product does not yet qualify as an end-to-end Copilot decision platform in React because the browser client lacks authentication and prerequisite state continuity.
