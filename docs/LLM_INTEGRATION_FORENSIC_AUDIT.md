# Phase 5.5C.6A LLM Integration Forensic Architecture Audit

Audit date: 2026-06-01  
Audit mode: Read-only forensic architecture audit  
Authoritative source read completely: `PROJECT_MASTER_STATE_V2.md` lines 1-997  
Decision: **NO-GO**

## Scope

The approved implemented baseline ends at Phase 5.5C.5 Memory Integration.
`PROJECT_MASTER_STATE_V2.md:899` says Phase 5.5C.6 LLM Integration may be
defined and implemented only after explicit phase approval.
`pf_scraper/fair-price-eg/MEMORY_INTEGRATION_FINAL_READINESS_REPORT.md:134`
records Phase 5.5C.6 as deferred pending explicit approval.

The forensic inventory found unauthorized Phase 5.5C.6 artifacts:

```text
backend/app/copilot/orchestrator/llm/__init__.py
backend/app/copilot/orchestrator/llm/contracts.py
backend/app/copilot/orchestrator/llm/prompts.py
backend/app/copilot/orchestrator/llm/integration.py
backend/app/tests/test_llm_integration.py
backend/app/scripts/validate_llm_integration.py
scripts/validate_llm_integration.ps1
backend/llm-validation.sqlite3
```

Related legacy broker LLM providers, prompts, runtime, grounding validator,
governance layer, broker orchestrator, API route, Composer contract, Memory
contract, and Memory Integration implementation were also audited.

No source code, migration, test, or runtime state was modified by this audit.
Validators were inspected statically and were not executed.

## Observed Runtime Shapes

### Unauthorized modern package

The implemented success path in
`backend/app/copilot/orchestrator/llm/integration.py:170-278` is:

```text
LLMIntegration.narrate
  -> map ComposedResponse into legacy BrokerContext
  -> PromptAssembler.build
  -> provider.generate
  -> parse legacy BrokerAnalyticalResponse JSON
  -> overwrite authoritative_values
  -> legacy GroundingValidator.validate
  -> query latest workspace chat
  -> persist generated assistant message through CopilotService
  -> return LLMNarrationResult
```

This package is detached from production routes. Repository search found its
imports only in its package initializer, its dedicated tests, and its
validator. There is no approved production delivery touchpoint.

### Live legacy broker path

The separate legacy path in
`backend/app/broker/orchestrator/core.py:126-287` is:

```text
classify legacy broker intent
  -> build legacy reasoning plan
  -> execute legacy broker tools
  -> assemble legacy BrokerContext
  -> legacy prompt assembly and optional LLM generation
  -> grounding validation
  -> response governance
  -> broker-session persistence
  -> API or SSE delivery
```

The legacy provider is disabled by default through
`backend/app/core/config.py:161`, but it can be activated independently of the
modern Copilot Orchestrator. The new package reuses this legacy provider and
validator stack instead of defining an approved Phase 5.5C.6 boundary.

## Checklist Results

| Audit area | Result | Summary |
| --- | --- | --- |
| Boundary ownership | FAIL | LLM adapter directly queries and writes persistence. |
| Citation ownership | FAIL | Adapter synthesizes deferred evidence IDs and zero-price comparable wrappers. |
| Grounding placement | FAIL | Local order is nominally close, but the canonical pipeline is absent and pre-validation mutation masks drift. |
| Arithmetic authority | FAIL | Prompt instructions prohibit arithmetic, but post-LLM enforcement does not. |
| Provider architecture | FAIL | Multi-provider support exists, but the abstraction is legacy-coupled and incomplete. |
| Memory boundary | FAIL | Generated assistant text is persisted outside Memory Integration. |
| Streaming boundary | PASS WITH QUALIFICATION | New package owns no SSE. Existing SSE remains API-owned. Canonical modern delivery remains undefined. |
| Tenant isolation | FAIL | Scoped context is accepted without binding validation; provider egress minimization is undefined. |
| Prompt assembly | FAIL | No raw executor payloads or ORM entities enter directly, but an ungoverned third input and fail-open token budget remain. |
| Governance review | FAIL | Unauthorized implementation exists before architecture approval. |

## Findings

### F-01: Phase approval was bypassed

**Severity:** P1

**Finding:** Phase 5.5C.6 implementation artifacts exist although the
authoritative roadmap defers implementation until explicit approval.

**Evidence:** `PROJECT_MASTER_STATE_V2.md:899`;
`pf_scraper/fair-price-eg/MEMORY_INTEGRATION_FINAL_READINESS_REPORT.md:129-135`;
the artifact inventory above.

**Risk:** Review is forced to reverse-engineer a de facto design after code
creation. Boundary decisions can be silently locked in by tests and validators
that were written against an unapproved implementation.

**Required Fix:** Stop Phase 5.5C.6 implementation work. Obtain an explicit
architecture decision before any implementation is retained, promoted, or
wired into runtime.

### F-02: LLM Integration bypasses Memory Integration ownership

**Severity:** P1

