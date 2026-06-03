# ValorAI Phase 5.5C.6B Canonical Runtime Path

Decision date: 2026-06-01  
Decision scope: Canonical Phase 5.5C.6 request lifecycle  
Implementation status: Architecture decision only  

## 1. Canonical Path

The canonical Phase 5.5C.6 runtime is:

```text
Authenticated scoped request
  -> Intent Engine
  -> Tool Planner
  -> Tool Executor
  -> Response Composer
  -> Memory Integration Pre-Generation
       -> remember bounded Composer summary
       -> rebuild bounded tenant-scoped MemoryContext
  -> Narration Admission Gate
       -> bind request, Composer response, MemoryContext, citations, and scope
       -> reject denied, unsupported, mismatched, or over-budget narration
       -> create deterministic provider-safe projection
  -> Prompt Assembly
       -> consume one validated scoped narration envelope
       -> emit one bounded prompt
  -> Stateless LLM Provider
       -> generate candidate narration without provider-side memory
  -> Candidate Parser
       -> preserve original provider output
       -> parse without repair
  -> Deterministic Grounding and Governance
       -> validate original candidate against locked deterministic context
       -> reject unsupported claims or citations
  -> Memory Integration Post-Generation, when approved
       -> commit accepted grounded narration and approved provenance
  -> Delivery
       -> deliver Composer-owned frontend payload
       -> attach accepted grounded narration when available
       -> otherwise deliver deterministic fallback status
```

This path adds an optional narration capability. It does not insert a new
truth, decision, execution, calculation, evidence, memory, or delivery owner.

## 2. Existing Approved Chain Remains Intact

The approved Phase 5.5C.5 chain is not rewritten:

| Stage | Existing authority preserved |
| --- | --- |
| Intent Engine | Classifies the request and decides clarification behavior. |
| Tool Planner | Decides which approved Tools are selected. |
| Tool Executor | Executes selected Tools and preserves raw Tool payloads. |
| Response Composer | Computes approved arithmetic, normalizes results, preserves citations, and creates structured response channels. |
| Memory Integration | Remembers the bounded Composer summary and rebuilds governed tenant-scoped context. |

Phase 5.5C.6 begins only after these responsibilities complete.

## 3. Canonical Stage Requirements

### Stage 0: Authentication and Tenant Scope

The request must enter through the existing authenticated tenant boundary.
Foreign, deleted, or invalid resources remain concealed. No narration work is
allowed before authorization succeeds.

### Stage 1: Intent Engine

The deterministic Intent Engine classifies the current turn. If clarification
is required, the governed clarification behavior completes without Tool
execution or LLM narration unless a separately approved clarification
narration policy exists.

### Stage 2: Tool Planner

The deterministic Tool Planner selects only approved Tools. The LLM cannot
add, remove, reorder, or repeat Tool calls.

### Stage 3: Tool Executor

The deterministic Tool Executor invokes the approved Tool Layer. Raw Tool
payloads stop at the Composer boundary and must never enter Prompt Assembly.

### Stage 4: Response Composer

The deterministic Response Composer owns all approved arithmetic,
normalization, compression, and citation preservation. It emits:

1. A bounded `compressed_context` for downstream narration use.
2. A complete frontend-safe payload for authoritative delivery.

The LLM may narrate the bounded context. It may not replace the frontend-safe
payload or recompute any values.

### Stage 5: Memory Integration Pre-Generation

Memory Integration performs its existing governed work:

1. Remember one bounded idempotent Composer summary in existing persistence.
2. Rebuild bounded tenant-scoped `MemoryContext`.
3. Preserve received and persisted citations.
4. Fail closed for foreign, deleted, or denied scope.

This stage is the only approved memory retrieval owner.

### Stage 6: Narration Admission Gate

The Narration Admission Gate creates the only allowed input to Prompt
Assembly: one scoped narration envelope.

Before any provider call, the gate must verify:

1. Authenticated user and workspace binding.
2. Optional scenario binding.
3. Optional broker-session binding.
4. Composed response and memory-context compatibility.
5. Memory status is not `FAILED` or `ACCESS_DENIED`.
6. Intent is approved for narration activation.
7. Citation package membership and immutability.
8. Provider-safe data minimization and redaction.
9. Current-turn content bound and size-limited.
10. Non-evictable prompt content can fit within the approved token budget.

