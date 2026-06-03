# Orchestrator Runtime Trace

Status date: 2026-06-02

## Canonical Activated Flow

```text
Authenticated POST /v1/copilot/orchestrator/respond
  -> CopilotOrchestratorRuntimeV1.run
  -> RuleBasedIntentEngine.classify
  -> DeterministicToolPlanner.plan
  -> DeterministicToolExecutor.execute
  -> CopilotToolsService Tool 1-8 invocation
  -> DeterministicResponseComposer.compose
  -> DeterministicMemoryIntegration.remember
  -> MemoryContext rebuild from existing persistence
  -> CopilotOrchestratorLLMV1.narrate
  -> NarrationAdmissionGate.evaluate
  -> PromptAssembler.build, only after ADMIT_NARRATION
  -> GeminiStatelessProviderAdapter.generate, only when configured
  -> CandidateParser.parse
  -> DeterministicGroundingLayer.validate
  -> grounded narration or Composer-owned deterministic fallback
  -> governed API delivery payload
```

## Request Entry

`backend/app/api/routes/copilot_orchestrator.py` binds the authenticated user
from JWT, accepts scoped workspace context and Tool inputs, constructs the
approved runtime with the request database session, and returns only the
governed delivery payload.

## Deterministic Stages

`backend/app/copilot/orchestrator/runtime.py` performs only call sequencing.
It does not classify intent, select Tools, execute Tool logic, calculate
values, rebuild memory itself, assemble prompts, parse candidates, or ground
claims.

Memory Integration persists one idempotent Composer summary and rebuilds
`MemoryContext` from existing PostgreSQL state before the narration handoff.

## Provider Handoff

Narration is default-off. When narration is not activated, the Admission Gate
returns deterministic-only behavior and the runtime delivers the
Composer-owned frontend payload.

When narration is activated for one approved intent, the gate must admit the
request before Prompt Assembly and the one-shot Gemini 2.5 Pro call. The
original candidate is parsed once and validated by fail-closed Grounding. A
rejected candidate is not repaired, retried, or failed over.

## Access Denial

If Memory Integration reports inaccessible tenant scope, narration returns
`ACCESS_DENIED`. The API delivery response redacts scoped payloads, citations,
memory identifiers, execution identifiers, and plan identifiers.
