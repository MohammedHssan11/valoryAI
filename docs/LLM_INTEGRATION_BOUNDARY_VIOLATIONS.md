# LLM Integration Boundary Violations

Audit date: 2026-06-01  
Phase: 5.5C.6A forensic audit  
Decision: **NO-GO**

This register lists boundary violations found in the unauthorized
`backend/app/copilot/orchestrator/llm` implementation and its related
touchpoints. No repair is included.

## V-01: Governance gate bypass

**Severity:** P1

**Finding:** Phase 5.5C.6 code, tests, validators, and generated artifacts exist
before explicit architecture approval.

**Evidence:** `PROJECT_MASTER_STATE_V2.md:899`;
`pf_scraper/fair-price-eg/MEMORY_INTEGRATION_FINAL_READINESS_REPORT.md:134`;
`backend/app/copilot/orchestrator/llm/`;
`backend/app/tests/test_llm_integration.py`;
`backend/app/scripts/validate_llm_integration.py`;
`scripts/validate_llm_integration.ps1`.

**Risk:** An implementation-first design can silently redefine approved
ownership boundaries.

**Required Fix:** Keep Phase 5.5C.6 stopped until a formal architecture review
approves the design.

## V-02: Persistence ownership leakage

**Severity:** P1

**Finding:** The LLM adapter queries messages and persists generated assistant
text directly.

**Evidence:** `backend/app/copilot/orchestrator/llm/integration.py:249-269`.
Approved Memory Integration write access is limited to one bounded
`decision_history` summary:
`pf_scraper/fair-price-eg/MEMORY_GOVERNANCE_AUDIT.md:44-45`.

**Risk:** The LLM layer can persist arbitrary memory and write into the wrong
workspace chat.

**Required Fix:** Move all persistence outside the LLM boundary and route it
through the explicitly approved persistence owner.

## V-03: Citation alias fabrication

**Severity:** P1

**Finding:** The adapter creates evidence aliases and fallback IDs:
`comp.<id>`, `valuation.authoritative`, and `explainability.truth_layer`.

**Evidence:** `backend/app/copilot/orchestrator/llm/integration.py:109-142`;
`pf_scraper/fair-price-eg/COMPOSER_CITATION_POLICY.md:83-98`.

**Risk:** Citation authority moves away from Composer and Memory. Deferred
`evidence_id` behavior is introduced without approval.

**Required Fix:** Pass Composer and Memory citation packages through unchanged.

## V-04: Comparable evidence corruption

**Severity:** P1

**Finding:** Comparable IDs are converted into synthetic
`BrokerComparableEvidence` records with `price_egp=0`.

**Evidence:** `backend/app/copilot/orchestrator/llm/integration.py:109-116`.

**Risk:** Grounding validation sees a replacement record rather than received
evidence. Comparable price claims cannot be validated against authoritative
prices.

**Required Fix:** Do not synthesize comparable records. Validate only received
Composer-owned structured evidence.

## V-05: Grounding mutation before validation

**Severity:** P1

**Finding:** Parsed LLM `authoritative_values` are replaced with deterministic
values before grounding validation.

**Evidence:** `backend/app/copilot/orchestrator/llm/integration.py:226-237`.

**Risk:** Hallucinated structured authoritative values are masked instead of
detected and rejected.

**Required Fix:** Validate original model output first. Attach deterministic
delivery fields only in an approved downstream stage.

## V-06: Narration-only arithmetic boundary is unenforced

**Severity:** P1

**Finding:** Prompts prohibit calculation, but the invoked validator checks
only authoritative structured values and citation arrays. The new path does
not invoke response governance.

**Evidence:** `backend/app/copilot/orchestrator/llm/prompts.py:18-24`;
`backend/app/broker/validators/grounding.py:16-53`;
`backend/app/copilot/orchestrator/llm/integration.py:236-249`.

**Risk:** LLM free text can calculate deltas or percentages, rank properties,
compute confidence, estimate prices, forecast values, or recommend offers and
still pass.

**Required Fix:** Approve and enforce a deterministic post-LLM narration
validator for every prohibited claim category.

## V-07: Tenant-bound envelope is missing

**Severity:** P1

**Finding:** `narrate()` accepts independently supplied identifiers and
contexts without verifying they belong together. `scenario_id` and
`broker_session_id` are unused.

**Evidence:** `backend/app/copilot/orchestrator/llm/integration.py:170-185`.

**Risk:** Mismatched context can be sent to a provider or persisted into the
wrong workspace.

**Required Fix:** Require a single fail-closed scoped narration envelope and
verify all tenant, scenario, session, response, and citation bindings before
prompt assembly.

## V-08: Legacy schema cannot ground modern intent coverage

**Severity:** P1

