# ValorAI Phase 5.5C.6B Formal Architecture Review

Review date: 2026-06-01  
Review mode: Final formal architecture review after forensic audit  
Review scope: Phase 5.5C.6 LLM Integration architecture only  
Implementation work during review: Prohibited  

## 1. Authoritative Sources

This review is based only on the following authoritative documents, each read
completely:

1. `PROJECT_MASTER_STATE_V2.md`
2. `LLM_INTEGRATION_FORENSIC_AUDIT.md`
3. `LLM_INTEGRATION_BOUNDARY_VIOLATIONS.md`
4. `LLM_INTEGRATION_ARCHITECTURE_DECISION.md`

The documents provide sufficient information for an architecture decision.
No implementation assumption is required.

## 2. Executive Decision

The attempted Phase 5.5C.6 implementation is not an approvable architecture.
It must not be treated as the canonical runtime, activated, promoted, or used
as the basis for implicit approval.

A Phase 5.5C.6 architecture may exist only as a constrained narration layer
after the locked deterministic chain:

```text
Intent Engine
  -> Tool Planner
  -> Tool Executor
  -> Response Composer
  -> Memory Integration
  -> Narration Admission Gate
  -> Prompt Assembly
  -> Stateless LLM Provider
  -> Deterministic Grounding and Governance
  -> Memory-owned Post-Narration Commit, when approved
  -> Delivery
```

The architecture is conditionally acceptable because an LLM can narrate
locked deterministic context without taking ownership of decisions,
execution, calculations, memory, citations, tenancy, or delivery.

```text
ARCHITECTURE_DECISION: CONDITIONAL_GO
EXISTING_ATTEMPTED_IMPLEMENTATION: NO_GO
IMPLEMENTATION_CONTINUATION: STOP UNTIL APPROVAL REQUIREMENTS ARE ACCEPTED
```

## 3. Locked Invariant

The governing rule remains unchanged:

```text
Planner decides.
Executor executes.
Composer computes.
Memory remembers.
Future LLM narrates.
```

The LLM is not a new reasoning authority. It is an optional presentation
adapter for already governed context. Any architecture that allows the LLM
layer to select Tools, calculate values, create evidence, retrieve memory,
persist memory, bind tenants, or control delivery violates the locked chain.

## 4. Objective Decisions

| Objective | Formal decision |
| --- | --- |
| Allowed LLM responsibilities | Bounded prompt construction, stateless provider invocation, parsing of untrusted candidate narration, and return of provider metadata only. |
| Responsibilities the LLM must never own | Intent classification, planning, Tool selection, Tool execution, orchestration, valuation, arithmetic, comparisons, ranking, forecasting, offer creation, citation creation, citation mutation, tenant binding, database access, memory retrieval, persistence, grounding approval, transport, or streaming. |
| Data allowed into Prompt Assembly | One fail-closed scoped narration envelope containing bounded current-turn content, Composer-owned compressed context, Memory-owned bounded summaries, immutable citation packages, supported-intent markers, and internal binding metadata required for deterministic checks. |
| Data forbidden from Prompt Assembly | Raw executor payloads, `ExecutionPlan`, raw Tool payloads, ORM entities, database rows, unrestricted transcripts, unvalidated scope identifiers, authentication secrets, provider secrets, foreign or deleted scope data, access-denied memory, fabricated evidence, and over-budget content. |
| Persistence before LLM | Existing deterministic persistence remains allowed under its existing owner. Memory Integration may remember the bounded Composer summary and rebuild `MemoryContext` before narration. |
| Persistence inside LLM | Forbidden. The LLM boundary must be stateless and must have no database or memory service access. |
| Persistence after LLM | Optional only after grounding approval and only through a Memory-owned downstream commit. Failed or rejected candidate narration must never be persisted as accepted assistant content. |
| Citation packages | Immutable. Composer and Memory remain the only upstream citation owners. |
| Grounding placement | Deterministic admission checks before generation; original-output validation after generation; approval required before persistence and before delivery. |
| Modern narration contract | Required. Legacy valuation-centric response contracts are insufficient for modern intents. |
| Legacy broker LLM runtime | Isolate immediately and retire as an activation path before modern LLM activation. The non-LLM broker adapter may remain transitional. |
| Canonical runtime path | Defined by this review, but not currently implemented or approved for activation. |

## 5. Formal Architecture Decisions

### A-01: LLM Integration Is Narration-Only

**Decision**

LLM Integration may own only bounded prompt assembly, invocation of an
approved stateless provider, parsing of the provider response as untrusted
candidate narration, and return of provider execution metadata.

**Reason**

