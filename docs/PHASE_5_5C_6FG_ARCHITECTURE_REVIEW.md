# ValorAI Phase 5.5C.6F + 5.5C.6G Architecture Review

Review date: 2026-06-02  
Review scope: Narration Admission Gate Architecture and Provider Adapter
Architecture  
Review mode: Architecture only  
Implementation status: Prohibited  

## 1. Authoritative Sources

This review is based only on the following authoritative sources, each read
completely:

1. `PROJECT_MASTER_STATE_V2.md`
2. `NARRATION_CONTRACT_ARCHITECTURE.md`
3. `NARRATION_ACTIVATION_POLICY.md`
4. `NARRATION_PROHIBITED_CLAIMS_MATRIX.md`
5. `VALUATION_NARRATION_CONTRACT.md`
6. `EXPLAINABILITY_NARRATION_CONTRACT.md`
7. `COMPARABLES_NARRATION_CONTRACT.md`
8. `FAIRNESS_NARRATION_CONTRACT.md`
9. `WHAT_IF_NARRATION_CONTRACT.md`
10. `NEGOTIATION_NARRATION_CONTRACT.md`
11. `INVESTMENT_NARRATION_CONTRACT.md`
12. `MARKET_INSIGHT_NARRATION_CONTRACT.md`
13. `PROPERTY_COMPARISON_NARRATION_CONTRACT.md`
14. `PHASE_5_5C_6B_FORMAL_ARCHITECTURE_REVIEW.md`
15. `PHASE_5_5C_6B_RUNTIME_DECISION.md`
16. `PHASE_5_5C_6B_BOUNDARY_OWNERSHIP_MATRIX.md`
17. `PHASE_5_5C_6B_CANONICAL_RUNTIME_PATH.md`
18. `PHASE_5_5C_6B_APPROVAL_REQUIREMENTS.md`

The sources provide sufficient information for this architecture review. No
implementation assumption is required.

## 2. Locked Rule

```text
Planner decides.
Executor executes.
Composer computes.
Memory remembers.
LLM narrates.
```

The Admission Gate and Provider Adapter exist only to preserve this rule. They
must not become hidden decision, calculation, memory, evidence, persistence,
or delivery layers.

## 3. Executive Verdict

```text
6F_DECISION: CONDITIONAL_GO
6G_DECISION: CONDITIONAL_GO
COMBINED_DECISION: CONDITIONAL_GO
IMPLEMENTATION: NO_GO
RUNTIME_ACTIVATION: NO_GO
PROVIDER_INTEGRATION: NO_GO
PRODUCTION_PROMOTION: NO_GO
```

The target architecture is approvable only if the Admission Gate is a
deterministic pre-provider policy firewall and the Provider Adapter is a
stateless, minimized, untrusted transport boundary.

The existing attempted LLM runtimes remain `NO_GO`. This review does not
approve Prompt Assembly architecture, code, APIs, schemas, providers, tests,
validators, runtime wiring, feature flags, or production traffic.

# Section A: Admission Gate Architecture

## A.1 Purpose

The Narration Admission Gate is the mandatory deterministic boundary between
Memory Integration and future Prompt Assembly.

Its purpose is to answer one narrow question:

```text
May this already-governed request proceed toward a provider-safe narration
attempt under the approved intent contract and egress policy?
```

The gate is not an LLM component. It does not generate narration. It prevents
provider contact unless the request is authorized, internally consistent,
eligible for narration, minimized for egress, and capable of deterministic
post-generation grounding.

## A.2 Runtime Placement

The approved placement is:

```text
Authenticated scoped request
  -> Intent Engine
  -> Tool Planner
  -> Tool Executor
  -> Response Composer
  -> Memory Integration Pre-Generation
  -> Narration Admission Gate
  -> Future Prompt Assembly
  -> Provider Adapter
  -> Future Candidate Parser
  -> Grounding Layer
  -> Memory Integration Post-Generation, when separately approved
  -> Delivery
```

The Admission Gate must complete before Prompt Assembly and before any
provider invocation. It must not be bypassable by routes, feature flags,
legacy broker runtime configuration, retries, failover, or direct provider
calls.

## A.3 Ownership

The Admission Gate owns:

1. Deterministic narration-admission policy evaluation.
2. Cross-artifact binding checks across authenticated scope, Composer output,
   Memory context, optional scenario, optional broker session, citations,
   intent contract, activation policy, and egress policy.
3. Classification into one explicit admission state.
4. Deterministic construction and validation of a provider-safe projection.
5. Pre-assembly prompt-budget eligibility checks.
6. Construction of the internal grounding-eligibility manifest needed by the
   downstream Grounding Layer.
7. Bounded redacted admission audit metadata.

The Admission Gate does not own:

1. Authentication or authorization policy execution.
2. JWT parsing, signature validation, token refresh, or identity provisioning.
3. Database, ORM, cache, or persistence access.
4. Intent classification or clarification logic.
5. Tool selection, Tool execution, or Tool orchestration.
6. Arithmetic, valuation, comparison, ranking, confidence computation,
   forecasting, offers, strategies, or evidence generation.
7. Memory retrieval, memory compression, or memory writes.
8. Prompt construction or prompt text.
9. Provider selection, provider invocation, retry, or failover.
10. Candidate parsing, output repair, grounding approval, delivery, SSE, or
    transport.

## A.4 Inputs

The Admission Gate may read only already-governed internal inputs:

| Input | Source owner | Admission use |
| --- | --- | --- |
| Internal authenticated-scope proof | Authentication and tenant-scope boundary | Verify that authentication and authorization were completed for the current request. |
| Bounded current-turn content | Authenticated request boundary | Bind the user turn as untrusted data and validate its size eligibility. |
| Intent result and activation marker | Intent Engine and approved activation policy | Confirm single-intent narration eligibility and approved contract mapping. |
| Composed response | Response Composer | Verify deterministic status, intent compatibility, bounded compressed context, and citation package binding. |
| Memory context | Memory Integration | Verify status, scope binding, bounded context, and approved provider-safe summary classes. |
| Optional scenario binding proof | Approved upstream scope owner | Verify active same-tenant and same-workspace scenario binding when present or required. |
| Optional broker-session binding proof | Approved upstream scope owner | Verify active same-tenant, same-workspace, and same-scenario session binding when present or required. |
| Immutable citation package and binding metadata | Response Composer and Memory Integration | Verify identity, provenance, scope, and immutability. |
| Intent-specific narration contract identifier and approved version | Narration-governance registry | Verify contract availability and default-off activation status. |
| Provider-safe projection policy identifier and approved version | Egress-governance policy | Apply minimized allowlist and denylist behavior. |
| Pre-assembly budget policy identifier and approved version | Future Prompt Assembly governance | Verify envelope eligibility before prompt construction. |
| Grounding-policy identifier and approved version | Grounding governance | Verify that downstream original-output grounding can deterministically evaluate the permitted narration surface. |

