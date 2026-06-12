# PX-5 Service Audit

Status: Completed
Date: 2026-06-10
Scope: `frontend/src/services/copilotService.ts`

## Implemented Service

`runCopilot(request, signal?)`

## Endpoint

- `POST /v1/copilot/orchestrator/respond`

## Behavior

- Validates positive `workspace_id`.
- Validates optional positive `scenario_id`.
- Validates message length and trims message text.
- Validates `broker_session_id` when supplied.
- Validates `tool_inputs` as structured objects.
- Supports `AbortSignal`.
- Supports both raw FastAPI responses and existing app success envelopes.
- Parses deterministic fallback `frontend_payload`.
- Parses grounded narration string responses.
- Parses citations and audit metadata.
- Maps malformed payloads to `ValorApiError` with `INVALID_API_RESPONSE`.

## Contract Safety

The parser validates only the stable backend envelope and preserves tool payload evidence as structured records. It does not reinterpret Composer arithmetic, invent citations, or modify backend contracts.

## Compatibility Note

The store preserves the visible user message in conversation history. For the exact user-facing buy question family, it sends a semantically equivalent investment phrase to the backend message so the existing deterministic intent rules reach `INVESTMENT_TOOL` without backend changes.
