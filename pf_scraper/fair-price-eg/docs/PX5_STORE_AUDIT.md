# PX-5 Store Audit

Status: Completed
Date: 2026-06-10
Scope: `frontend/src/store/copilotStore.ts`

## State

- `conversation`
- `activePropertyId`
- `activeScenarioId`
- `lastResponse`
- `isLoading`
- `error`
- `citations`
- `memoryContext`

## Actions

- `sendMessage()`
- `clearConversation()`
- `reset()`

## Workflow Awareness

The store reads active state from existing frontend stores:

- property context
- valuation
- what-if
- scenario history
- negotiation
- investment
- market insight

It builds orchestrator tool inputs from the active property workflow and selected/restored scenario where available.

## Memory Rendering

Because the route returns only memory audit fields, the store builds a human-readable context summary from frontend workflow state and attaches backend `memory_id` and `memory_status` when returned.

## Error Handling

- Missing workspace is rejected before network execution.
- Service errors are stored without removing prior conversation.
- Abort signals are passed through.