The deterministic chain already owns classification, planning, execution,
calculation, compression, citations, and memory. Allowing the LLM to duplicate
any of these responsibilities creates competing truth systems and makes
governance dependent on model behavior.

**Alternatives considered**

1. Allow the LLM to reason over raw Tool results.
2. Allow the LLM to choose Tools or trigger follow-up execution.
3. Allow the LLM to calculate comparisons or fill missing values.
4. Omit the LLM entirely.

**Risks**

Even a narration-only model can produce unsupported numeric or decision claims
in prose.

**Mitigations**

Treat provider output as untrusted candidate text, validate the original
output deterministically, and deliver the Composer-owned structured payload
as the authoritative channel.

**GO / NO-GO impact**

Any broader LLM ownership is `NO-GO`. Narration-only ownership is required for
`CONDITIONAL_GO`.

### A-02: Prompt Assembly Receives One Scoped Narration Envelope

**Decision**

Prompt Assembly must accept one fail-closed scoped narration envelope. The
envelope may contain:

1. Bounded current-turn content, explicitly marked as untrusted user input.
2. Composer-owned `compressed_context`, status, and supported-intent markers.
3. Memory-owned bounded summaries selected by Memory Integration.
4. Composer and Memory citation packages preserved without mutation.
5. Internal scope-binding metadata needed for deterministic validation.

Internal tenant identifiers are validation metadata. They must not be sent to
an external provider unless an explicit egress allowlist proves they are
necessary.

**Reason**

The forensic audit found a third raw `user_message` input and independently
supplied scope values. A single envelope prevents hidden input expansion and
requires scope validation before provider egress.

**Alternatives considered**

1. Permit Prompt Assembly to receive `ComposedResponse`, `MemoryContext`, and
   raw user text as independent arguments.
2. Send full chat transcripts.
3. Send raw `frontend_payload`.
4. Send raw executor output for model flexibility.

**Risks**

User text can contain prompt-injection instructions. Compressed context can
still contain more tenant-scoped information than the narration requires.

**Mitigations**

Bound the current turn, frame it as data rather than instruction, apply an
egress allowlist and redaction policy, reject over-budget envelopes, and
validate the output independently of prompt compliance.

**GO / NO-GO impact**

Independent unbound inputs or fail-open token handling are `NO-GO`.

### A-03: LLM Integration Owns No Persistence

**Decision**

Persistence is permitted before and after LLM generation only under Memory
Integration ownership. No persistence exists inside LLM Integration.

Before generation, the existing Memory Integration behavior may persist one
bounded idempotent Composer summary and rebuild governed `MemoryContext`.
After generation, accepted narration may be committed only by an explicitly
approved Memory-owned downstream operation after grounding approval.

**Reason**

The attempted adapter queried messages and persisted generated assistant text
directly. That bypassed the approved memory boundary and could select the
wrong chat.

**Alternatives considered**

1. Allow the LLM adapter to call the Copilot persistence service.
2. Persist all provider output before validation for debugging.
3. Never persist accepted narration.
4. Persist accepted narration through a separate non-Memory owner.

**Risks**

Post-narration persistence can expand memory scope or accidentally make
rejected content durable.

**Mitigations**

Keep the post-narration commit under Memory ownership, accept only grounded
output, bind it to the validated envelope, preserve provider and grounding
provenance, and suppress narrative delivery if a required commit fails.

**GO / NO-GO impact**

Any database read or write inside LLM Integration is `NO-GO`.

### A-04: Citation Packages Are Immutable

**Decision**

Citation packages received from Response Composer and Memory Integration are
immutable. LLM Integration may not create, rename, alias, replace, enrich,
resolve, or synthesize citation IDs or comparable records.

**Reason**

The attempted adapter created fallback evidence IDs and zero-price comparable
wrappers. That moved citation authority into the narration layer and weakened
provenance.

**Alternatives considered**

1. Permit LLM-friendly citation aliases.
2. Permit fallback citation IDs when evidence is sparse.
3. Permit synthetic comparable wrappers for compatibility.
4. Allow the provider to return arbitrary citations.

**Risks**

Provider output may reference a missing, foreign, or unsupported citation.

**Mitigations**

Expose only allowlisted citation tokens, validate every returned reference
against the immutable package, and attach delivery citations
deterministically rather than trusting provider-generated citation objects.

**GO / NO-GO impact**

Citation mutation or fabrication is `NO-GO`.

### A-05: Grounding Is a Multi-Gate Deterministic Control

**Decision**

Grounding must occur at four points:

1. Before generation: validate tenant bindings, status, supported intent,
   citation membership, egress projection, and prompt budget.