The Admission Gate must never receive or retrieve:

1. Raw JWTs, bearer tokens, signing secrets, API keys, or connection strings.
2. `ExecutionPlan`.
3. Raw `ExecutionResult`.
4. Raw Tool 1-8 payloads.
5. ORM entities, database rows, direct database results, unrestricted logs,
   or full chat history.
6. Foreign-tenant, deleted-scope, unbound, or unrestricted context.
7. Provider credentials.
8. Prompt text or provider response content.

## A.5 Outputs

The Admission Gate emits exactly one admission decision. Only
`ADMIT_NARRATION` may proceed toward Prompt Assembly.

| Admission state | Meaning | Provider invocation |
| --- | --- | --- |
| `ADMIT_NARRATION` | Every required security, integrity, contract, minimization, budget-preflight, and grounding-eligibility check passed. | Permitted to proceed to future Prompt Assembly only. |
| `DETERMINISTIC_ONLY` | The request is authorized, but LLM narration is not enabled, not contractually supported, or not useful for this request. | Blocked. |
| `REJECT_NARRATION` | The request is authorized, but narration-specific integrity, minimization, budget, Composer, Memory, citation, contract, or grounding-eligibility validation failed. | Blocked. |
| `ACCESS_DENIED` | Authentication, authorization, tenant isolation, workspace, scenario, session, or cross-scope binding failed or cannot be trusted. | Blocked with no scoped disclosure. |

For `ADMIT_NARRATION`, the gate emits two logically separate internal
artifacts:

1. A validated scoped narration envelope for future Prompt Assembly and
   downstream grounding.
2. A minimized provider-safe projection that is the maximum content eligible
   for future external egress.

The internal envelope may carry binding metadata required for validation.
That internal metadata must not be copied into the external provider request
unless the provider-egress policy explicitly allows the individual field.

## A.6 Deterministic Behavior

The Admission Gate must be deterministic:

1. The same governed inputs and the same approved policy versions must produce
   the same admission state.
2. The same governed inputs and policy versions must produce the same
   provider-safe projection.
3. The gate may not call a model, provider, database, Tool, external service,
   or hidden retrieval system.
4. The gate may not silently repair, truncate, infer, or substitute required
   content.
5. Optional-field omission must follow a versioned deterministic rule.
6. Any required-field overflow, mismatch, or ambiguity fails closed.
7. Admission audit metadata must be bounded and redacted.

## A.7 Required Validations

### A.7.1 Authentication Validation

The gate must verify an internal authenticated-scope proof created by the
existing authentication boundary.

Required checks:

1. Authentication was completed for the current request.
2. The proof is bound to the current request lifecycle.
3. The proof is active and not stale under the approved policy.
4. No raw bearer token or JWT claim set enters the gate envelope or provider
   projection.

The gate must not parse or revalidate JWTs itself. Duplicating authentication
logic would create ownership drift.

### A.7.2 Tenant Validation

Required checks:

1. One tenant-scoped subject is bound consistently across all internal
   artifacts.
2. No foreign-tenant artifact is present.
3. No ambiguous or missing tenant binding is accepted.
4. Tenant identifiers remain internal and are absent from provider egress.

Any foreign, ambiguous, or mismatched tenant condition returns
`ACCESS_DENIED`.

### A.7.3 Workspace Validation

Required checks:

1. The workspace is active, authorized, and bound to the authenticated
   subject.
2. Composer and Memory artifacts belong to the same workspace.
3. Optional scenario and optional broker session, when present, belong to the
   same workspace.
4. No cross-workspace merge is permitted.

Any foreign, deleted, ambiguous, or mismatched workspace condition returns
`ACCESS_DENIED`.

### A.7.4 Scenario Validation

Required checks:

1. If a scenario is present or required by the intent, it is active and bound
   to the same subject and workspace.
2. Composer output and Memory context use compatible scenario scope.
3. What-if, Negotiation, and Investment narration cannot silently switch
   scenario lineage.
4. Scenario identifiers remain internal and are absent from provider egress.

Any foreign, deleted, ambiguous, or mismatched scenario condition returns
`ACCESS_DENIED`.

### A.7.5 Broker Session Validation

Required checks:

1. If a broker session is present or required, it is active and bound to the
   same subject and workspace.
2. If scenario-bound, its scenario matches the current scope.
3. The gate does not select the latest session or infer a session.
4. Session identifiers remain internal and are absent from provider egress.

Any foreign, deleted, ambiguous, or mismatched broker-session condition
returns `ACCESS_DENIED`.

### A.7.6 Intent Activation Validation

Required checks:

1. The intent is a single approved evidence-bearing domain intent.
2. The intent maps to exactly one approved narration contract version.
3. The intent is explicitly enabled by a default-off activation policy.
4. The contract and activation policy versions are known and internally
   consistent.

The following return `DETERMINISTIC_ONLY`:

1. `GENERAL_QUESTION`.
2. Clarification-required results.
3. Unsupported intents.
4. Generic catch-all flows.
5. Multi-intent flows without a separately approved combined contract.
6. Eligible intents that remain default-off or administratively disabled.

### A.7.7 Citation Validation

Required checks:

1. Citation packages come only from Composer and Memory Integration.
2. Package identity and binding metadata are intact.
3. Every exposed token is exact, immutable, and scoped.
4. No aliases, fallback evidence IDs, placeholder comparables, synthetic
   citations, or replacement records exist.
5. Property-comparison citations remain bound to the correct property.
6. Citation tokens are the only opaque evidence identifiers eligible for
   provider egress.

Failure classification:

1. A foreign-tenant or cross-workspace citation returns `ACCESS_DENIED`.
2. A malformed, missing, fabricated, aliased, or unsupported citation package
   within an otherwise authorized request returns `REJECT_NARRATION`.

### A.7.8 Memory Validation

Required checks:

1. Memory context comes only from Memory Integration.
2. Its subject, workspace, optional scenario, optional broker session,
   composed response, and citations bind to the current request.
