# LLM Integration Architecture Decision

Decision date: 2026-06-01  
Decision scope: Phase 5.5C.6A forensic audit  
Decision: **NO-GO**

## Decision Statement

The current LLM Integration implementation must not be approved, promoted,
wired into production routes, or extended.

The approved ValorAI baseline ends at Phase 5.5C.5:

```text
Intent Engine
  -> Tool Planner
  -> Tool Executor
  -> Response Composer
  -> Memory Integration
```

The locked rule remains:

```text
Planner decides.
Executor executes.
Composer computes.
Memory remembers.
Future LLM narrates.
```

The unauthorized package does more than narration. It owns database access,
persists generated chat content, synthesizes citation aliases, relies on a
legacy valuation-centric response schema, and lacks fail-closed tenant binding
and arithmetic enforcement.

## Architecture Review Outcome

| Required property | Outcome |
| --- | --- |
| LLM narrates only | FAIL |
| Composer retains arithmetic authority | FAIL: prompt-only prohibition is not enforcement |
| Composer + Memory retain citation authority | FAIL |
| Memory Integration retains persistence ownership | FAIL |
| Prompt Assembly -> LLM -> Grounding -> Persistence -> Delivery | FAIL: no canonical modern pipeline exists |
| Tenant scope fails closed before provider call | FAIL |
| Provider-side conversation memory absent | PASS |
| SSE and transport remain outside LLM layer | PASS |
| Modern provider abstraction approved | FAIL |
| Formal architecture approval precedes code | FAIL |

## Blocking Findings

### D-01: Unauthorized implementation precedes architecture approval

**Severity:** P1

**Finding:** The repository contains Phase 5.5C.6 code, tests, validators, and
generated artifacts although the phase is deferred pending explicit approval.

**Evidence:** `PROJECT_MASTER_STATE_V2.md:899`;
`pf_scraper/fair-price-eg/MEMORY_INTEGRATION_FINAL_READINESS_REPORT.md:134`.

**Risk:** Governance is inverted: code chooses architecture before review.

**Required Fix:** Keep the phase stopped. Approve architecture before deciding
the disposition of the unauthorized artifacts.

### D-02: Persistence and Memory boundaries are violated

**Severity:** P1

**Finding:** `LLMIntegration` queries messages and persists generated assistant
text directly.

**Evidence:** `backend/app/copilot/orchestrator/llm/integration.py:249-269`;
`pf_scraper/fair-price-eg/MEMORY_GOVERNANCE_AUDIT.md:44-45`.

**Risk:** The LLM layer can persist arbitrary memory and bypass governed
Memory Integration.

**Required Fix:** The approved architecture must keep generated narration
outside persistence until a downstream approved persistence stage accepts it.

### D-03: Citation authority is violated

**Severity:** P1

**Finding:** The adapter invents evidence aliases and zero-priced comparable
wrappers.

**Evidence:** `backend/app/copilot/orchestrator/llm/integration.py:109-142`;
`pf_scraper/fair-price-eg/COMPOSER_CITATION_POLICY.md:83-98`.

**Risk:** Citation provenance is no longer pass-through and tenant-safe.

**Required Fix:** The approved architecture must treat Composer and Memory
citation packages as immutable inputs.

### D-04: Grounding cannot prove narration-only behavior

**Severity:** P1

**Finding:** The adapter mutates authoritative fields before validation and
does not enforce arithmetic, forecast, ranking, confidence, or offer
prohibitions in free text.

**Evidence:** `backend/app/copilot/orchestrator/llm/integration.py:226-249`;
`backend/app/broker/validators/grounding.py:16-53`.

**Risk:** Unsupported LLM claims can pass and be persisted.

**Required Fix:** The approved architecture must validate original model
output after generation and reject unsupported authority claims before
persistence or delivery.

### D-05: Canonical runtime path is unresolved

**Severity:** P1

**Finding:** A live legacy broker LLM runtime coexists with a detached modern
package that reuses legacy providers and validators.

**Evidence:** `backend/app/broker/llm/runtime/narration.py:26-138`;
`backend/app/broker/orchestrator/core.py:205-234`;
`backend/app/copilot/orchestrator/llm/integration.py:11-30`.

**Risk:** Activation can bypass the modern Composer and Memory chain.

**Required Fix:** Formal review must select one canonical runtime and define
whether the legacy path is retired, isolated, or governed separately.

### D-06: Tenant and provider egress boundaries are unresolved

**Severity:** P1

**Finding:** Independently supplied tenant identifiers and contexts are not
bound before provider use. Broad scoped context is sent to external endpoints
without an approved egress contract.

**Evidence:** `backend/app/copilot/orchestrator/llm/integration.py:170-185`;
`backend/app/copilot/orchestrator/llm/prompts.py:151-164`;
`backend/app/broker/llm/providers/http.py:20-36`;
`backend/app/broker/llm/providers/http.py:77-85`.

**Risk:** Cross-tenant caller mistakes and unnecessary external disclosure are
possible.

**Required Fix:** Formal review must approve a scoped narration envelope,
pre-prompt binding checks, egress allowlist, redaction rules, provider
retention assumptions, and stateless generation requirement.

### D-07: Validation evidence is insufficient

**Severity:** P1

**Finding:** The validator hand-builds upstream contracts, scans an incomplete
forbidden list, and falls back to SQLite through an invalid connectivity
probe.

**Evidence:** `backend/app/scripts/validate_llm_integration.py:30-72`;
`backend/app/scripts/validate_llm_integration.py:133-219`;
`backend/app/scripts/validate_llm_integration.py:292-314`.

**Risk:** A PASS does not demonstrate architecture compliance.

**Required Fix:** Any future validator must exercise the approved runtime
chain and assert boundaries adversarially.

## Required Architecture Work Before Any GO Review

1. Approve one canonical Phase 5.5C.6 sequence:

```text
ComposedResponse + MemoryContext + approved scoped current-turn envelope
  -> Prompt Assembly
  -> stateless LLM Provider
  -> deterministic Grounding Validation
  -> approved Persistence Stage
  -> Delivery Stage
```

2. Define immutable citation pass-through from Composer and Memory only.
3. Define a fail-closed tenant-bound narration envelope.
4. Define deterministic rejection rules for arithmetic, ranking, confidence,
   price estimation, forecasts, and offer recommendations.
5. Define supported intents and a modern narration response contract.
6. Define the disposition of the legacy broker LLM runtime.
7. Define provider egress minimization, redaction, retention, timeout, retry,
   schema, and statelessness rules.
8. Define validation criteria before implementation resumes.

## Final Decision

```text
ARCHITECTURE DECISION: NO-GO
IMPLEMENTATION CONTINUATION: STOP
SOURCE REPAIR DURING THIS AUDIT: NOT PERMITTED
NEXT REQUIRED ACTION: FORMAL ARCHITECTURE REVIEW
```