2. After generation: validate the original unmodified provider output.
3. Before persistence: accept only grounded narration for any Memory-owned
   commit.
4. Before delivery: deliver only grounded narration and deterministic
   Composer-owned structured payloads.

**Reason**

Prompt instructions are not enforcement. The attempted architecture overwrote
authoritative fields before validation and did not reject unsupported free
text arithmetic or authority claims.

**Alternatives considered**

1. Trust prompt instructions.
2. Validate only structured fields.
3. Repair provider output before validation.
4. Deliver first and audit later.

**Risks**

Unsupported percentages, rankings, prices, forecasts, confidence claims, or
offers can be phrased in many ways.

**Mitigations**

Validate the original candidate output, reject unsupported claim categories,
use per-intent allowlists, keep deterministic values outside model ownership,
and fall back to the Composer payload when narration fails.

**GO / NO-GO impact**

Any mutation-before-validation or delivery-before-validation path is `NO-GO`.

### A-06: A Modern Narration Contract Is Required

**Decision**

Phase 5.5C.6 requires a modern narration contract derived from
`ComposedResponse` and `MemoryContext`. It must be intent-specific and
activation must be allowlisted by supported intent.

The narration contract must represent candidate narration and existing
citation references without granting the provider authority to restate or
replace deterministic values. Unsupported intents must bypass LLM narration
and use deterministic delivery.

**Reason**

The legacy schema primarily represents valuation and explainability. It
cannot ground Tool 3-8 outputs or property comparison safely.

**Alternatives considered**

1. Reuse the legacy response contract unchanged.
2. Use one generic free-text contract for all intents.
3. Activate all intents before intent-specific validation exists.

**Risks**

A superficially generic contract can conceal intent-specific authority drift.

**Mitigations**

Require explicit per-intent coverage, default unsupported intents to LLM-off,
and separate narration from Composer-owned structured delivery data.

**GO / NO-GO impact**

Legacy-contract reuse as the modern contract is `NO-GO`.

### A-07: The Legacy Broker LLM Runtime Must Be Isolated and Retired

**Decision**

The legacy broker LLM runtime must be isolated immediately and retired as an
activation path before modern Phase 5.5C.6 LLM activation. The transitional
non-LLM Broker Adapter may remain operational while the modern path is
governed.

**Reason**

The forensic audit found two competing LLM architectures. A legacy feature
flag can activate a path that bypasses the modern Composer and Memory chain.

**Alternatives considered**

1. Keep both LLM runtimes available.
2. Route modern orchestration through the legacy LLM runtime.
3. Activate the attempted detached modern package.
4. Remove the entire non-LLM broker surface immediately.

**Risks**

Legacy code or configuration can remain a hidden bypass even when disabled by
default.

**Mitigations**

Treat the legacy LLM path as non-canonical, prohibit its activation, require
configuration and dependency review before modern activation, and document
any transitional non-LLM broker behavior separately.

**GO / NO-GO impact**

Coexisting activatable LLM paths are `NO-GO`.

### A-08: Provider Integration Is Stateless and Minimized

**Decision**

The provider boundary must be provider-neutral, stateless, and governed by an
explicit egress policy. Provider-side threads, conversation memory, and
provider-managed continuity are prohibited.

The approved boundary must define consistent timeout, bounded retry, error,
structured-output capability, retention assumption, and redaction behavior
for each approved provider.

**Reason**

The forensic audit found external providers receiving broad scoped context
through a legacy-coupled abstraction with incomplete operational semantics.

**Alternatives considered**

1. Reuse the legacy provider abstraction without review.
2. Use provider-side conversation state.
3. Send the complete MemoryContext to simplify prompts.
4. Restrict the architecture to one vendor permanently.

**Risks**

Unnecessary provider egress can disclose tenant-scoped context. Provider
differences can create inconsistent failure behavior.

**Mitigations**

Use deterministic provider-safe projections, data minimization, redaction,
stateless requests, explicit retention assumptions, and uniform failure
semantics.

**GO / NO-GO impact**

Undefined egress or provider-side memory is `NO-GO`.

### A-09: Narration Failure Must Fail Closed Without Blocking Deterministic Delivery

**Decision**

LLM narration is optional. Scope failure, unsupported intent, prompt
overflow, provider failure, parse failure, grounding rejection, or required
post-narration commit failure must suppress LLM narration. Where the request
is otherwise authorized, delivery may fall back to the Composer-owned
structured response.

**Reason**

The platform already has an authoritative deterministic response channel.
LLM failure must not force an ungrounded response or erase a valid governed
result.

**Alternatives considered**

