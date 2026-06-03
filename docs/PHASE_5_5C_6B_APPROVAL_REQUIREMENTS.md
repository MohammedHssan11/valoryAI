# ValorAI Phase 5.5C.6B Approval Requirements

Decision date: 2026-06-01  
Decision scope: Governance gates for Phase 5.5C.6 implementation resumption,
runtime activation, and production promotion  
Implementation status: Architecture decision only  

## 1. Gate Structure

Phase 5.5C.6 has three separate gates:

1. **Gate A: Architecture approval before implementation resumes.**
2. **Gate B: Runtime activation approval after implementation evidence.**
3. **Gate C: Production promotion approval after platform blockers are
   resolved.**

Passing one gate does not imply passage of the next.

## 2. Current Gate Status

| Gate | Status | Reason |
| --- | --- | --- |
| Gate A: Architecture approval | `CONDITIONAL_GO` | This review defines an approvable narration-only architecture, but its minimum decisions still require explicit acceptance. |
| Gate B: Runtime activation | `NO-GO` | No compliant implementation or validation evidence exists for the newly defined canonical path. |
| Gate C: Production promotion | `NO-GO` | The master state retains unresolved frontend JWT/context, direct valuation authentication, managed-secret, RBAC, and regression-test blockers. |

The unauthorized Phase 5.5C.6 artifacts do not satisfy any gate and must not
be treated as implementation evidence.

## 3. Gate A: Minimum Architecture Decisions Before Implementation May Resume

Implementation may resume only after explicit approval of every item below.

| ID | Required architecture decision | Approval evidence |
| --- | --- | --- |
| A-01 | LLM Integration is narration-only. | Accepted responsibility statement matching `PHASE_5_5C_6B_BOUNDARY_OWNERSHIP_MATRIX.md`. |
| A-02 | Planner remains the only Tool-decision owner. | Accepted prohibition on LLM Tool selection, follow-up execution, and orchestration. |
| A-03 | Executor remains the only Tool-execution owner. | Accepted prohibition on provider, prompt, grounding, or delivery Tool calls. |
| A-04 | Composer remains the only approved arithmetic and deterministic response-composition owner. | Accepted prohibition on LLM pricing, arithmetic, ranking, confidence calculation, comparison calculation, forecasting, and offer creation. |
| A-05 | Memory Integration remains the only memory retrieval and accepted conversation-persistence owner. | Accepted pre-generation and optional post-generation persistence decision. |
| A-06 | Prompt Assembly accepts one fail-closed scoped narration envelope only. | Accepted envelope boundary, field-governance process, and hidden-side-input prohibition. |
| A-07 | Current-turn content is bounded, treated as untrusted data, and represented inside the scoped envelope. | Accepted prompt-injection posture and hard size limit policy. |
| A-08 | Composer and Memory citation packages remain immutable. | Accepted prohibition on aliases, fallback evidence IDs, replacement comparable records, and provider-owned citations. |
| A-09 | Grounding runs before generation, after generation on original output, before persistence, and before delivery. | Accepted grounding timeline and rejection semantics. |
| A-10 | A modern intent-specific narration contract is required. | Accepted per-intent activation policy and default-off behavior. |
| A-11 | Provider integration is stateless and provider-neutral. | Accepted prohibition on provider-side conversation memory and accepted operational policy categories. |
| A-12 | Provider egress is minimized by deterministic allowlist and redaction rules. | Accepted provider-safe projection categories and denied-by-default tenant identifiers. |
| A-13 | Narration failure fails closed while authorized deterministic Composer delivery remains available. | Accepted fallback and denial semantics. |
| A-14 | The legacy broker LLM runtime is isolated immediately and retired as an activation path before modern activation. | Accepted legacy disposition decision. |
| A-15 | The canonical runtime path is the modern narration-only sequence in `PHASE_5_5C_6B_CANONICAL_RUNTIME_PATH.md`. | Accepted sole-path decision. |
| A-16 | The unauthorized Phase 5.5C.6 artifacts receive an explicit governed disposition before implementation work continues. | Recorded retain-for-reference, replace, quarantine, or retire decision without implicit promotion. |

### Gate A Required Sign-Off Roles

Gate A requires explicit sign-off from:

1. AI Systems Architecture.
2. Software Governance.
3. Multi-Tenant Security Architecture.
4. LLM Systems Review.
5. Product or platform owner accountable for accepted narration behavior.

## 4. Gate B: Runtime Activation Requirements

After Gate A approval and subsequent implementation work, runtime activation
remains `NO-GO` until evidence proves all requirements below.

### B-01: Canonical Dependency Direction

Evidence must prove:

1. The modern path begins after Composer and Memory Integration.
2. Prompt Assembly receives only one validated scoped narration envelope.
3. No LLM-stage component imports or calls database, ORM, Tool Layer, Router,
   CMT, ML, memory retrieval, memory persistence, API delivery, SSE, or
   WebSocket ownership.
4. No route, feature flag, or configuration can activate a competing legacy
   LLM path.

### B-02: Tenant-Binding and Denial Cases

Evidence must prove fail-closed behavior for:

1. Foreign user and workspace combinations.
2. Foreign or deleted scenario.
3. Foreign or deleted broker session.
4. Mismatched composed response and memory context.
5. Mismatched citation package.
6. `FAILED` memory context.
7. `ACCESS_DENIED` memory context.
8. Missing required scope.

No failed binding case may contact the provider or disclose scoped content.

### B-03: Prompt Assembly and Budget Cases

Evidence must prove:

1. Raw executor payloads do not enter Prompt Assembly.
2. Raw Tool payloads do not enter Prompt Assembly.
3. ORM entities and database rows do not enter Prompt Assembly.
4. Full transcripts do not enter Prompt Assembly.
5. Current-turn content is bounded inside the approved envelope.
6. Non-evictable content that exceeds the token budget fails closed.
7. Optional context eviction is deterministic and does not remove required
   grounding data silently.
8. Unsupported intents bypass LLM narration.

### B-04: Provider Egress Cases

Evidence must prove:

1. Provider requests contain only approved minimized fields.
2. JWTs, bearer tokens, secrets, connection strings, and internal provider
   credentials never appear in prompt content.
3. Tenant identifiers are denied by default and absent unless separately
   approved.
4. Provider-side thread IDs and conversation memory are absent.
5. Timeout, bounded retry, error, retention assumption, and
   structured-output behavior are documented consistently for every enabled
   provider.

### B-05: Citation Cases

Evidence must prove:

1. Composer and Memory citation packages pass through unchanged.
2. No aliases, fallback evidence IDs, or synthetic comparable wrappers are
   created.
3. Missing citation references are rejected.
4. Foreign citation references are rejected.
5. Unsupported citation references are rejected.
6. Sparse evidence remains sparse evidence.

### B-06: Grounding and Governance Cases

Evidence must prove rejection of original provider output containing:

1. Unsupported authoritative values.
2. Unsupported prices.
3. Unsupported percentages or deltas.
4. New comparison arithmetic.
5. Unsupported ranking.
6. Unsupported confidence claims.
7. Unsupported negotiation positions or offer values.
8. Forecasts or future-price predictions.
9. ROI, IRR, CAGR, yield, appreciation, or return claims.
10. Synthetic market trends.
11. Claims that contradict sparse or insufficient evidence status.
12. Unsupported intent-specific claims.

Evidence must also prove that original provider output is checked before any
value attachment, normalization, or mutation.

### B-07: Persistence Cases

Evidence must prove:

1. Existing pre-generation summary persistence remains bounded, idempotent,
   and Memory-owned.
2. LLM Integration has no database or memory service access.
3. Prompt Assembly has no database or memory service access.
4. Provider adapters have no database or memory service access.
5. Grounding has no accepted-memory write access.
6. Delivery has no accepted-memory write access.
7. If post-generation commit exists, it is Memory-owned, conversation-bound,
   and accepts grounded narration only.
8. Rejected provider text is never persisted as accepted assistant memory.
9. Required commit failure suppresses narrative delivery and permits
   authorized deterministic fallback only.

### B-08: Failure and Fallback Cases

Evidence must prove:

1. Scope rejection contacts no provider.
2. Prompt overflow contacts no provider.
3. Provider timeout suppresses narrative delivery.
4. Provider error suppresses narrative delivery.
5. Parse failure suppresses narrative delivery.
6. Grounding failure suppresses narrative delivery.
7. Required narration-commit failure suppresses narrative delivery.
8. Authorized deterministic Composer payload remains available as fallback.
9. Authorization failures never become deterministic scoped-data fallbacks.

### B-09: Per-Intent Activation Cases

Each enabled intent requires separate evidence for:

1. Allowed narration fields.
2. Prohibited claim categories.
3. Citation behavior.
4. Sparse or insufficient evidence behavior.
5. Deterministic fallback behavior.

No generic catch-all LLM narration mode may activate an unapproved intent.

### B-10: Validation Harness Integrity

Validation evidence must prove:

1. Real approved upstream components are exercised.
2. Real tenant boundaries are exercised.
3. Real persistence behavior is exercised where persistence is in scope.
4. SQLite fallback cannot masquerade as the required PostgreSQL/PostGIS
   validation environment.
5. Static dependency allowlists are checked.
6. Adversarial grounding cases are checked.
7. Provider egress assertions are checked.
8. Competing-runtime activation assertions are checked.
9. Failures cannot be converted into false `llm_narrator_only` PASS results.

