# Orchestrator Runtime Docker Validation Report

Status date: 2026-06-02

## Commands

```powershell
.\scripts\validate_orchestrator_runtime.ps1
.\scripts\validate_llm_integration.ps1
docker compose exec -T backend python -m app.scripts.run_migrations --verify
```

All commands were run from:

```text
pf_scraper/fair-price-eg
```

## Runtime Replay Result

```text
docker_validation = PASS
endpoint = /v1/copilot/orchestrator/respond
runtime_id = COPILOT_ORCHESTRATOR_LLM_V1
backend_restart_replay_equal = true
postgres_restart_replay_equal = true
access_denied_status = ACCESS_DENIED
access_denied_response_redacted = true
```

## Required Intent Coverage

| Case | Intent | Tool result | Composition | Delivery |
| --- | --- | --- | --- | --- |
| Runtime validation | `VALUATION` | Tool 1, `TruthLayer`, fair price `85000` | `SUCCESS` | `DETERMINISTIC_FALLBACK` |
| Property comparison | `PROPERTY_COMPARISON` | Property A Tool 1 plus Property B Tool 1, both `TruthLayer` | `SUCCESS` | `DETERMINISTIC_FALLBACK` |
| Negotiation | `NEGOTIATION` | Tool 6, `TruthLayer` | `SUCCESS` | `DETERMINISTIC_FALLBACK` |
| Investment | `INVESTMENT` | Tool 7, `TruthLayer` | `SUCCESS` | `DETERMINISTIC_FALLBACK` |
| Market insight | `MARKET_INSIGHT` | Tool 8, `TruthLayer` | `SUCCESS` | `DETERMINISTIC_FALLBACK` |
| Clarification | `GENERAL_QUESTION` | No Tool invocation | `CLARIFICATION_REQUIRED` | `DETERMINISTIC_FALLBACK` |

Deterministic fallback is expected because live Gemini traffic remains
default-off.

## Grounding Rejection Result

```text
accepted_status = ACCEPT_NARRATION
grounding_status = ACCEPT_NARRATION
citation_rejection_status = REJECT_NARRATION
fake_value_rejection_status = REJECT_NARRATION
fake_prediction_rejection_status = REJECT_NARRATION
fail_closed_transport_status = REJECT_NARRATION
tenant_isolation_status = ACCESS_DENIED
tenant_isolation_provider_calls = 0
legacy_python_file_count = 0
target_runtime_count = 1
backend_restart_fingerprint_stable = true
database_restart_fingerprint_stable = true
docker_validation = PASS
```

The grounding cases use the approved modern pipeline with a deterministic
mock Gemini transport inside the backend container. No live Gemini credential
was configured or required.

## Infrastructure Result

```text
backend = healthy
db = healthy
migration_verify_success
```
