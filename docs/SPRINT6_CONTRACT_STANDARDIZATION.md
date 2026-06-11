# Sprint 6 Contract Standardization

Date: 2026-06-11

## Objective

Audit every API route and remove ambiguity about response contracts without breaking current clients.

## Route Contract Inventory

### Standard Success Envelope

These routes return:

```json
{
  "success": true,
  "data": {},
  "meta": {
    "request_id": "..."
  }
}
```

Routes:

- `GET /health`
- `GET /health/ready`
- `GET /health/metrics`
- `GET /health/operational`
- `POST /v1/rent/fair-price`
- `POST /v1/valuation/fair-price`
- `POST /v1/broker/analyze`
- `POST /v1/broker/chat`
- `POST /v1/broker/intent`
- `POST /v1/broker/reason`
- `GET /v1/broker/session/{session_id}`

### Streaming Contract

- `POST /v1/broker/stream`

Returns server-sent events. It is intentionally not a JSON success envelope.

### Raw Typed Success Responses

These routes return route-specific Pydantic objects or arrays directly:

- `POST /v1/auth/token-exchange`
- `/v1/copilot/users/*`
- `/v1/copilot/workspaces*`
- `/v1/copilot/chats*`
- `/v1/copilot/messages*`
- `/v1/copilot/properties*`
- `/v1/copilot/scenarios*`
- `/v1/copilot/assumptions*`
- `/v1/copilot/tool-events*`
- `/v1/copilot/workspaces/{workspace_id}/decisions`
- `/v1/copilot/tools/*`
- `POST /v1/copilot/orchestrator/respond`

### Error Contract

Global exception handlers normalize validation, HTTP, timeout, body-size, rate-limit, and unhandled errors into:

```json
{
  "success": false,
  "error": {
    "code": "...",
    "message": "...",
    "details": []
  },
  "meta": {
    "request_id": "..."
  }
}
```

## Drift Assessment

Contract drift remains in success responses by design:

- Health, pricing, and broker use standard success envelopes.
- Auth, Copilot persistence, Copilot tools, and orchestrator use raw typed responses.
- Frontend services are tolerant in many places by unwrapping either raw or enveloped responses.

Changing all Copilot/Auth/Tool routes to envelopes in Sprint 6 would be risky because React, Flutter, and tests currently bind to raw route models.

## Standardization Decision

Do not rewrite success contracts in Sprint 6.

Formalize the current contract rules:

1. Error responses must use the standard error envelope everywhere.
2. Health, pricing, and broker non-stream JSON routes must use success envelopes.
3. Broker stream remains SSE.
4. Auth/token-exchange, Copilot persistence, Copilot Tool Layer, and orchestrator success responses remain raw typed models unless versioned under a future `/v2` contract.
5. New routes must explicitly declare which family they follow.

## Verification

- `test_api_contract.py` verifies pricing success envelope.
- `test_api_contract_hardening.py` verifies health/readiness/metrics/operational envelopes, validation envelopes, rate-limit envelopes, request-id headers, and OpenAPI exposure.
- Frontend test suite passed against current mixed strategy: 35 files, 144 tests.
- Flutter tests passed against current backend mapping: 11 tests.

## Contract Certification

Contract strategy is stable enough for pilot.

Full production recommendation: define a versioned API contract policy and either envelope all success responses in `/v2` or generate SDKs from explicit raw/enveloped OpenAPI metadata.