1. Deliver raw provider text on validation failure.
2. Retry indefinitely.
3. Treat LLM availability as required for all delivery.
4. Hide all deterministic results when narration fails.

**Risks**

Fallback behavior can become ambiguous to clients or operators.

**Mitigations**

Define explicit narration status, preserve the deterministic payload, emit
auditable failure metadata outside the LLM layer, and never downgrade tenant
authorization failures into disclosures.

**GO / NO-GO impact**

Any fail-open narrative delivery is `NO-GO`.

### A-10: Current Attempted Runtime Is Not the Canonical Runtime

**Decision**

The detached modern package and the live legacy LLM runtime are not approved
canonical paths. The canonical target path is the staged sequence defined in
`PHASE_5_5C_6B_CANONICAL_RUNTIME_PATH.md`.

**Reason**

The attempted package is detached from production delivery, crosses memory
and citation boundaries, accepts unbound context, and reuses legacy
grounding. The legacy runtime can independently bypass the modern chain.

**Alternatives considered**

1. Promote the attempted package after minor cleanup.
2. Declare the live legacy path canonical.
3. Leave runtime choice to configuration.

**Risks**

Implementation-first reuse can preserve hidden ownership drift.

**Mitigations**

Approve the runtime path first, then evaluate future implementation solely
against that path and the ownership matrix.

**GO / NO-GO impact**

Promotion of either observed LLM runtime shape is `NO-GO`.

## 6. Architectural Contradictions Found

| Contradiction | Resolution |
| --- | --- |
| The locked rule says Memory remembers, but the attempted LLM adapter persists generated text. | All post-generation persistence moves under Memory ownership after grounding. |
| The Composer preserves received citations, but the attempted adapter creates citation aliases and replacement comparable records. | Citation packages remain immutable through prompt, validation, persistence, and delivery. |
| The system has a deterministic modern chain, but the live broker LLM path can bypass it. | The legacy LLM activation path is isolated and retired before modern activation. |
| Prompt assembly is intended to consume governed context, but raw user text and unbound scope values arrive independently. | One scoped narration envelope becomes the only Prompt Assembly input. |
| Prompt instructions prohibit calculations, but validation does not enforce the prohibition. | Original provider output is checked deterministically before persistence or delivery. |
| The modern chain supports Tools 1-8 and comparison, but the reused legacy response contract does not. | A modern intent-specific narration contract is mandatory. |

## 7. Hidden Ownership Drift Prohibited by This Review

The following are architecture violations even if they appear convenient:

- LLM retries that silently change prompt content or deterministic values.
- Provider-specific continuity that creates memory outside Memory Integration.
- Prompt templates that perform calculations or select among Tool outputs.
- Grounding logic that repairs model claims before recording a rejection.
- Delivery code that trusts provider citations rather than deterministic
  citation packages.
- Logging or debug persistence that stores rejected provider text as accepted
  assistant memory.
- A generic compatibility mapper that drops Tool 3-8 evidence while allowing
  narration to continue.
- Feature flags that can reactivate the legacy LLM bypass path.
- Token-budget behavior that emits an oversized prompt when non-evictable
  inputs exceed the configured limit.

## 8. Minimum Required Architecture Decisions Before Implementation May Resume

1. Accept the narration-only responsibility boundary.
2. Accept the single fail-closed scoped narration envelope as the only Prompt
   Assembly input.
3. Accept the exact Prompt Assembly allowlist, provider egress allowlist, and
   forbidden-data list.
4. Accept Memory Integration as the exclusive owner of pre-LLM memory work
   and any post-grounding narration commit.
5. Accept immutable Composer and Memory citation packages.
6. Accept deterministic grounding before generation, after generation, before
   persistence, and before delivery.
7. Accept a modern intent-specific narration contract with per-intent
   activation allowlists.
8. Accept immediate isolation and pre-activation retirement of the legacy
   broker LLM runtime.
9. Accept a stateless provider-neutral boundary with minimization, redaction,
   retention, timeout, retry, and error rules.
10. Accept deterministic fallback delivery and fail-closed narration
    semantics.
11. Accept the canonical runtime path defined by this review.
12. Decide the governed disposition of the unauthorized Phase 5.5C.6
    artifacts before any implementation work continues.

## 9. Final Verdict

```text
ARCHITECTURE_DECISION: CONDITIONAL_GO
```

The LLM architecture may exist only as an optional, stateless,
narration-only stage after the governed deterministic chain. The existing
attempted implementation remains `NO-GO`. Implementation may resume only
after the minimum architecture decisions above and the requirements in
`PHASE_5_5C_6B_APPROVAL_REQUIREMENTS.md` are explicitly approved.
