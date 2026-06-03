# ValorAI Phase 5.5C.6B Runtime Decision

Decision date: 2026-06-01  
Decision scope: Canonical LLM runtime selection  
Implementation status: Architecture decision only  

## 1. Runtime Finding

No approved canonical LLM runtime currently exists.

The forensic audit identified two incompatible runtime shapes:

1. A detached modern Copilot Orchestrator LLM package that maps modern
   Composer output into legacy broker contracts, calls a provider, mutates
   authoritative values before validation, queries messages, and persists
   generated assistant text.
2. A live legacy broker LLM runtime that can be activated independently of
   the modern deterministic chain.

Neither runtime shape is approved.

## 2. Runtime Decision

The only approvable Phase 5.5C.6 runtime is a modern narration-only path after
the existing deterministic chain:

```text
Authenticated and tenant-scoped request
  -> Intent Engine
  -> Tool Planner
  -> Tool Executor
  -> Response Composer
  -> Memory Integration pre-generation work
  -> Narration Admission Gate
  -> Prompt Assembly
  -> Stateless LLM Provider
  -> Deterministic Grounding and Governance
  -> Memory-owned Post-Narration Commit, when approved
  -> Delivery
```

The provider response is never authoritative. The delivery surface remains
authoritative only because it carries deterministic Composer-owned payloads
and, when accepted, separately grounded narration.

## 3. Runtime Status Matrix

| Runtime shape | Status | Reason |
| --- | --- | --- |
| Existing deterministic chain through Memory Integration | Approved baseline | This is the locked Phase 5.5C.5 architecture. |
| Detached modern LLM package observed by forensic audit | Rejected | It crosses persistence, citation, tenant-binding, and grounding boundaries. |
| Live legacy broker LLM generation path | Rejected as activation path | It can bypass the modern Composer and Memory chain. |
| Transitional non-LLM Broker Adapter | May remain isolated | It is outside this LLM activation decision and currently uses Tool 1 and Tool 2. |
| Modern narration-only path defined by this review | Conditionally approved architecture | It preserves deterministic ownership if all approval requirements are accepted. |

## 4. Formal Runtime Decisions

### R-01: One Canonical Modern Path

**Decision**

Phase 5.5C.6 must have exactly one canonical LLM runtime path. It must begin
only after Response Composer and Memory Integration complete their approved
deterministic responsibilities.

**Reason**

The repository currently contains competing activation paths. Runtime choice
cannot be left to incidental imports, feature flags, or provider
configuration.

**Alternatives considered**

1. Keep the live legacy and modern LLM paths in parallel.
2. Select the legacy path as canonical.
3. Allow each API route to select its own LLM path.
4. Leave the detached modern package as an optional helper.

**Risks**

Parallel paths create policy divergence, inconsistent grounding, and
different persistence behavior.

**Mitigations**

Document one runtime sequence, require one activation control surface, and
reject any dependency path that bypasses Composer, Memory Integration, or the
Narration Admission Gate.

**GO / NO-GO impact**

Multiple activatable LLM paths are `NO-GO`.

### R-02: Legacy Broker LLM Runtime Isolation and Retirement

**Decision**

The legacy broker LLM runtime must be isolated immediately and retired as an
LLM activation path before the modern narration path can be activated.

The transitional non-LLM Broker Adapter may remain available while migration
decisions are governed separately.

**Reason**

The legacy path can be enabled independently and bypasses the modern
deterministic chain. Disabled-by-default is not an architectural boundary.

**Alternatives considered**

1. Retain the legacy LLM path as a fallback.
2. Use the legacy LLM path for valuation and the modern path for Tools 3-8.
3. Remove all broker behavior immediately.

**Risks**

Configuration drift can reactivate a bypass. Shared legacy provider
configuration can also blur which runtime is active.

**Mitigations**

Prohibit legacy LLM activation, separate any transitional non-LLM behavior,
and require an activation audit that proves the legacy path cannot receive
production LLM traffic.

**GO / NO-GO impact**

Modern activation while the legacy LLM path remains activatable is `NO-GO`.

### R-03: Narration Admission Gate Before Prompt Assembly

**Decision**

A deterministic Narration Admission Gate must sit between Memory Integration
and Prompt Assembly.

It must validate the complete binding of user, workspace, optional scenario,
optional broker session, Composer response, Memory context, status, intent,
citations, egress projection, and token-budget eligibility before provider
contact.

**Reason**

The forensic audit found independently supplied identifiers and contexts,
unused scenario and broker-session values, and provider egress before a
fail-closed binding decision.

**Alternatives considered**

1. Validate after provider invocation.
2. Trust upstream callers.
3. Let Prompt Assembly perform ad hoc checks.
4. Let the provider infer missing context.

**Risks**

Mismatched context can disclose another tenant's memory before downstream
validation runs.

**Mitigations**

Bind once, reject before prompt assembly, and expose only a deterministic
provider-safe projection of the validated envelope.