3. Its bounded-summary limits and provider-safe summary classes are approved.
4. Its status permits narration admission.
5. It contains no unrestricted transcript, raw database row, or foreign
   artifact.

Failure classification:

1. Memory `ACCESS_DENIED`, foreign scope, deleted scope, or cross-scope
   mismatch returns `ACCESS_DENIED`.
2. Memory `FAILED`, malformed bounded context, or unsupported provider-safe
   summary class returns `REJECT_NARRATION`.

### A.7.9 Composer Validation

Required checks:

1. The composed response comes only from Response Composer.
2. Its response status permits the intent contract's narration behavior.
3. Its primary intent matches the narration contract.
4. Its compressed context is bounded and structurally eligible.
5. Its citations bind to the immutable citation package.
6. Its arithmetic remains Composer-owned and unchanged.
7. Raw `frontend_payload` is not copied into provider egress.

Failure classification:

1. Cross-scope Composer binding returns `ACCESS_DENIED`.
2. Malformed, unsupported, failed, or narration-ineligible Composer context
   returns `REJECT_NARRATION` or `DETERMINISTIC_ONLY` according to the
   approved deterministic fallback policy.

### A.7.10 Provider-Safe Projection Validation

The gate must create and validate a minimized external-egress projection.

Allowed projection classes:

1. Bounded current-turn content, marked as untrusted user data.
2. Approved minimized Composer compressed context fields.
3. Approved redacted bounded Memory-summary classes.
4. Exact immutable citation tokens needed for narration references.
5. Approved intent-contract and narration-policy markers required for
   bounded narration behavior.

Forbidden projection classes:

1. Raw execution, Tool, database, ORM, transcript, log, or frontend payloads.
2. Authentication tokens, JWT claims, secrets, or connection strings.
3. User, tenant, workspace, scenario, broker-session, or chat identifiers.
4. Foreign, deleted, failed, access-denied, or unbound data.
5. Hidden retrieval instructions, provider-memory identifiers, or external
   Tool capabilities.

Any denylisted field or unrecognized field returns `REJECT_NARRATION`.

### A.7.11 Prompt Budget Validation

The Admission Gate performs pre-assembly budget eligibility checks only. It
does not build a prompt.

Required checks:

1. Each projection class respects its approved hard size limit.
2. Required non-evictable content fits inside the approved pre-assembly
   budget.
3. Output allowance and fixed-policy overhead are reserved under a versioned
   budget policy.
4. Optional-field omission follows deterministic versioned rules.
5. Required content is never silently truncated.

Future Prompt Assembly must perform the final exact prompt-budget check before
provider invocation. Either preflight or final-budget failure blocks provider
invocation and produces authorized deterministic fallback.

### A.7.12 Narration Contract Validation

Required checks:

1. Exactly one approved intent-specific narration contract applies.
2. The contract version is active and default-off activation has been
   explicitly enabled.
3. Allowed narration fields are available only through the provider-safe
   projection.
4. Required sparse, insufficient, partial-success, and failure disclosures
   are preserved.
5. The prohibited-claims matrix applies.
6. No generic contract substitution is permitted.

Missing, mismatched, disabled, or ambiguous narration contract status returns
`DETERMINISTIC_ONLY` when the request remains safe for deterministic delivery.
Contract-integrity corruption returns `REJECT_NARRATION`.

### A.7.13 Grounding Eligibility Validation

Before provider invocation, the gate must prove that downstream grounding can
evaluate the future candidate deterministically.

The internal grounding-eligibility manifest must identify:

1. Approved intent and contract version.
2. Allowed narration fields.
3. Exact upstream numeric values eligible for pass-through.
4. Immutable scoped citation-token set.
5. Required evidence-limitation disclosures.
6. Applicable prohibited-claim categories.
7. Property-specific citation binding for comparison narration.
8. Required rejection behavior.

The provider must not receive the internal grounding manifest unless an
individual policy marker is explicitly allowed in the provider-safe
projection.

If deterministic post-generation grounding cannot be proven possible, the
gate returns `REJECT_NARRATION`.

## A.8 Required Rejection Conditions

The gate must block provider invocation when:

1. Authentication proof is absent, invalid, stale, or unbound.
2. Tenant, workspace, scenario, or broker-session scope is foreign, deleted,
   ambiguous, or mismatched.
3. Composer and Memory artifacts do not bind.
4. Memory status is `FAILED` or `ACCESS_DENIED`.
5. Citations are foreign, malformed, unsupported, fabricated, aliased, or
   unbound.
6. The intent is not explicitly enabled under one approved contract.
7. A generic or multi-intent narration path is attempted without approval.
8. The provider-safe projection contains any denylisted or unrecognized
   field.
9. Pre-assembly budget eligibility fails.
10. Grounding eligibility cannot be proven.
11. Any required policy version is missing, ambiguous, or inconsistent.

## A.9 Fail-Closed Behavior

The gate's fail-closed rule is:

```text
Only ADMIT_NARRATION may continue toward Prompt Assembly.
Every other state blocks provider invocation.
```

The fallback distinction is security-critical:

1. `ACCESS_DENIED` permits no scoped disclosure.
2. `DETERMINISTIC_ONLY` permits the authorized Composer-owned deterministic
   response when existing delivery policy allows it.
3. `REJECT_NARRATION` suppresses model narration and permits authorized
   deterministic fallback only when confidentiality and authorization remain
   intact.

# Section B: Admission Gate Decisions

## B.1 Mandatory Pre-Provider Validation

The following must be validated before provider invocation:

| Validation | Required outcome |
| --- | --- |
| Authentication proof | Active, request-bound, internal proof only. |
| Tenant scope | One consistent authorized subject scope. |
| Workspace scope | Active, same-tenant, cross-artifact match. |
| Optional scenario | Active, same-tenant, same-workspace, intent-compatible match. |
| Optional broker session | Active, same-tenant, same-workspace, scenario-compatible match. |
| Intent activation | Single contract, explicitly enabled, default-off policy satisfied. |
| Composer context | Response-owned, bounded, structurally eligible, intent-compatible. |
| Memory context | Memory-owned, bounded, structurally eligible, scope-compatible. |
| Citation package | Immutable, exact, scoped, non-generated, correctly bound. |
| Provider-safe projection | Allowlisted fields only, denylisted fields absent. |
| Prompt budget preflight | Required non-evictable content fits approved budget. |
| Narration contract | Exact approved contract and prohibited-claims policy available. |
| Grounding eligibility | Downstream original-output grounding can evaluate every allowed claim class. |

