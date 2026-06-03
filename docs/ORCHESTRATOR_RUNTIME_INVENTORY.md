# Orchestrator Runtime Inventory

Status date: 2026-06-02

## Authoritative Boundary

The activated modern Copilot runtime is:

```text
COPILOT_ORCHESTRATOR_LLM_V1
```

Live Gemini narration remains default-off. The modern runtime endpoint always
executes the deterministic orchestration path and invokes Gemini only when the
approved global flag, explicit per-intent allowlist, credential, and provider
data-governance acknowledgement are configured.

## HTTP Entry Points

| Surface | Entry point | Runtime owner | Status |
| --- | --- | --- | --- |
| Modern Copilot orchestrator | `POST /v1/copilot/orchestrator/respond` | `backend/app/copilot/orchestrator/runtime.py` | Activated |
| Transitional broker analysis | `POST /v1/broker/analyze` | `backend/app/broker/orchestrator/core.py` | Existing deterministic compatibility surface |
| Transitional broker chat | `POST /v1/broker/chat` | `backend/app/broker/orchestrator/core.py` | Existing deterministic compatibility surface |
| Transitional broker reasoning | `POST /v1/broker/reason` | `backend/app/broker/orchestrator/core.py` | Existing deterministic compatibility surface |
| Transitional broker stream | `POST /v1/broker/stream` | `backend/app/broker/orchestrator/core.py` | Existing broker SSE surface |
| Transitional broker intent | `POST /v1/broker/intent` | `backend/app/broker/orchestrator/core.py` | Existing deterministic classifier |
| Copilot memory | `/v1/copilot/*` workspace, chat, message, property, scenario, assumption, event, and decision routes | `backend/app/services/copilot_service.py` | Existing |
| Copilot Tools 1-8 | `/v1/copilot/tools/*` | `backend/app/services/copilot_tools_service.py` | Existing |

The modern orchestrator route is registered in
`backend/app/main.py`. No modern pre-grounding streaming endpoint was added.

## Runtime Components

| Stage | Existing component |
| --- | --- |
| Intent Engine | `backend/app/copilot/orchestrator/intents/` |
| Tool Planner | `backend/app/copilot/orchestrator/planner/` |
| Tool Executor | `backend/app/copilot/orchestrator/executor/` |
| Response Composer | `backend/app/copilot/orchestrator/composer/` |
| Memory Integration | `backend/app/copilot/orchestrator/memory/` |
| Admission Gate | `backend/app/copilot/orchestrator/llm/gate.py` |
| Prompt Assembly | `backend/app/copilot/orchestrator/llm/prompts.py` |
| Gemini 2.5 Pro Adapter | `backend/app/copilot/orchestrator/llm/provider.py` |
| Candidate Parser | `backend/app/copilot/orchestrator/llm/parser.py` |
| Grounding | `backend/app/copilot/orchestrator/llm/grounding.py` |
| Activation wiring | `backend/app/copilot/orchestrator/runtime.py` |

## Provider Inventory

The only authorized modern provider adapter is
`GeminiStatelessProviderAdapter`. No active legacy broker provider package,
legacy OpenAI adapter, competing narration provider, retry path, or failover
path is present.

The transitional broker API retains deterministic compatibility narration in
`backend/app/broker/services/narration.py`; it does not construct or invoke an
LLM provider.