## 5. Gate C: Production Promotion Requirements

Phase 5.5C.6 activation does not override the broader platform production
blockers recorded in `PROJECT_MASTER_STATE_V2.md`.

Production promotion remains `NO-GO` until at least:

1. Frontend JWT attachment is implemented and validated.
2. Frontend workspace, scenario, and recovered-session context integration is
   implemented and validated.
3. Direct valuation endpoint authentication policy is decided and enforced.
4. Managed secret storage and rotation are implemented.
5. Organization membership and RBAC are implemented.
6. Backend regression test drift is resolved.
7. External telemetry and shared rate-limiting posture are approved for the
   intended deployment.
8. LLM provider retention, redaction, and operational controls are approved
   for the intended environment.

## 6. Required Governance Records

Before implementation resumes, record:

1. The accepted canonical runtime path.
2. The accepted boundary ownership matrix.
3. The accepted Prompt Assembly input allowlist.
4. The accepted Prompt Assembly forbidden-data list.
5. The accepted provider egress allowlist and redaction posture.
6. The accepted immutable citation policy.
7. The accepted grounding timeline and prohibited-claim categories.
8. The accepted per-intent narration activation policy.
9. The accepted Memory-owned post-narration persistence decision.
10. The accepted deterministic fallback semantics.
11. The accepted legacy broker LLM retirement decision.
12. The governed disposition of the unauthorized Phase 5.5C.6 artifacts.

## 7. Formal Approval Decisions

### P-01: Implementation Resumption Is Conditional

**Decision**

Implementation may resume only after every Gate A decision is explicitly
accepted.

**Reason**

The forensic audit demonstrated that implementation-first work caused
ownership drift and a false-confidence validator.

**Alternatives considered**

1. Resume implementation while architecture decisions remain open.
2. Repair the attempted package incrementally.
3. Treat existing tests as implicit approval.

**Risks**

Partial approval can recreate the same architecture through incremental
exceptions.

**Mitigations**

Require a complete Gate A record before implementation continuation.

**GO / NO-GO impact**

Until Gate A is accepted, implementation continuation is `NO-GO`.

### P-02: Runtime Activation Requires Adversarial Evidence

**Decision**

Runtime activation requires Gate B evidence, including adversarial tenant,
citation, grounding, prompt-budget, egress, persistence, and fallback cases.

**Reason**

Happy-path validators cannot prove a multi-tenant narration boundary.

**Alternatives considered**

1. Activate after static review only.
2. Activate after provider smoke tests only.
3. Activate with monitoring and fix violations later.

**Risks**

Validation can still miss unanticipated provider language.

**Mitigations**

Use per-intent default-off activation, deterministic fallback, and bounded
rollout only after Gate B approval.

**GO / NO-GO impact**

Without Gate B evidence, runtime activation is `NO-GO`.

### P-03: Production Promotion Is a Separate Decision

**Decision**

Production promotion remains separate from Phase 5.5C.6 architecture and
runtime activation approval.

**Reason**

The master state identifies unresolved platform blockers unrelated to the LLM
boundary.

**Alternatives considered**

1. Let Phase 5.5C.6 approval imply production readiness.
2. Defer broader security blockers until after LLM launch.

**Risks**

An architecture milestone can be mistaken for a security or deployment
approval.

**Mitigations**

Maintain Gate C as an independent `NO-GO` until production requirements are
closed.

**GO / NO-GO impact**

Phase 5.5C.6 `CONDITIONAL_GO` does not change production promotion `NO-GO`.

## 8. Final Approval Verdict

```text
ARCHITECTURE_DECISION: CONDITIONAL_GO
IMPLEMENTATION_RESUMPTION: NO_GO UNTIL GATE A IS EXPLICITLY ACCEPTED
RUNTIME_ACTIVATION: NO_GO UNTIL GATE B EVIDENCE PASSES
PRODUCTION_PROMOTION: NO_GO UNTIL GATE C IS CLOSED
```

## 9. Minimum Required Architecture Decisions Before Implementation May Resume

1. Approve narration-only LLM ownership.
2. Approve the sole canonical modern runtime path.
3. Approve the single scoped narration envelope.
4. Approve Prompt Assembly allowed and forbidden data.
5. Approve provider egress minimization and redaction.
6. Approve stateless provider behavior.
7. Approve immutable Composer and Memory citations.
8. Approve deterministic grounding at all required checkpoints.
9. Approve the modern per-intent narration contract policy.
10. Approve Memory-owned pre-generation and optional post-generation
    persistence.
11. Approve deterministic fallback delivery.
12. Approve isolation and retirement of the legacy broker LLM activation
    path.
13. Approve a governed disposition for the unauthorized Phase 5.5C.6
    artifacts.
