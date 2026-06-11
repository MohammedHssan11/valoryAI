# PX-1 Store Audit

Status: Complete
Date: 2026-06-09

## Created

- `frontend/src/store/whatIfStore.ts`

## State

- `lastRequest`
- `lastResponse`
- `isLoading`
- `error`

## Actions

- `runScenario(request, signal?)`
- `clearScenario()`
- `reset()`

## Behavior

- `runScenario` records the attempted request before executing.
- Successful runs store the authoritative Tool 5 response.
- Failed runs keep the attempted request and expose the mapped error.
- `clearScenario` clears current scenario output without changing the base valuation store.
- `reset` returns the what-if store to its initial state.

## Architecture Impact

The store is independent from `valuationStore`; base valuation results remain frozen while users run multiple what-if scenarios.