## B.2 Conditions That Must Block Provider Invocation

Every state other than `ADMIT_NARRATION` blocks provider invocation.

This includes:

1. Authentication or scope uncertainty.
2. Cross-tenant or cross-workspace mismatch.
3. Deleted, foreign, or mismatched scenario or session.
4. Failed or denied Memory context.
5. Invalid Composer binding.
6. Invalid citation package.
7. Default-off, unsupported, generic, clarification, or multi-intent
   narration.
8. Projection minimization failure.
9. Prompt-budget failure.
10. Grounding-ineligibility failure.
11. Missing or ambiguous policy version.

## B.3 Conditions That Must Produce Deterministic Fallback

Authorized Composer-owned deterministic fallback must be used, when existing
delivery policy allows it, for:

1. `DETERMINISTIC_ONLY`.
2. `REJECT_NARRATION` where authorization and confidentiality remain intact.
3. Future Prompt Assembly final-budget rejection.
4. Future Provider Adapter timeout, transport error, unavailable provider, or
   malformed response.
5. Future Candidate Parser rejection.
6. Future Grounding Layer rejection.
7. Future required Memory-owned post-narration commit failure.

Deterministic fallback must never weaken `ACCESS_DENIED`.

## B.4 Conditions That Must Return ACCESS_DENIED

`ACCESS_DENIED` is required for:

1. Missing, invalid, stale, or untrusted authentication proof reaching the
   gate.
2. Foreign, deleted, ambiguous, or mismatched tenant scope.
3. Foreign, deleted, ambiguous, or mismatched workspace.
4. Foreign, deleted, ambiguous, or mismatched scenario.
5. Foreign, deleted, ambiguous, or mismatched broker session.
6. Memory `ACCESS_DENIED`.
7. Cross-tenant or cross-workspace Composer, Memory, or citation binding.
8. Any condition where deterministic fallback could disclose scoped content
   to an untrusted subject.

`ACCESS_DENIED` blocks the provider and permits no scoped disclosure.

## B.5 Conditions That Must Return REJECT_NARRATION

`REJECT_NARRATION` is required when authorization remains valid but narration
cannot safely proceed:

1. Memory `FAILED`.
2. Malformed or narration-ineligible Composer context.
3. Invalid in-scope citation package, fabricated citation, alias, fallback
   evidence ID, or placeholder comparable.
4. Provider-safe projection denylist hit or unknown field.
5. Pre-assembly prompt-budget overflow.
6. Missing grounding-eligibility manifest.
7. Grounding policy cannot validate an allowed claim category.
8. Required policy versions are corrupt or inconsistent.

`REJECT_NARRATION` blocks the provider and uses authorized deterministic
fallback when permitted.

## B.6 Conditions That Must Return DETERMINISTIC_ONLY

`DETERMINISTIC_ONLY` is required when the request is authorized but model
narration is not approved or not useful:

1. `GENERAL_QUESTION`.
2. Clarification-required result.
3. Unsupported intent.
4. Generic catch-all flow.
5. Multi-intent result without a separately approved contract.
6. Eligible intent still default-off or administratively disabled.
7. Sparse or insufficient evidence where the intent contract and policy
   determine that no useful grounded narration remains.

`DETERMINISTIC_ONLY` blocks the provider and preserves the authorized
deterministic response.

## B.7 Formal Admission Gate Decision

**Decision**

The Narration Admission Gate must be a deterministic, no-I/O, fail-closed
policy firewall with four explicit states.

**Reason**

A binary allow-or-deny result would collapse security denial, safe
deterministic-only behavior, and narration-specific rejection. That ambiguity
could either leak scoped data or unnecessarily suppress safe deterministic
delivery.

**Alternatives considered**

1. Put checks inside Prompt Assembly.
2. Put checks inside the Provider Adapter.
3. Validate only after provider response.
4. Use one generic failure state.

**Risks**

Policy complexity can drift across versions or become duplicated downstream.

**Mitigations**

Keep the gate deterministic, version policies, centralize admission
classification, prohibit I/O, and require downstream stages to honor the
admission state without reinterpretation.

**GO / NO-GO impact**

Any bypass, I/O ownership, fail-open behavior, or collapsed security state is
`NO_GO`.

# Section C: Provider Adapter Architecture

## C.1 Purpose

The Provider Adapter is a stateless external-transport boundary. It sends one
approved future Prompt Assembly payload to one explicitly approved provider
profile and returns the original unmodified provider response plus bounded
transport metadata.

The Provider Adapter is not a reasoning, policy, prompt, parsing, grounding,
memory, persistence, failover, or delivery layer.

## C.2 Runtime Placement

The Provider Adapter sits only after:

1. `ADMIT_NARRATION` from the Admission Gate.
2. Future Prompt Assembly creation of one bounded provider request.
3. Future Prompt Assembly final exact budget approval.

It sits before:

1. Future Candidate Parser.
2. Grounding Layer.
3. Any optional Memory-owned post-generation commit.
4. Delivery.

No provider response may be streamed to a client before parsing and grounding
complete.

## C.3 Provider Abstraction

The modern Provider Adapter boundary must be provider-neutral:

1. One common invocation contract.
2. One common bounded response wrapper.
3. One common timeout outcome.
4. One common transport-error outcome.
5. One common malformed-response outcome after parsing.
6. One common audit-metadata vocabulary.
7. One common statelessness rule.
8. One common denylist for provider-visible data.

Provider-specific HTTP formats, credentials, endpoint conventions, and
structured-output capabilities remain behind the adapter boundary. They must
not leak into Intent Engine, Planner, Executor, Composer, Memory Integration,
Admission Gate, Grounding Layer, or delivery policy.

The modern adapter must not inherit its architecture implicitly from the
legacy broker namespace.

## C.4 Provider Neutrality

Provider neutrality does not mean every vendor is automatically allowed.

Each provider profile requires explicit governance approval for:

1. Vendor and endpoint.
2. Model or model family.
3. Data-processing location.
4. Retention posture.
5. Training-use posture.
6. Logging posture.
7. Statelessness behavior.
8. Structured-output capability.
9. Timeout ceiling.
10. Maximum request size.
11. Maximum response size.
12. Audit and observability metadata.
13. Credential handling.
14. Contractual and operational controls.

An unapproved profile is unavailable and causes deterministic fallback.