**GO / NO-GO impact**

Any provider call before fail-closed scope validation is `NO-GO`.

### R-04: Original Provider Output Is an Untrusted Candidate

**Decision**

The provider response must remain unmodified until deterministic grounding
and governance checks complete. Deterministic delivery values may be attached
separately after approval but may not overwrite candidate output before drift
detection.

**Reason**

The attempted runtime overwrote authoritative values before validation,
masking model disagreement instead of rejecting it.

**Alternatives considered**

1. Normalize or repair model values before validation.
2. Validate only citations.
3. Trust structured output schema compliance.
4. Deliver prose without governance checks.

**Risks**

Free text can contain unsupported authority claims even when structured
fields look valid.

**Mitigations**

Validate original structured content and prose, reject prohibited claims, and
keep deterministic payloads as a separate authoritative delivery channel.

**GO / NO-GO impact**

Mutation-before-validation is `NO-GO`.

### R-05: Memory-Owned Persistence on Both Sides of Narration

**Decision**

Existing pre-generation persistence remains under Memory Integration.
Optional post-generation persistence also belongs exclusively to Memory
Integration and runs only after grounding approval.

No Prompt Assembly, provider adapter, LLM integration adapter, grounding
validator, or delivery component may write memory.

**Reason**

The locked rule is explicit: Memory remembers. The attempted adapter violated
that rule by selecting messages and writing assistant content directly.

**Alternatives considered**

1. Persist inside the LLM adapter.
2. Persist inside delivery.
3. Persist rejected provider text as assistant memory.
4. Avoid post-generation persistence entirely.

**Risks**

Post-generation commits can become a second uncontrolled memory pipeline.

**Mitigations**

Require a Memory-owned commit bound to the validated envelope, accept only
grounded narration, keep rejection telemetry separate from accepted memory,
and suppress narrative delivery if a required commit fails.

**GO / NO-GO impact**

Persistence outside Memory ownership is `NO-GO`.

### R-06: Deterministic Fallback Delivery

**Decision**

LLM narration is optional. When narration is unavailable or rejected, the
runtime may deliver the Composer-owned frontend-safe response without model
text, provided authorization has succeeded.

Authorization or tenant-binding failure must return no scoped disclosure.

**Reason**

The platform already has a deterministic structured response. LLM failure
must not force unsafe narrative delivery or suppress valid governed data.

**Alternatives considered**

1. Make narration mandatory.
2. Deliver unvalidated model text as a degraded fallback.
3. Retry until a provider succeeds.
4. Return scoped data when tenant binding is uncertain.

**Risks**

Clients may treat narration absence as a platform error unless status is
clear.

**Mitigations**

Expose explicit narration status, preserve Composer status semantics, and
keep tenant denial separate from LLM degradation.

**GO / NO-GO impact**

Fail-open model delivery is `NO-GO`. Deterministic non-LLM fallback is
required for `CONDITIONAL_GO`.

### R-07: Provider Boundary Must Be Modern and Provider-Neutral

**Decision**

The canonical runtime requires a modern provider boundary with consistent
stateless generation, timeout, bounded retry, error, structured-output,
redaction, retention, and capability rules.

Legacy broker namespace ownership must not define the modern architecture.

**Reason**

Supporting more than one vendor does not by itself create a governed provider
architecture. The audited abstraction remains legacy-coupled and
operationally incomplete.

**Alternatives considered**

1. Reuse the existing provider abstraction unchanged.
2. Hard-code one provider.
3. Allow provider-specific behavior to leak into orchestration.
4. Use provider-side conversation threads.

**Risks**

Provider differences can change error semantics, retention posture, and
structured-output reliability.

**Mitigations**

Approve provider capabilities explicitly, enforce a shared contract, minimize
egress, and keep continuity in ValorAI Memory Integration only.

**GO / NO-GO impact**

Undefined provider behavior or provider-side memory is `NO-GO`.

## 5. Runtime Activation Rules

The modern narration path must remain inactive until all of the following are
true:

1. The canonical path is accepted as the sole Phase 5.5C.6 path.
2. The legacy broker LLM path is proven non-activatable.
3. The scoped narration envelope and provider-safe projection are approved.
4. The modern narration contract is approved for each enabled intent.
5. Immutable citation handling is approved.
6. Original-output grounding and governance are approved.
7. Memory-owned post-narration persistence behavior is approved or explicitly
   deferred.
8. Deterministic fallback semantics are approved.
9. Validation evidence satisfies
   `PHASE_5_5C_6B_APPROVAL_REQUIREMENTS.md`.

## 6. Final Runtime Verdict

```text
RUNTIME_DECISION: CONDITIONAL_GO FOR THE DEFINED TARGET PATH
CURRENT_LLM_RUNTIME_STATUS: NO_GO
LEGACY_LLM_ACTIVATION_PATH: ISOLATE AND RETIRE
CANONICAL_RUNTIME_PATH: MODERN NARRATION-ONLY PATH
```
