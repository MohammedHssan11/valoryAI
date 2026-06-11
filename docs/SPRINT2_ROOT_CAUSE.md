# Sprint 2 Root Cause Analysis

Analysis date: 2026-06-11

## Verified Claim

The audit claim was correct.

Backend expected:

- `workspace_id`
- `scenario_id`
- `message`
- optional `session_id`
- optional `valuation_request`
- optional `investor_preferences`

Frontend previously sent:

- `session_id`
- `message`
- optional `valuation_request`

## Exact Mismatch

The React Broker request type omitted backend-required `workspace_id` and `scenario_id`.

The React Broker screen built requests from:

- intelligence session id
- prompt message
- current valuation draft

It did not bind to:

- active workspace from the property context bridge
- active property context
- active or selected scenario from scenario history

Because the backend `BrokerReasonRequest` inherits `BrokerChatRequest`, both `/v1/broker/reason` and `/v1/broker/stream` rejected the old React payload with schema validation errors before Broker runtime execution.

`/v1/broker/chat` had the same schema dependency and was also contract-incompatible.

## Secondary Runtime Cause

The property context bridge could produce:

- `activeWorkspaceId`
- `activePropertyId`
- `activeScenarioId = null`

That was valid for some tools, but invalid for Broker because Broker sessions require a positive `scenario_id`.

## Fix Strategy

Sprint 2 did not change backend schemas or create new backend endpoints.

React now:

- requires `workspace_id` and `scenario_id` in Broker request types
- resolves active workspace/property/scenario before Broker execution
- reuses `activeScenarioId` when present
- promotes a valid selected scenario from scenario history when present
- creates a baseline `Base valuation` scenario through the existing scenario API when no scenario is active
- validates and sanitizes Broker payloads before reason/chat/stream requests

## Root Cause Verdict

P0-2 was caused by frontend request-shape drift from backend-owned Broker schemas, plus missing scenario binding after property context bridge creation. The drift is now corrected in types, service payload construction, store context resolution, and the Broker screen execution path.