## C.5 Provider Selection

The Provider Adapter must not select providers dynamically.

Provider selection must be:

1. Deterministic.
2. Configuration-bound.
3. Restricted to an explicitly approved profile.
4. Independent of prompt content, tenant content, LLM output, and provider
   suggestions.
5. Auditable without disclosing tenant content.

No runtime heuristic, model preference, cheapest-provider routing, content
inspection, or vendor fallback is approved by this review.

## C.6 Provider Failover Policy

Transparent provider failover is `FORBIDDEN` by default.

Reason:

1. Failover sends tenant-scoped content to an additional external processor.
2. Providers can differ in retention, geography, logging, and structured
   output behavior.
3. Silent failover complicates audit and consent posture.
4. Duplicate egress increases leakage surface.

If the selected provider is unavailable, the approved behavior is:

```text
Suppress narration -> use authorized deterministic Composer fallback
```

Any future failover policy requires a separate architecture review and
explicit approval for every provider pair and failure class.

## C.7 Provider Timeout Handling

The adapter must enforce an explicit hard timeout ceiling approved per
provider profile.

On timeout:

1. Stop waiting for provider output.
2. Emit a bounded timeout outcome.
3. Do not deliver partial provider content.
4. Do not persist provider content as accepted narration.
5. Use authorized deterministic Composer fallback.
6. Record bounded redacted operational metadata.

Exact timeout values are not approved by this review and must be decided
before implementation.

## C.8 Provider Retry Policy

Automatic retry is `FORBIDDEN` by default.

Reason:

1. Retry duplicates tenant-scoped external egress.
2. Retry can change operational cost and exposure.
3. Retry can conceal provider instability.
4. Retry can create divergent outputs for the same request.

Any future retry policy requires separate approval and must be:

1. Bounded.
2. Restricted to explicitly approved transient transport conditions.
3. Identical in provider profile, payload, policy version, and timeout.
4. Prohibited for malformed output, hallucination, grounding rejection,
   contract rejection, or content-policy rejection.
5. Auditable as a distinct additional egress event.

## C.9 Provider Isolation

The Provider Adapter must enforce:

1. Stateless request-response behavior.
2. No provider-side thread, assistant, session, or conversation continuity.
3. No provider memory.
4. No Tool invocation.
5. No function calling.
6. No browsing.
7. No external retrieval.
8. No file upload.
9. No embeddings or vector-memory call.
10. No database access.
11. No arbitrary endpoint selection.
12. No client-visible token streaming before grounding.

If a provider cannot operate under these restrictions, it is not eligible.

## C.10 Provider Ownership Boundaries

The Provider Adapter owns:

1. Approved-profile transport invocation.
2. Out-of-band provider authentication.
3. Hard timeout enforcement.
4. Bounded response-size enforcement.
5. Original-response preservation.
6. Bounded redacted transport metadata.
7. Uniform unavailable, timeout, and transport-error outcomes.

The Provider Adapter does not own:

1. Provider selection policy.
2. Prompt construction.
3. Prompt minimization.
4. Tenant validation.
5. Citation validation.
6. Retry or failover unless separately approved.
7. Candidate repair or normalization.
8. Grounding acceptance.
9. Memory retrieval or persistence.
10. Frontend payload construction.
11. Delivery, SSE, WebSocket, or client streaming.

## C.11 Provider Audit Requirements

The adapter may record only bounded redacted operational metadata:

1. Internal opaque request correlation identifier.
2. Approved provider-profile identifier.
3. Approved model-profile identifier.
4. Policy versions.
5. Start and finish timestamps.
6. Duration.
7. Request-size metadata.
8. Response-size metadata.
9. Outcome category.
10. Timeout category.
11. Attempt count.
12. Transport error category.

The adapter must not log by default:

1. Prompt content.
2. Provider response content.
3. Full current-turn text.
4. Tenant identifiers.
5. Workspace, scenario, broker-session, or chat identifiers.
6. JWT claims, tokens, secrets, or credentials.
7. Raw citation packages.
8. Raw Memory context.
9. Raw Composer context.

Any exceptional redacted-content logging requires a separate retention,
access-control, and security approval. It must never become conversation
memory.

## C.12 Provider Observability

Required observability is operational, not content-based:

1. Invocation count by approved provider profile.
2. Timeout rate.
3. Transport-error rate.
4. Response-size rejection rate.
5. Candidate-parser rejection rate.
6. Grounding rejection rate.
7. Deterministic-fallback rate.
8. Latency distribution.
9. Unavailable-profile rate.
10. Legacy-path activation attempts.

Observability must not expose scoped content or create a shadow transcript
store.

# Section D: Provider Restrictions

## D.1 Provider-Visible Allowlist

Providers may see only the future Prompt Assembly output derived from the
validated provider-safe projection:

| Provider-visible category | Decision | Justification |
| --- | --- | --- |
| Bounded current-turn content | `ALLOWED` | Allowed only as untrusted user data required for narration. |
| Minimized Composer compressed-context projection | `ALLOWED` | Composer-owned bounded context is the approved narration source. |
| Approved redacted bounded Memory-summary classes | `ALLOWED` | Only explicitly allowlisted summaries may support narration continuity. |
| Exact immutable citation tokens required for narration | `ALLOWED` | Citation tokens are pass-through-only evidence references. |
| Approved intent-contract and narration-policy markers | `ALLOWED` | Providers need bounded behavioral instructions, not authority. |

Citation tokens are the only opaque evidence identifiers eligible for
provider visibility. Their presence does not authorize any other internal
identifier.

## D.2 Provider-Visible Forbidden Matrix

