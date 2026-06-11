# PX-1 Service Audit

Status: Complete
Date: 2026-06-09

## Created

- `frontend/src/services/whatIfService.ts`

## Public API

`runWhatIfAnalysis(request, signal?)`

- Calls `POST /v1/copilot/tools/what-if`.
- Accepts an optional `AbortSignal`.
- Returns `{ data, meta }`.
- Supports both current success envelopes and raw response payloads.

## Runtime Validation

The service validates:

- Positive integer `workspace_id`.
- Positive integer `property_id`.
- Positive integer `scenario_id` when present.
- Non-empty object `modifications`.
- Required response fields.
- Literal `tool_name`, `source`, and `fairness_status` values.
- Nested explainability, feature change, and comparable structures.

## Error Mapping

- Local request validation throws `ValorApiError` with `INVALID_WHAT_IF_REQUEST`.
- Malformed backend responses throw `ValorApiError` with `INVALID_API_RESPONSE`.
- Backend/network errors continue through the shared Axios interceptor and preserve status, request id, and correlation id when supplied.

## Contract-Safe Parsing

Undefined values are stripped before transport, while `null`, `false`, `0`, and empty arrays are preserved because they can be meaningful backend inputs.