The gate must reject narration before provider egress if any condition fails.

### Stage 7: Prompt Assembly

Prompt Assembly is a pure bounded transformation over the validated envelope.
It receives no raw executor output, raw Tool payload, ORM object, database
row, full transcript, unvalidated scope value, or hidden retrieval result.

Prompt instructions may state the narration policy, but they are not the
enforcement mechanism. Token overflow fails closed.

### Stage 8: Stateless LLM Provider

The provider receives only the minimized provider-safe projection. Provider
invocation must be stateless:

- No provider-managed conversation thread.
- No provider-side memory continuity.
- No hidden retrieval plugin.
- No Tool invocation.
- No autonomous follow-up execution.

ValorAI remains the owner of context and continuity.

### Stage 9: Candidate Parser

The provider response is untrusted. Parsing must preserve the original output
for validation. No deterministic values may be injected into or overwritten
inside the candidate before grounding.

### Stage 10: Deterministic Grounding and Governance

Grounding and governance validate the original candidate against the locked
deterministic context.

The validator must reject:

1. Missing, fabricated, foreign, or unsupported citation references.
2. Unsupported price values or replacement authoritative values.
3. New arithmetic, percentages, deltas, or comparisons not already owned by
   Composer.
4. New ranking, confidence, recommendation, or offer claims not already
   authorized by deterministic context.
5. Forecasts, future-price claims, synthetic trends, ROI, IRR, CAGR, rental
   yield estimates, or investment-return claims.
6. Intent-specific claims outside the approved narration contract.
7. Claims that contradict sparse or insufficient evidence status.

Validation must happen before persistence and before delivery.

### Stage 11: Memory Integration Post-Generation

This stage exists only if accepted narration persistence is explicitly
approved.

When enabled, it may persist only:

1. Grounded accepted narration.
2. The validated conversation binding.
3. Approved provider provenance and grounding outcome metadata.

It must never persist rejected candidate text as accepted assistant memory,
select the latest chat heuristically, or create a second memory system.

### Stage 12: Delivery

Delivery remains outside LLM Integration. API, SSE, or future transport code
owns client delivery.

Delivery sends:

1. The authoritative Composer-owned frontend payload.
2. Optional grounded narration when accepted.
3. Explicit narration status when narration is skipped, unavailable, or
   rejected.
4. Deterministic citation attachments from immutable packages.

## 4. Grounding Timeline

| Gate | When | Purpose | Must complete before |
| --- | --- | --- | --- |
| G0: Authentication and scope | Before deterministic orchestration | Establish authorized tenant scope. | Any scoped retrieval or disclosure. |
| G1: Memory and envelope binding | After Memory Integration, before Prompt Assembly | Ensure Composer response, Memory context, optional scenario, optional broker session, and citations belong together. | Any provider egress. |
| G2: Egress and budget | Before provider invocation | Enforce minimized provider-safe projection and hard prompt budget. | Any provider egress. |
| G3: Candidate grounding | After provider response, before mutation | Reject unsupported claims and citations in original output. | Any persistence or delivery of narration. |
| G4: Persistence approval | After grounding | Permit only Memory-owned commit of accepted narration. | Narrative delivery when commit is required. |
| G5: Delivery approval | Immediately before transport | Deliver Composer payload and only accepted grounded narration. | Client disclosure. |

## 5. Failure Semantics

| Failure condition | Provider contacted | Narration persisted | Narrative delivered | Deterministic Composer payload delivered |
| --- | --- | --- | --- | --- |
| Authentication failure | No | No | No | No scoped disclosure |
| Foreign, deleted, or mismatched scope | No | No | No | No scoped disclosure |
| Memory status `FAILED` or `ACCESS_DENIED` | No | No | No | Only behavior permitted by existing denial policy |
| Unsupported intent | No | No | No | Yes, when otherwise authorized |
| Prompt budget overflow | No | No | No | Yes, when otherwise authorized |
| Provider timeout or error | Attempted | No | No | Yes, when otherwise authorized |
| Provider parse failure | Yes | No | No | Yes, when otherwise authorized |
| Citation validation failure | Yes | No | No | Yes, when otherwise authorized |
| Unsupported claim or arithmetic detected | Yes | No | No | Yes, when otherwise authorized |
| Required Memory-owned post-narration commit failure | Yes | No accepted commit | No | Yes, when otherwise authorized |
| Transport failure after accepted commit | Yes | Yes | Transport-dependent | Retried or recovered under delivery policy |