| Proposed provider-visible data | Decision | Justification |
| --- | --- | --- |
| Raw `ExecutionResult` | `FORBIDDEN` | Raw execution output stops at Response Composer. |
| Raw Tool payloads | `FORBIDDEN` | Tools are upstream execution owners; only Composer-minimized context may cross the provider boundary. |
| Database rows | `FORBIDDEN` | Providers have no persistence or raw-data authority. |
| ORM objects | `FORBIDDEN` | ORM entities expose persistence structure and uncontrolled fields. |
| JWT claims | `FORBIDDEN` | Providers do not authenticate or authorize requests. |
| Tenant identifiers | `FORBIDDEN` | Tenant identity is internal validation metadata and is unnecessary for narration. |
| User identifiers | `FORBIDDEN` | User identity is unnecessary for narration. |
| Workspace identifiers | `FORBIDDEN` | Workspace identity remains internal binding metadata. |
| Scenario identifiers | `FORBIDDEN` | Scenario identity remains internal binding metadata. |
| Broker-session identifiers | `FORBIDDEN` | Provider-side session continuity is prohibited. |
| Chat identifiers | `FORBIDDEN` | Provider-side conversation continuity is prohibited. |
| Secrets | `FORBIDDEN` | Secrets have no narration purpose. Provider credentials remain out-of-band and model-invisible. |
| Full chat history | `FORBIDDEN` | Only approved redacted bounded Memory summaries may cross the boundary. |
| Raw frontend payloads | `FORBIDDEN` | Frontend-safe delivery data is not automatically provider-safe or provider-necessary. |
| Raw Memory context | `FORBIDDEN` | Only approved redacted bounded summary classes may cross the boundary. |
| Raw Composer context | `FORBIDDEN` | Only the minimized approved projection may cross the boundary. |
| Authentication tokens or bearer tokens | `FORBIDDEN` | Tokens are secrets and create direct compromise risk. |
| Connection strings or database credentials | `FORBIDDEN` | Providers have no infrastructure role. |
| Provider-side thread or conversation IDs | `FORBIDDEN` | ValorAI Memory Integration exclusively owns continuity. |
| Unrestricted logs, snapshots, prediction logs, shadow logs, or Tool events | `FORBIDDEN` | Only governed Composer and Memory summaries may cross the boundary. |

## D.3 Provider Restrictions Decision

**Decision**

The provider may receive only a minimized provider-safe prompt. Every
unlisted field is denied by default.

**Reason**

Provider neutrality and narration utility do not justify broad tenant-data
egress.

**Alternatives considered**

1. Send the entire validated internal envelope.
2. Send full Memory context.
3. Send raw frontend-safe payloads.
4. Allow provider-specific extra fields.

**Risks**

A future implementation may treat internal validation data as external
provider context.

**Mitigations**

Keep internal envelope and external projection separate, use explicit
allowlists, and reject unknown fields before provider invocation.

**GO / NO-GO impact**

Broad, implicit, or provider-specific hidden egress is `NO_GO`.

# Section E: Provider Response Policy

## E.1 Maximum Allowed Provider Output

The provider response must be minimal. The maximum semantic output is:

1. One bounded candidate narration text.
2. One bounded list of exact immutable citation tokens referenced by the
   candidate narration.

The candidate narration may include inline references only in the approved
form:

```text
[citation:<exact-received-id>]
```

The provider must not return:

1. Authoritative-value replacement fields.
2. New arithmetic fields.
3. Scores, rankings, confidence computations, forecasts, or recommendations.
4. Tool calls, function calls, plans, or follow-up requests.
5. Memory writes, provider-thread IDs, session IDs, or continuity metadata.
6. Fabricated citation objects, aliases, comparable wrappers, or evidence
   records.
7. Frontend payloads or transport instructions.

Exact maximum character count, token count, and citation-reference count are
not approved by this review. They must be explicitly decided before
implementation. Absence of approved hard limits blocks implementation.

## E.2 Required Narration Schema

The future Candidate Parser may accept only a minimal conceptual schema:

| Field | Requirement | Authority |
| --- | --- | --- |
| Candidate narration text | Required, bounded, untrusted. | Provider proposes; Grounding Layer accepts or rejects. |
| Citation-reference list | Required when the text references citations; bounded; exact tokens only. | Provider proposes; Grounding Layer verifies against immutable package. |

No provider field is authoritative. Additional or unknown fields cause
candidate rejection unless separately approved in a later architecture
decision.

## E.3 Citation Handling

Provider citation behavior is pass-through only:

1. The provider may repeat exact allowlisted citation tokens.
2. The provider may not create, transform, alias, normalize, infer, or repair
   a citation.
3. The parser and Grounding Layer must compare citation references against
   the immutable scoped package.
4. Inline citations and the citation-reference list must agree.
5. Foreign, missing, fabricated, unsupported, or mismatched citations reject
   the candidate.

## E.4 Grounding Relationship

The Provider Adapter never grounds output.

Required downstream sequence:

```text
Original provider response
  -> Candidate Parser
  -> Grounding Layer validates original candidate
  -> accept or reject
```

The adapter and parser must not repair, overwrite, enrich, or attach
deterministic authoritative values before Grounding Layer rejection or
acceptance.

## E.5 Rejection and Fail-Closed Handling

The future narration runtime must reject provider narration and use authorized
deterministic fallback for:

1. Provider unavailable.
2. Timeout.
3. Transport error.
4. Response-size overflow.
5. Empty response.
6. Malformed response.
7. Unknown response fields.
8. Schema mismatch.
9. Citation mismatch.
10. Hallucinated facts.
11. Prohibited claims.
12. New arithmetic.
13. Stronger certainty than upstream evidence allows.
14. Grounding rejection.

No rejected or partial candidate content may reach delivery or accepted
conversation memory.

## E.6 Provider Hallucination Handling

Hallucination is not repaired. It is rejected.

The approved rule is:

```text
Detect unsupported claim -> reject original candidate -> suppress narration
-> deliver authorized deterministic fallback
```

The runtime must not:

1. Replace a hallucinated value with a deterministic value before rejection.
2. Remove one unsupported sentence and deliver the rest.
3. Ask the same provider to repair the output automatically.
4. Send the output to a second provider automatically.
5. Persist the rejected text as accepted assistant memory.

## E.7 Timeout and Malformed Output Handling

| Provider outcome | Narrative delivery | Accepted-memory persistence | Deterministic fallback |
| --- | --- | --- | --- |
| Timeout | Suppressed | Forbidden | Required when authorized |
| Transport error | Suppressed | Forbidden | Required when authorized |
| Response-size overflow | Suppressed | Forbidden | Required when authorized |
| Empty output | Suppressed | Forbidden | Required when authorized |
| Malformed output | Suppressed | Forbidden | Required when authorized |
| Unknown output fields | Suppressed | Forbidden | Required when authorized |
| Grounding rejection | Suppressed | Forbidden | Required when authorized |
| Grounding acceptance | Eligible only after downstream policy | Memory-owned only when separately approved | Not needed |

## E.8 Formal Provider Response Decision

**Decision**

Provider output is a minimal untrusted candidate, never an authoritative
response.

**Reason**

Structured output can still contain unsupported claims. Schema compliance is
not grounding.