**Finding:** The adapter advertises all modern intents but maps only valuation
and explainability summaries into a legacy broker context.

**Evidence:** `backend/app/copilot/orchestrator/llm/prompts.py:38-49`;
`backend/app/copilot/orchestrator/llm/integration.py:39-84`.

**Risk:** Tool 3-8 and property-comparison narration can be generated without
intent-specific validation.

**Required Fix:** Define an approved modern narration contract and validate
each supported intent explicitly.

## V-09: Competing activation paths

**Severity:** P1

**Finding:** A live legacy broker LLM runtime and a detached modern LLM package
coexist. Both reuse broker provider configuration.

**Evidence:** `backend/app/broker/llm/runtime/narration.py:26-138`;
`backend/app/broker/orchestrator/core.py:205-234`;
`backend/app/copilot/orchestrator/llm/integration.py:11-30`;
`backend/app/core/config.py:161-181`.

**Risk:** Enabling one flag can activate a path that bypasses the modern
Composer and Memory chain.

**Required Fix:** Select one canonical runtime architecture and explicitly
retire, isolate, or govern the other path before activation.

## V-10: Prompt input contract drift

**Severity:** P2

**Finding:** Prompt assembly accepts raw `user_message` in addition to
`ComposedResponse` and `MemoryContext`. The budget loop can return an
over-budget prompt when non-evictable inputs remain oversized.

**Evidence:** `backend/app/copilot/orchestrator/llm/prompts.py:62-68`;
`backend/app/copilot/orchestrator/llm/prompts.py:91-132`;
`backend/app/copilot/orchestrator/llm/prompts.py:151-164`.

**Risk:** The approved assembly boundary is ambiguous and token governance can
fail open.

**Required Fix:** Approve a bounded current-turn envelope and hard fail-closed
budget behavior.

## V-11: Provider egress policy is undefined

**Severity:** P2

**Finding:** Prompt payloads include scoped workspace, scenario, session,
property, assumption, tool-event, valuation, and citation data. Providers send
that payload to external HTTP endpoints without an approved minimization or
redaction contract.

**Evidence:** `backend/app/copilot/orchestrator/llm/prompts.py:151-164`;
`backend/app/broker/llm/providers/http.py:20-36`;
`backend/app/broker/llm/providers/http.py:77-85`.

**Risk:** Tenant-scoped internal identifiers and property context can be
disclosed unnecessarily to a provider.

**Required Fix:** Approve explicit egress allowlists, redaction rules,
retention assumptions, and stateless provider requirements.

## V-12: Provider abstraction is incomplete

**Severity:** P2

**Finding:** The provider abstraction supports two vendors but is owned by the
legacy broker namespace. Retry configuration exists but is unused, and
provider structured-output behavior differs.

**Evidence:** `backend/app/broker/llm/providers/factory.py:8-25`;
`backend/app/broker/llm/providers/http.py:12-115`;
`backend/app/core/config.py:173-181`.

**Risk:** Modern orchestration inherits incomplete legacy operational
semantics. This is not single-vendor lock-in, but it is premature reuse.

**Required Fix:** Approve a modern provider-neutral contract with consistent
timeout, retry, error, schema, and statelessness behavior.

## V-13: Validator certifies the wrong boundary

**Severity:** P1

**Finding:** The dedicated validator labels the implementation
`llm_narrator_only` using a narrow scan. It permits SQLAlchemy, models, and
`CopilotService`, hand-builds upstream results, and uses an invalid SQLAlchemy
probe that falls back to SQLite.

**Evidence:** `backend/app/scripts/validate_llm_integration.py:30-43`;
`backend/app/scripts/validate_llm_integration.py:56-72`;
`backend/app/scripts/validate_llm_integration.py:133-157`;
`backend/app/scripts/validate_llm_integration.py:160-219`;
`backend/app/scripts/validate_llm_integration.py:292-314`.

**Risk:** Validation can pass while major ownership violations remain.

**Required Fix:** Replace the validator only after architecture approval with
a real end-to-end boundary audit and adversarial cases.

## Confirmed Non-Violations

- No intent classification logic was added to the new LLM package.
- No planning or Tool execution logic was added to the new LLM package.
- No raw `ExecutionResult` or raw Tool payload enters prompt assembly.
- No ORM entity enters prompt assembly directly.
- No SSE, WebSocket, or frontend transport code exists in the new package.
- Existing SSE transport remains API-owned in
  `backend/app/api/routes/broker.py:115-212`.
- Providers send no provider-side conversation or thread identifier.
- `MemoryContext` is not mutated in place.

## ARCHITECTURE DECISION

**NO-GO**

The violations are architecture blockers, not cleanup tasks. Phase 5.5C.6
must remain stopped pending formal approval.