**Finding:** `LLMIntegration` owns a SQLAlchemy session, queries messages, and
persists generated assistant text through `CopilotService.create_message`.

**Evidence:** `backend/app/copilot/orchestrator/llm/integration.py:162-165`;
`backend/app/copilot/orchestrator/llm/integration.py:249-269`;
`backend/app/services/copilot_service.py:253-269`.
The approved Memory write boundary is one bounded idempotent
`decision_history` summary:
`pf_scraper/fair-price-eg/MEMORY_GOVERNANCE_AUDIT.md:44-45`.

**Risk:** The LLM layer can persist arbitrary generated narrative, select the
latest chat in a workspace rather than an explicitly bound chat, and create
history outside the governed Memory Integration layer.

**Required Fix:** Remove persistence responsibility from the LLM boundary in
the approved design. Persistence must be a separate downstream stage owned by
Memory Integration or another explicitly approved persistence owner.

### F-03: Citation authority is violated by synthesized evidence IDs

**Severity:** P1

**Finding:** The adapter creates `comp.<id>`, `valuation.authoritative`, and
`explainability.truth_layer` evidence IDs outside Composer and Memory. It also
creates zero-priced comparable wrappers.

**Evidence:** `backend/app/copilot/orchestrator/llm/integration.py:109-142`.
The approved citation policy defers `evidence_id` and prohibits creating
evidence IDs:
`pf_scraper/fair-price-eg/COMPOSER_CITATION_POLICY.md:15-19`;
`pf_scraper/fair-price-eg/COMPOSER_CITATION_POLICY.md:83-98`.

**Risk:** Citation pass-through becomes a new citation system. Fabricated
wrappers can misrepresent evidence coverage, lose comparable prices, and blur
tenant-scoped provenance.

**Required Fix:** Preserve Composer and Memory citation packages unchanged.
Do not mint aliases, fallback evidence IDs, or replacement comparable records
inside LLM Integration.

### F-04: Grounding validation does not enforce narration-only behavior

**Severity:** P1

**Finding:** The new path invokes only the legacy `GroundingValidator`. It
overwrites `response.authoritative_values` before validation and does not run
the existing response governance layer.

**Evidence:** `backend/app/copilot/orchestrator/llm/integration.py:226-249`;
`backend/app/broker/validators/grounding.py:16-53`;
`backend/app/broker/governance/response.py:48-70`.

**Risk:** An LLM response can include unsupported percentages, deltas,
rankings, confidence claims, price estimates, forecasts, or offer
recommendations in free text and still pass. Overwriting authoritative values
before validation masks model drift instead of detecting it.

**Required Fix:** Define an approved post-LLM grounding contract that validates
the original model output against Composer-owned values and rejects unsupported
numeric or decision claims. Do not mutate model output before drift detection.

### F-05: Tool 3-8 and comparison narration are not grounded by the legacy schema

**Severity:** P1

**Finding:** Prompt instructions request narration for all modern intents, but
the compatibility mapper extracts only valuation and explainability summaries.
Several modern intents map to legacy fallback intent values.

**Evidence:** `backend/app/copilot/orchestrator/llm/prompts.py:38-49`;
`backend/app/copilot/orchestrator/llm/integration.py:39-50`;
`backend/app/copilot/orchestrator/llm/integration.py:58-84`.

**Risk:** Negotiation, investment, market-insight, fairness, what-if, and
property-comparison language can be generated without intent-specific
grounding validation. The legacy `BrokerAnalyticalResponse` contract is not an
approved narration contract for the modern chain.

**Required Fix:** Approve a modern narration contract derived from
`ComposedResponse` and `MemoryContext`. Validate every supported intent's
allowed fields and fail closed for unsupported intents.

### F-06: Tenant scope is accepted without fail-closed binding

**Severity:** P1

**Finding:** `narrate()` accepts `user_id`, `workspace_id`, `scenario_id`,
`broker_session_id`, `ComposedResponse`, and `MemoryContext`, but does not
verify that the contexts belong together. `scenario_id` and
`broker_session_id` are unused after receipt.

**Evidence:** `backend/app/copilot/orchestrator/llm/integration.py:170-185`;
`backend/app/copilot/orchestrator/llm/integration.py:249-269`.
The approved Memory layer performs fail-closed scope checks:
`backend/app/copilot/orchestrator/memory/integration.py:421-476`.

**Risk:** A caller error or future route mistake can prompt with one tenant's
memory while persisting into another tenant's workspace. The provider can
receive mismatched scoped context before any failure is detected.

**Required Fix:** Require and validate one approved scoped narration envelope.
Reject `FAILED` and `ACCESS_DENIED` memory contexts and any workspace,
scenario, broker-session, citation, or response mismatch before prompt
assembly.

### F-07: Two competing LLM architectures exist

**Severity:** P1

**Finding:** The repository contains a live legacy broker LLM runtime and a
detached modern Copilot Orchestrator LLM package. The modern package imports
legacy providers and validators, while the live broker path can be enabled
independently.