**Alternatives considered**

1. Accept provider JSON as authoritative.
2. Repair malformed output.
3. Deliver partial text.
4. Stream model tokens directly to the client.

**Risks**

Strict rejection can reduce narration availability.

**Mitigations**

Preserve the Composer-owned deterministic fallback as the authoritative
delivery path.

**GO / NO-GO impact**

Any direct, repaired, partial, or pre-grounding narrative delivery is
`NO_GO`.

# Section F: Multi-Tenant Review

## F.1 Tenant-Safe Provider Requests

Provider requests remain tenant-safe only when:

1. Authentication and scope validation complete upstream.
2. The Admission Gate verifies one consistent subject and workspace binding.
3. Optional scenario and broker-session bindings are verified internally.
4. Internal identifiers are stripped from provider egress.
5. Only minimized allowlisted context crosses the provider boundary.
6. Unknown fields fail closed.
7. No provider-side continuity exists.

The provider does not need tenant identity to narrate approved context.

## F.2 Citation Leakage Prevention

Citation leakage is prevented by:

1. Composer and Memory ownership of immutable citation packages.
2. Admission Gate package-binding validation.
3. Exact scoped citation-token allowlists.
4. No aliases, fallback IDs, repair, lookup, or synthesis.
5. Property-specific citation binding for Property Comparison.
6. Grounding rejection for foreign, missing, fabricated, unsupported, or
   mismatched tokens.

Citation tokens are the only permitted opaque evidence identifiers. They must
not be used as a path to broader retrieval.

## F.3 Memory Leakage Prevention

Memory leakage is prevented by:

1. Memory Integration remaining the only retrieval owner.
2. Admission Gate accepting bounded governed Memory context only.
3. Provider egress allowing only explicitly approved redacted bounded-summary
   classes.
4. Full transcripts, raw messages, unrestricted history, and database rows
   remaining forbidden.
5. No provider-side thread, memory, or continuity.
6. No Provider Adapter persistence.

## F.4 Session Leakage Prevention

Session leakage is prevented by:

1. Internal broker-session binding validation.
2. No heuristic latest-session selection.
3. No broker-session ID in provider egress.
4. No provider-managed session or thread.
5. Fail-closed `ACCESS_DENIED` for foreign, deleted, or mismatched session
   scope.

## F.5 Cross-Workspace Leakage Prevention

Cross-workspace leakage is prevented by:

1. Workspace binding validation across authenticated proof, Composer output,
   Memory context, optional scenario, optional broker session, and citations.
2. No cross-workspace merge.
3. No workspace ID in provider egress.
4. `ACCESS_DENIED` for any foreign, deleted, ambiguous, or mismatched
   workspace artifact.
5. No scoped deterministic fallback after access denial.

## F.6 Multi-Tenant Review Decision

**Decision**

Tenant safety must be established before provider egress and must not depend
on the provider.

**Reason**

Post-provider detection is too late: the disclosure has already happened.

**Alternatives considered**

1. Trust route-level checks only.
2. Validate only after grounding.
3. Include tenant IDs so the provider can separate requests.
4. Use provider-side conversations for continuity.

**Risks**

Artifact-binding mistakes can still create accidental mixed context.

**Mitigations**

Require fail-closed Admission Gate binding, deny internal identifiers from
egress, and treat any cross-scope inconsistency as `ACCESS_DENIED`.

**GO / NO-GO impact**

Any provider contact before tenant-safe admission is `NO_GO`.

# Section G: Boundary Ownership Matrix

## G.1 Final Ownership Matrix

| Layer | Owns | Does Not Own | May Read | May Not Read |
| --- | --- | --- | --- | --- |
| Intent Engine | Deterministic intent classification and clarification decision. | Tool calls, provider calls, prompt assembly, arithmetic, memory, persistence, delivery. | Authenticated current-turn content. | Database, ORM, Tool payloads, Memory context, provider responses, secrets. |
| Tool Planner | Deterministic mapping from approved intent to approved execution plan. | Tool execution, provider calls, arithmetic, narration, memory, persistence. | Intent result. | Database, ORM, Tool runtime payloads, Memory context, provider responses, secrets. |
| Tool Executor | Approved Tool 1-8 invocation, raw payload preservation, timeout and failure isolation. | Tool-selection policy, composition, prompt assembly, provider calls, narration, memory ownership. | Execution plan and approved tenant-scoped Tool context. | Prompt content, provider responses, narration contracts, delivery transport. |
| Response Composer | Tool normalization, approved arithmetic, citation preservation, bounded compressed context, frontend-safe payload. | Database access, memory retrieval, provider calls, narration, prompt assembly, delivery. | Extended `ExecutionResult` only. | `ExecutionPlan`, database, ORM, provider responses, secrets. |
| Memory Integration | Bounded idempotent Composer-summary persistence, governed bounded Memory-context rebuild, citation preservation, optional separately approved post-generation accepted-narration commit. | Prompt assembly, provider calls, narration generation, grounding acceptance, delivery. | Validated scope, execution result, composed response, approved accepted grounded narration when post-generation commit is approved. | Provider credentials, raw rejected provider output as accepted memory, foreign context. |
| Admission Gate | Deterministic narration-admission classification, artifact binding, projection minimization, pre-budget eligibility, grounding eligibility. | Authentication execution, database access, prompt text, provider invocation, retry, failover, output parsing, grounding acceptance, persistence, delivery. | Internal authenticated-scope proof, bounded current turn, intent marker, Composer output, Memory context, binding proofs, citation package, approved policy versions. | Raw JWT, tokens, secrets, `ExecutionPlan`, raw `ExecutionResult`, raw Tool payloads, ORM, database rows, full transcripts, provider response. |
| Provider Adapter | Stateless approved-profile transport, out-of-band provider authentication, hard timeout, response-size enforcement, original-response preservation, bounded redacted transport metadata. | Provider selection policy, prompt construction, tenant decisions, citations, parsing repair, grounding acceptance, memory, persistence, delivery, SSE. | Future Prompt Assembly output, approved provider profile, out-of-band credential handle, bounded internal correlation metadata. | Raw scope envelope, database, ORM, raw Tool payloads, raw Memory context, raw Composer context, frontend payloads, tenant identifiers in prompt content. |
| Grounding Layer | Original-candidate validation against contract, immutable citations, exact upstream values, evidence limitations, and prohibited claims. | Prompt assembly, provider invocation, output repair before rejection, Tool calls, memory writes, delivery. | Original parsed candidate, internal grounding manifest, validated scoped envelope, immutable citation package. | Database, ORM, raw Tool payloads, provider credentials, foreign context. |
| Future Narration Runtime | Sequence coordination, state propagation, deterministic fallback handoff, approved-stage invocation order. | Intent classification, Tool selection, Tool execution, arithmetic, memory retrieval, persistence, citation creation, grounding override, provider-side memory, delivery content mutation. | Admission decision, future prompt result, Provider Adapter outcome, parser outcome, grounding outcome, deterministic fallback status. | Database, ORM, raw Tool payloads, raw unrestricted Memory context, secrets, foreign scope, rejected candidate as deliverable narration. |

