# PX-5 Orchestrator Audit

Status: Completed
Date: 2026-06-10
Scope: Frontend Copilot Orchestrator Layer audit against existing backend contracts

## Backend Sources Audited

- `backend/app/api/schemas/copilot_orchestrator.py`
- `backend/app/api/routes/copilot_orchestrator.py`
- `backend/app/copilot/orchestrator/runtime.py`
- `backend/app/copilot/orchestrator/intents/contracts.py`
- `backend/app/copilot/orchestrator/planner/contracts.py`
- `backend/app/copilot/orchestrator/executor/contracts.py`
- `backend/app/copilot/orchestrator/composer/contracts.py`
- `backend/app/copilot/orchestrator/memory/contracts.py`
- `backend/app/copilot/orchestrator/llm/contracts.py`
- `docs/COMPOSED_RESPONSE_CONTRACT_V1.md`
- `docs/EXECUTION_RESULT_CONTRACT.md`
- `docs/COMPOSER_CITATION_POLICY.md`
- `docs/MEMORY_CONTEXT_CONTRACT.md`

## Route Contract

- Method: `POST`
- Path: `/v1/copilot/orchestrator/respond`
- Auth: inherited from `get_authenticated_user`
- Runtime: `COPILOT_ORCHESTRATOR_LLM_V1`

## Request Schema

`CopilotOrchestratorRequest`

- `workspace_id: int`
- `scenario_id: int | null`
- `broker_session_id: str | null`
- `message: str`
- `tool_inputs: dict[str, dict[str, Any]]`

The backend normalizes simple tool aliases to planned tool IDs. The frontend sends planned tool IDs directly.

## Response Schema

`CopilotOrchestratorResponse`

- `runtime_id`
- `response_id`
- `intent`
- `status`
- `delivery_mode`
- `response`
- `citation_package`
- `audit`

Default frontend runtime path is deterministic fallback, where `response` is the Composer `frontend_payload`.

## Citation Behavior

The frontend renders only the citation package returned by the backend:

- `valuation_ids`
- `tool_event_ids`
- `comparable_ids`
- `unavailable_optional_citation_types`

No frontend citation IDs are fabricated.

## Memory Payloads

The route exposes memory in delivery audit as:

- `memory_id`
- `memory_status`

It does not expose the full `MemoryContext` object in the response. PX-5 therefore renders human-readable active context from frontend workflow state and displays backend memory ID/status when returned.

## Composed Responses

The frontend handles:

- `GROUNDED_NARRATION` string responses.
- `DETERMINISTIC_FALLBACK` structured `frontend_payload` responses.
- `ACCESS_DENIED` redacted responses.

Structured payload rendering keeps answer, reasoning summary, tool outputs, failed tools, full evidence, citations, confidence/status, and memory status separate.

## Tool Routing Behavior

Planner-owned tool routing remains backend-only. The frontend supplies inputs for the active workflow tools:

- `VALUATION_TOOL`
- `EXPLAINABILITY_TOOL` when a valuation ID is available
- `COMPARABLES_TOOL`
- `FAIRNESS_TOOL` when an asking/target price is available
- `WHAT_IF_TOOL` when scenario modifications exist
- `NEGOTIATION_TOOL`
- `INVESTMENT_TOOL`
- `MARKET_INSIGHT_TOOL`

No backend route, contract, planner, executor, composer, memory, or tool logic was modified.