**Evidence:** `backend/app/broker/llm/runtime/narration.py:26-138`;
`backend/app/broker/orchestrator/core.py:205-234`;
`backend/app/copilot/orchestrator/llm/integration.py:11-30`;
`backend/app/core/config.py:161-181`.

**Risk:** Runtime activation can bypass the approved modern
Intent -> Planner -> Executor -> Composer -> Memory chain. Ownership,
grounding, persistence, and delivery behavior depend on which dormant path is
enabled.

**Required Fix:** Architecture review must select one canonical LLM path,
define the fate of the legacy broker runtime, and prohibit activation until
the selected dependency direction is documented and approved.

### F-08: Prompt assembly contract is only partially governed

**Severity:** P2

**Finding:** The assembler correctly consumes compressed Composer context and
bounded MemoryContext summaries, but also accepts raw `user_message` as a
third boundary input. If fixed current-turn inputs alone exceed budget, the
loop exits and returns an over-budget prompt.

**Evidence:** `backend/app/copilot/orchestrator/llm/prompts.py:62-68`;
`backend/app/copilot/orchestrator/llm/prompts.py:91-132`;
`backend/app/copilot/orchestrator/llm/prompts.py:151-164`.

**Risk:** The literal approved input rule, "Only ComposedResponse +
MemoryContext enter prompt assembly," is not met. Oversized prompts can fail
open, and raw user text reaches the provider without an approved envelope or
explicit injection-handling policy.

**Required Fix:** Architecture review must define how the current user turn is
represented in the approved envelope, impose hard size limits, and fail closed
when sacred inputs exceed budget.

### F-09: Provider abstraction is not vendor locked, but it is incomplete

**Severity:** P2

**Finding:** The reused provider factory supports OpenAI and Gemini, so it is
not single-vendor locked. It remains coupled to the legacy broker namespace,
uses broker-prefixed configuration, exposes a retry setting that providers do
not use, and sends broad scoped context to external endpoints without an
approved redaction policy.

**Evidence:** `backend/app/broker/llm/providers/factory.py:8-25`;
`backend/app/broker/llm/providers/http.py:12-115`;
`backend/app/core/config.py:173-181`;
`pf_scraper/fair-price-eg/docker-compose.yml:42-61`.

**Risk:** Operational behavior differs by provider, egress policy is
undefined, and the modern orchestrator inherits legacy configuration and
failure semantics. Provider-side conversation memory is not used, which is a
positive control.

**Required Fix:** Approve a provider-neutral modern boundary with explicit
stateless generation, data minimization, timeout, retry, error, structured
output, and provider-capability rules.

### F-10: The dedicated validator can report false confidence

**Severity:** P1

**Finding:** The validator scans a narrow forbidden-term list, hand-builds
`ExecutionResult` and `ComposedResponse`, and uses an invalid SQLAlchemy
connectivity probe that drives local fallback to SQLite. It does not test the
modern runtime chain, cross-tenant mismatch, arbitrary persistence, citation
aliasing, or unsupported arithmetic.

**Evidence:** `backend/app/scripts/validate_llm_integration.py:30-43`;
`backend/app/scripts/validate_llm_integration.py:56-72`;
`backend/app/scripts/validate_llm_integration.py:133-157`;
`backend/app/scripts/validate_llm_integration.py:160-219`;
`backend/app/scripts/validate_llm_integration.py:292-314`.

**Risk:** A passing validator can incorrectly label the package
`llm_narrator_only` while the package owns database access and persistence.
The persisted `backend/llm-validation.sqlite3` artifact is consistent with the
fallback path having executed previously.

**Required Fix:** After architecture approval, replace the validator contract
with an end-to-end, fail-closed audit that uses real approved upstream
components, real scope checks, static dependency allowlists, adversarial
grounding cases, and explicit persistence and egress assertions.

## Positive Controls Observed

- Intent classification remains in the deterministic Intent Engine.
- Planning remains in the deterministic Tool Planner.
- Tool execution remains in the deterministic Tool Executor.
- Approved arithmetic remains implemented in Response Composer:
  `backend/app/copilot/orchestrator/composer/composer.py:92-99` and
  `backend/app/copilot/orchestrator/composer/composer.py:530-558`.
- Prompt assembly does not directly consume raw `ExecutionResult`, raw Tool
  payloads, or ORM entities.
- `MemoryContext` is frozen and the LLM package does not mutate it in place.
- External HTTP providers are stateless and send no provider conversation ID.
- The unauthorized modern package contains no SSE, WebSocket, or frontend
  transport code.
- Existing SSE ownership remains in the API route:
  `backend/app/api/routes/broker.py:115-212`.

## ARCHITECTURE DECISION

**NO-GO**

The current Phase 5.5C.6 implementation would not pass formal architecture
review. It was created before approval, bypasses Memory Integration for
persistence, synthesizes citation aliases, does not enforce narration-only
output, lacks fail-closed tenant binding, reuses a legacy valuation-centric
schema for modern intents, and is validated by a harness that can certify
false positives.

The correct governance action is to stop implementation work and complete an
explicit architecture review before any Phase 5.5C.6 code is retained,
repaired, activated, or extended.
