# Orchestrator Runtime Gaps

Status date: 2026-06-02

## Resolved Activation Gaps

| Gap | Evidence before activation | Resolution |
| --- | --- | --- |
| Modern orchestrator endpoint absent | No route sequenced Intent Engine through final governed delivery | Added `POST /v1/copilot/orchestrator/respond` |
| Approved components remained standalone | Existing validators invoked stages individually | Added thin `CopilotOrchestratorRuntimeV1` call sequencing |
| Runtime dependency construction absent | No request-scoped Memory Integration plus governed narrator builder | Added request-scoped runtime builder |
| Modern delivery boundary absent | No API shape for grounded narration versus deterministic fallback | Added governed response schema with access-denied redaction |
| End-to-end restart replay absent | Existing validators covered components independently | Added `scripts/validate_orchestrator_runtime.ps1` |
| Grounding Docker evidence did not name fake value and fake prediction separately | Citation rejection was explicit; adjacent unit tests covered value and prediction rejection | Extended the in-container LLM validator and Docker wrapper |

## Intentionally Preserved Surfaces

The transitional broker routes remain active because the Master State
documents them as an existing repaired Tool 1 and Tool 2 compatibility layer.
Their narration runtime is deterministic and reports
`legacy_broker_llm_runtime_retired`. It is not a competing provider path.

No modern orchestrator SSE route was added. Provider-side pre-grounding
streaming remains forbidden by the approved governance profile.

## Existing Non-Blocking Test Debt

The broad backend suite still has the pre-existing drift documented in the
Master State:

```text
1 stale collection import:
  app/tests/test_spatial_confidence.py imports removed pricing._combine_confidence

8 stale monkeypatch failures:
  tests patch removed pricing.nearest_area route symbols instead of current
  service boundaries
```

These failures are outside the orchestrator activation wiring and were not
modified in this phase.