Narration failure is fail-closed. Authorized deterministic response delivery
may remain available.

## 6. Intent Activation Policy

LLM narration activation must be per-intent and default-off.

| Intent category | Activation rule |
| --- | --- |
| Valuation | Activate only after valuation-specific narration contract and grounding coverage are approved. |
| Explainability | Activate only after explainability-specific narration contract and grounding coverage are approved. |
| Comparable | Activate only after sparse-evidence and citation behavior are approved. |
| Fairness | Activate only after Router-owned fairness output is preserved without new thresholds or calculations. |
| What-if | Activate only after scenario-bound narration and existing Composer-owned delta validation are approved. |
| Negotiation | Activate only after deterministic position, offer-band, and evidence constraints are validated. |
| Investment | Activate only after forecast, return, yield, and synthetic-trend prohibitions are validated. |
| Market Insight | Activate only after descriptive-only and sparse-history controls are validated. |
| Property comparison | Activate only after Composer-owned comparison arithmetic and citation behavior are validated. |
| Clarification or general question | Default to deterministic clarification behavior unless separately approved. |

Generic fallback narration for unsupported intents is prohibited.

## 7. Explicitly Rejected Runtime Paths

The following paths are not canonical:

```text
ComposedResponse
  -> map into legacy BrokerContext
  -> legacy prompt
  -> provider
  -> overwrite model values
  -> legacy grounding
  -> direct chat persistence
  -> return
```

```text
Legacy broker intent
  -> legacy broker plan
  -> legacy tools
  -> legacy prompt and provider
  -> legacy grounding
  -> legacy governance
  -> delivery
```

The first path crosses modern boundaries. The second can bypass the modern
chain. Neither may be activated as Phase 5.5C.6.

## 8. Formal Canonical Path Decisions

### C-01: Narration Begins After Memory Integration

**Decision**

LLM narration begins only after Composer and Memory Integration finish their
approved deterministic responsibilities.

**Reason**

This preserves the locked chain and gives Prompt Assembly governed bounded
context.

**Alternatives considered**

1. Place LLM generation before Composer.
2. Place LLM generation before Memory Integration.
3. Let the LLM choose whether memory is needed.

**Risks**

An early LLM stage would invite raw payload use and independent reasoning.

**Mitigations**

Require the Narration Admission Gate after Memory Integration and prohibit
raw upstream payloads in Prompt Assembly.

**GO / NO-GO impact**

LLM generation before Composer or outside governed Memory context is `NO-GO`.

### C-02: Grounding Occurs Before Generation, After Generation, Before Persistence, and Before Delivery

**Decision**

The runtime uses the full grounding timeline defined in this document.

**Reason**

No single validation point covers tenant leakage, egress minimization,
unsupported output, persistence safety, and delivery safety.

**Alternatives considered**

1. Post-generation validation only.
2. Prompt-only rules.
3. Audit-only review after delivery.

**Risks**

Controls can become duplicated or inconsistently interpreted.

**Mitigations**

Assign each checkpoint a narrow deterministic purpose and make its failure
behavior explicit.

**GO / NO-GO impact**

Missing any required checkpoint is `NO-GO`.

### C-03: Unsupported Narration Uses Deterministic Fallback

**Decision**

If narration cannot safely proceed, use authorized Composer-owned delivery
without model text.

**Reason**

The deterministic response is authoritative and already available.

**Alternatives considered**

1. Use unvalidated provider text.
2. Block all delivery.
3. Generate a second provider response until one passes.

**Risks**

Fallback status can be overlooked by clients.

**Mitigations**

Make narration status explicit and observable.

**GO / NO-GO impact**

Fail-open narrative fallback is `NO-GO`.

## 9. Canonical Runtime Verdict

```text
CANONICAL_RUNTIME_PATH: DEFINED
CANONICAL_RUNTIME_IMPLEMENTATION: NOT YET APPROVED
TARGET_PATH_DECISION: CONDITIONAL_GO
OBSERVED LLM PATHS: NO_GO
```
