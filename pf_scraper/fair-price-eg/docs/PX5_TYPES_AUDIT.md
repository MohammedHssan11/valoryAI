# PX-5 Types Audit

Status: Completed
Date: 2026-06-10
Scope: `frontend/src/types/copilot.ts`

## Contract Sources

- `backend/app/api/schemas/copilot_orchestrator.py`
- `backend/app/copilot/orchestrator/planner/contracts.py`
- `backend/app/copilot/orchestrator/executor/contracts.py`
- `backend/app/copilot/orchestrator/composer/contracts.py`
- `backend/app/copilot/orchestrator/memory/contracts.py`
- `backend/app/copilot/orchestrator/llm/contracts.py`

## Implemented Types

- `CopilotOrchestratorRequest`
- `CopilotOrchestratorResponse`
- `CopilotRuntimeId`
- `CopilotIntent`
- `CopilotNarrationStatus`
- `CopilotDeliveryMode`
- `CopilotCompositionStatus`
- `CopilotPlannedToolCall`
- `CopilotFrontendPayload`
- `CopilotFrontendToolOutput`
- `CopilotFailedTool`
- `CopilotCitationPackage`
- `CopilotAudit`

## Tool Input Coverage

The Copilot request type supports existing backend tool input contracts only:

- valuation
- explainability
- comparable
- fairness
- what-if
- negotiation
- investment
- market insight

Existing PX-1 through PX-4 request and response types are reused where already present.

## Notes

- Unknown Composer evidence remains structured as records rather than flattened prose.
- No unsupported backend fields were added to orchestrator request or response contracts.
- Human-readable context state is typed separately from backend contracts because the orchestrator route does not return full `MemoryContext`.