## G.2 Prompt Assembly Boundary Reservation

Prompt Assembly architecture is intentionally reserved for a separate review.
This review approves no prompt text and no prompt implementation.

Any future Prompt Assembly architecture must:

1. Consume only the validated scoped narration envelope.
2. Use only the provider-safe projection for external request content.
3. Apply the final exact hard-budget check.
4. Add no database, ORM, Tool, memory-retrieval, provider-selection,
   persistence, or delivery ownership.
5. Preserve all denylist rules in this review.

# Section H: GO / NO-GO Review

## H.1 Phase 5.5C.6F Admission Gate Decision

```text
6F_DECISION: CONDITIONAL_GO
```

### Decision

The Narration Admission Gate architecture is conditionally approved as a
deterministic, no-I/O, fail-closed policy firewall with the four states
`ADMIT_NARRATION`, `DETERMINISTIC_ONLY`, `REJECT_NARRATION`, and
`ACCESS_DENIED`.

### Reason

The gate is necessary to prove authorization, tenancy, artifact binding,
contract activation, citation integrity, egress minimization, budget
eligibility, and grounding eligibility before provider contact.

### Alternatives Considered

1. Put checks in Prompt Assembly.
2. Put checks in the Provider Adapter.
3. Trust upstream route checks.
4. Validate only after provider response.

### Risks

1. Policy duplication.
2. Ambiguous failure-state handling.
3. Internal identifiers leaking into provider projection.
4. Budget logic drifting into prompt construction.

### Mitigations

1. Centralize pre-provider policy in the gate.
2. Keep the gate no-I/O and deterministic.
3. Separate internal envelope from provider-safe projection.
4. Require a separate final Prompt Assembly budget check.

### GO / NO-GO Impact

Any gate bypass, provider contact before `ADMIT_NARRATION`, hidden I/O,
collapsed security denial, or broad provider projection is `NO_GO`.

## H.2 Phase 5.5C.6G Provider Adapter Decision

```text
6G_DECISION: CONDITIONAL_GO
```

### Decision

The Provider Adapter architecture is conditionally approved as a stateless,
provider-neutral, minimized, no-retry, no-failover transport boundary that
returns original unmodified provider output for downstream parsing and
grounding.

### Reason

The provider is untrusted. Narrow transport ownership limits disclosure and
prevents legacy provider behavior from redefining modern orchestration.

### Alternatives Considered

1. Reuse the legacy broker provider runtime unchanged.
2. Enable transparent failover.
3. Enable automatic retries.
4. Use provider-side conversations.
5. Stream provider tokens directly to clients.

### Risks

1. Reduced narration availability.
2. Provider-specific retention or logging behavior.
3. Malformed or hallucinated output.
4. Duplicate egress if retry or failover is later introduced.

### Mitigations

1. Use Composer-owned deterministic fallback.
2. Require per-provider governance profiles.
3. Ground original candidate output after parsing.
4. Keep retry and failover forbidden unless separately reviewed.

### GO / NO-GO Impact

Provider-side memory, broad egress, direct delivery, implicit legacy reuse,
transparent failover, automatic retry, output repair, or missing hard limits
are `NO_GO`.

## H.3 Combined Decision

```text
COMBINED_DECISION: CONDITIONAL_GO
ARCHITECTURE_ONLY: APPROVABLE
PROMPT_ASSEMBLY_ARCHITECTURE: NOT APPROVED BY THIS REVIEW
IMPLEMENTATION: NO_GO
RUNTIME_ACTIVATION: NO_GO
PROVIDER_INTEGRATION: NO_GO
PRODUCTION_PROMOTION: NO_GO
```

The combined architecture may advance only to the next explicit architecture
gate. It does not authorize implementation or provider traffic.

## H.4 Minimum Approvals Before Implementation May Resume

Before implementation may resume, governance must explicitly approve:

1. The four Admission Gate states and their exact fallback semantics.
2. `ACCESS_DENIED` as the mandatory no-disclosure state for cross-scope risk.
3. `DETERMINISTIC_ONLY` for general-question, clarification, unsupported,
   generic, multi-intent, and disabled narration flows.
4. `REJECT_NARRATION` for authorized but narration-unsafe flows.
5. The complete Admission Gate validation list.
6. The strict separation between internal scoped envelope and external
   provider-safe projection.
7. The provider-visible allowlist.
8. The provider-visible forbidden matrix.
9. Tenant identifiers as forbidden provider-visible data.
10. Citation tokens as the only externally eligible opaque evidence
    identifiers.
11. The minimal provider response contract.
12. Exact hard request, response, output-token, character, citation-count, and
    timeout limits.
13. Provider-specific profile approvals for endpoint, model, geography,
    retention, logging, training use, statelessness, and credentials.
14. Automatic retry forbidden by default.
15. Transparent failover forbidden by default.
16. Provider-side memory, threads, sessions, Tools, functions, browsing,
    retrieval, files, embeddings, and client-visible pre-grounding streaming
    forbidden.
17. Original-output grounding with no repair before rejection.
18. Deterministic Composer fallback for authorized narration failure.
19. No scoped fallback for `ACCESS_DENIED`.
20. A separate Prompt Assembly Architecture review before any prompt work.
21. Isolation and retirement of the legacy broker LLM activation path.
22. Governed disposition of the unauthorized prior Phase 5.5C.6 artifacts.

## H.5 Final Verdict

```text
6F_DECISION: CONDITIONAL_GO
6G_DECISION: CONDITIONAL_GO
COMBINED_DECISION: CONDITIONAL_GO
NEXT_ALLOWED_WORK_AFTER_EXPLICIT_APPROVAL: PROMPT ASSEMBLY ARCHITECTURE REVIEW ONLY
```
