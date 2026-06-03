# ValorAI Phase 5.5C.6B Boundary Ownership Matrix

Decision date: 2026-06-01  
Decision scope: Phase 5.5C.6 component ownership and prohibited drift  
Implementation status: Architecture decision only  

## 1. Governing Rule

```text
Planner decides.
Executor executes.
Composer computes.
Memory remembers.
Future LLM narrates.
```

Every Phase 5.5C.6 boundary must preserve this rule. Convenience, legacy
compatibility, and provider capability do not justify ownership drift.

## 2. Component Ownership Matrix

| Component | Exclusive responsibilities | Allowed inputs | Allowed outputs | Must never own |
| --- | --- | --- | --- | --- |
| Authentication and Tenant Scope Boundary | Authenticate subject, establish tenant scope, conceal foreign resources, authorize request entry. | Request credentials and route context. | Authenticated scoped request or denial. | Prompt content, LLM provider calls, narration, Tool selection, arithmetic, citations, or memory writes. |
| Intent Engine | Deterministic intent classification and clarification decision. | Authenticated current turn. | Auditable intent result. | Tool calls, database access, prompt assembly, provider use, or persistence. |
| Tool Planner | Deterministic mapping from approved intent to approved execution plan. | Intent result. | Auditable execution plan. | Tool execution, database access, arithmetic, narration, or persistence. |
| Tool Executor | Invoke only approved Tools 1-8, preserve raw payloads, isolate failures and timeouts. | Execution plan and authenticated scoped Tool context. | Raw auditable execution result. | Tool selection policy, response composition, arithmetic, compression, prompt assembly, LLM use, or memory writes beyond Tool-owned existing behavior. |
| Response Composer | Normalize Tool 1-8 outputs, compute approved arithmetic, preserve received citations, create compressed context, create frontend-safe payload. | Extended execution result only. | Composed response with deterministic structured channels. | Tool execution, database access, memory retrieval, persistence, prompt assembly, LLM use, or citation fabrication. |
| Memory Integration Pre-Generation | Persist one bounded idempotent Composer summary in the approved store, rebuild bounded tenant-scoped memory context, preserve received and persisted citations. | Validated scope, execution result, composed response, optional scenario, optional broker session. | Governed memory context or fail-closed denial. | LLM use, prompt assembly, narration, provider calls, arbitrary assistant-message selection, or citation fabrication. |
| Narration Admission Gate | Bind scope, validate context compatibility, reject denied or unsupported states, enforce provider egress projection and budget eligibility. | Authenticated scope, composed response, memory context, bounded current turn. | One validated scoped narration envelope or rejection. | Intent classification, Tool calls, arithmetic, database access, persistence, provider calls, narration, or citation mutation. |
| Prompt Assembly | Build bounded provider prompt from the validated provider-safe projection and fail closed on budget overflow. | One validated scoped narration envelope only. | Provider request payload. | Independent scope resolution, raw user transcript retrieval, database access, Tool payload retrieval, arithmetic, citation creation, persistence, or delivery. |
| Stateless LLM Provider Adapter | Invoke one approved provider with uniform timeout, bounded retry, error, structured-output, and statelessness behavior. | Provider request payload. | Untrusted provider response and provider metadata. | Provider-side conversation memory, Tool calls, database access, persistence, tenant decisions, citations, calculations, grounding approval, or delivery. |
| Candidate Parser | Parse provider response without repairing authority claims. | Original provider response. | Original candidate narration representation or rejection. | Value overwrite, citation synthesis, arithmetic, persistence, or delivery. |
| Deterministic Grounding and Governance | Validate original candidate against Composer values, Memory context, immutable citations, supported-intent policy, and prohibited-claim rules. | Original candidate, validated scoped envelope, deterministic composed response, immutable citation packages. | Accepted grounded narration or rejection with reason. | Prompt assembly, provider calls, Tool calls, value repair before validation, citation fabrication, memory writes, or transport. |
| Memory Integration Post-Generation | When explicitly approved, commit accepted grounded narration and required provenance to the correct bound conversation. | Accepted grounded narration and validated binding. | Commit success or failure. | Provider calls, grounding approval, arbitrary chat selection, rejected narration persistence, or delivery. |
| Delivery and Transport | Deliver Composer-owned frontend payload and optional grounded narration; own API, SSE, or other transport behavior. | Authorized deterministic payload, optional accepted grounded narration, delivery status. | Client response or stream events. | Tool selection, arithmetic, prompt assembly, provider calls, grounding approval, citation mutation, or memory ownership. |
| Audit and Telemetry | Record bounded operational facts under an approved retention policy. | Stage status, latency, rejection category, provider metadata allowed by policy. | Audit events and metrics. | Accepted-memory substitution, secret logging, unrestricted prompt logging, unrestricted provider-output logging, or cross-tenant disclosure. |

## 3. Exact LLM Integration Ownership

LLM Integration is allowed to own only:

1. Deterministic use of an approved prompt template.
2. Token-budget enforcement with fail-closed overflow behavior.
3. Creation of a minimized provider request from the approved provider-safe
   projection.
4. Invocation of an approved stateless provider.
5. Collection of bounded provider metadata required for audit and operations.
6. Parsing of provider output as untrusted candidate narration.
7. Return of that candidate to a separate deterministic Grounding and
   Governance stage.

LLM Integration must never own:

1. Intent classification, clarification, planning, Tool selection, Tool
   execution, Tool orchestration, or follow-up execution.
2. Valuation, pricing, calculation, comparison arithmetic, ranking,
   confidence computation, forecasting, ROI, returns, offer construction, or
   market-trend invention.
3. Citation creation, aliases, fallback citation IDs, comparable wrappers,
   citation resolution, citation repair, or citation mutation.
4. Tenant authentication, tenant authorization, scope binding, soft-delete
   decisions, workspace selection, scenario selection, session selection, or
   chat selection.
5. Database sessions, ORM access, database queries, database writes, memory
   retrieval, memory compression, memory commits, or persistence fallback.
6. Grounding approval, response repair before grounding, governance
   acceptance, frontend payload construction, API delivery, SSE, WebSocket,
   or transport wrappers.
7. Provider-side threads, provider-side conversation history, embeddings,
   vector memory, or unapproved external state.

## 4. Prompt Assembly Input Allowlist

Prompt Assembly receives exactly one validated scoped narration envelope. The
envelope may contain only the following categories:

| Allowed category | Ownership | Conditions |
| --- | --- | --- |
| Bounded current-turn content | Narration Admission Gate | Must be marked as untrusted user data, size-limited, and represented inside the envelope rather than supplied as a separate raw argument. |
| `compressed_context` | Response Composer | Must remain Composer-owned, bounded, and unchanged by LLM Integration. |
| Supported-intent markers and deterministic status | Response Composer and approved activation policy | Only intents with an approved narration contract may proceed. |
| Bounded memory summaries | Memory Integration | Must be selected by Memory Integration, tenant-scoped, bounded, and provider-safe. |
| Immutable citation packages or deterministic provider-safe citation projection | Response Composer and Memory Integration | Must preserve identity and provenance; no aliasing or replacement records. |
| Internal scope-binding metadata | Narration Admission Gate | Used for deterministic checks; excluded from external egress unless explicitly allowlisted as necessary. |
| Explicit narration policy markers | Governance policy | Used to state prohibited claim categories and supported narration behavior. |

## 5. Prompt Assembly Forbidden Input List

The following data must never enter Prompt Assembly:

| Forbidden category | Reason |
| --- | --- |
| `ExecutionPlan` | Planning ownership must remain upstream. |
| Raw `ExecutionResult` | Raw Tool execution payloads exceed the narration boundary. |
| Raw Tool 1-8 payloads | Response Composer is the required normalization and compression boundary. |
| ORM entities or database rows | Prompt Assembly must not become a persistence or retrieval boundary. |
| Direct database query results | Memory Integration and Composer own governed context construction. |
| Full chat transcripts or unrestricted message history | Only Memory-owned bounded summaries are allowed. |
| Independently supplied raw user text | Current-turn content must be bounded inside the validated envelope. |
| Unvalidated user, workspace, scenario, broker-session, chat, property, or citation identifiers | Scope must fail closed before Prompt Assembly. |
| Authentication tokens, signing secrets, API keys, provider keys, or connection strings | Secrets have no narration purpose. |
| Foreign-tenant, deleted-scope, `FAILED`, or `ACCESS_DENIED` memory content | Denied data must not reach a provider. |
| Raw `frontend_payload` by default | Frontend-safe delivery data is not automatically provider-necessary data. |
| Fabricated evidence IDs, aliases, placeholder comparables, or zero-price replacement records | Citation ownership remains upstream and immutable. |
| Unrestricted audit logs, prediction logs, shadow logs, tool events, or snapshots | Only governed Composer and Memory summaries may cross the prompt boundary. |
| Content that exceeds the approved non-evictable prompt budget | Prompt budget must fail closed. |
| Unsupported-intent context | Unsupported intents bypass LLM narration. |

## 6. Provider Egress Allowlist

Data entering Prompt Assembly is not automatically data that may leave
ValorAI. The provider request must be a deterministic minimized projection.

| Egress category | External provider egress |
| --- | --- |
| Bounded current-turn content | Allowed only when required for narration and framed as untrusted data. |
| Composer compressed context | Allowed only through an approved minimized projection. |
| Memory summaries | Allowed only when each summary class is explicitly allowlisted and redacted. |
| Citation tokens | Allowed when needed for narration references and preserved immutably. |
| User ID, workspace ID, scenario ID, broker-session ID, chat ID | Denied by default. Allow only if a separately approved provider requirement proves necessity. |
| JWT claims and bearer tokens | Always denied. |
| Secrets and provider credentials | Always denied except provider authentication handled outside prompt content. |
| Full transcripts, raw Tool payloads, raw database content | Always denied. |

## 7. Citation Ownership Matrix

| Citation action | Response Composer | Memory Integration | Narration Admission Gate | Prompt Assembly | LLM Provider | Grounding and Governance | Delivery |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Preserve received citations | Owns | Owns for persisted and received citations | Verifies package binding | Passes provider-safe projection | May reference allowlisted tokens only | Verifies every returned reference | Attaches deterministic package |
| Create citation aliases | Forbidden | Forbidden unless separately governed upstream policy exists | Forbidden | Forbidden | Forbidden | Forbidden | Forbidden |
| Create fallback evidence IDs | Forbidden | Forbidden | Forbidden | Forbidden | Forbidden | Forbidden | Forbidden |
| Synthesize comparable records | Forbidden | Forbidden | Forbidden | Forbidden | Forbidden | Forbidden | Forbidden |
| Resolve returned citation membership | Not applicable | Not applicable | Checks envelope membership before provider use | Not applicable | Not authoritative | Owns post-generation check | Uses approved result |
| Mutate citation package | Forbidden after emission | Forbidden after emission | Forbidden | Forbidden | Forbidden | Forbidden | Forbidden |

Citation packages are immutable once emitted by their approved upstream
owner. If evidence is sparse, the correct behavior is sparse or insufficient
evidence disclosure, not evidence fabrication.

## 8. Persistence Ownership Matrix

| Persistence point | Allowed | Owner | Conditions |
| --- | --- | --- | --- |
| Tool-owned existing persistence before Composer | Yes | Existing Tool Layer owners | Existing approved Tool behavior only. |
| Composer persistence | No | None | Composer remains deterministic and persistence-free. |
| Memory summary persistence before LLM | Yes | Memory Integration | Existing bounded idempotent Composer summary only. |
| Memory context retrieval before LLM | Yes | Memory Integration | Tenant-scoped, bounded, fail-closed retrieval only. |
| Prompt Assembly persistence | No | None | No database or memory service access. |
| Provider adapter persistence | No | None | Stateless generation only. |
| Candidate parser persistence | No | None | Parse only. |
| Grounding validator persistence | No | None | Validate only. |
| Accepted narration persistence after grounding | Optional | Memory Integration Post-Generation | Must be explicitly approved, bound to the validated conversation, and limited to accepted grounded narration plus approved provenance. |
| Rejected candidate persistence as assistant memory | No | None | Rejected output is never accepted memory. |
| Operational rejection telemetry | Optional | Audit and Telemetry | Bounded, redacted, retention-governed, and distinct from conversation memory. |
| Delivery persistence | No | None | Delivery does not remember. |

## 9. Grounding Ownership Matrix

| Checkpoint | Timing | Required checks | Failure behavior |
| --- | --- | --- | --- |
| G0: Tenant and status admission | Before Prompt Assembly | Scope binding, soft-delete state, `FAILED`, `ACCESS_DENIED`, supported intent. | Reject narration before provider egress. |
| G1: Egress and budget admission | Before provider invocation | Provider-safe projection, redaction, immutable citation membership, token budget. | Reject narration before provider egress. |
| G2: Original-output grounding | Immediately after parsing | Citation membership, unsupported numeric claims, unsupported arithmetic, rankings, confidence claims, prices, forecasts, offers, intent-specific policy. | Reject candidate without repair. |
| G3: Pre-persistence approval | Before Memory-owned commit | Candidate accepted, validated binding unchanged, approved provenance present. | Do not persist candidate narration. |
| G4: Pre-delivery approval | Before API or stream delivery | Grounding accepted, required commit status satisfied, deterministic payload attached separately. | Suppress narration; use authorized deterministic fallback when available. |

## 10. Formal Matrix Decisions

### B-01: The Ownership Matrix Is Normative

**Decision**

The component ownership matrix is the normative Phase 5.5C.6 responsibility
boundary.

**Reason**

The forensic audit found ownership drift caused by convenience coupling to
legacy persistence, citations, and validators.

**Alternatives considered**

1. Use informal responsibility guidance.
2. Let implementation define boundaries.
3. Approve exceptions case by case after activation.

**Risks**

A matrix can become documentation-only unless approval evidence tests it.

**Mitigations**

Make matrix conformance a prerequisite for implementation review and runtime
activation evidence.

**GO / NO-GO impact**

Any implementation that contradicts the matrix is `NO-GO`.

### B-02: Prompt Assembly Is a Closed Boundary

**Decision**

Prompt Assembly accepts one validated envelope and no hidden side inputs.

**Reason**

Independent user text, raw context, retrieval, or scope values create
unreviewed prompt channels.

**Alternatives considered**

1. Permit multiple convenience arguments.
2. Permit Prompt Assembly database lookups.
3. Permit provider-specific extra context.

**Risks**

Future features may pressure the boundary to expand silently.

**Mitigations**

Require governance approval for any new envelope field or egress class.

**GO / NO-GO impact**

Hidden Prompt Assembly side inputs are `NO-GO`.

### B-03: Citation Identity Is Immutable

**Decision**

Citation identity and provenance remain unchanged after Composer and Memory
emission.

**Reason**

Aliases and replacement comparable records create a second evidence system.

**Alternatives considered**

1. Allow adapter-level aliases.
2. Allow provider-generated evidence IDs.
3. Allow compatibility wrappers.

**Risks**

Sparse evidence can tempt implementations to fabricate compatibility records.

**Mitigations**

Use explicit sparse-evidence narration and deterministic citation validation.

**GO / NO-GO impact**

Fabricated or mutated citations are `NO-GO`.

### B-04: Memory Is the Exclusive Persistence Owner

**Decision**

Memory Integration exclusively owns memory retrieval and all accepted
conversation persistence before or after narration.

**Reason**

The locked architecture explicitly assigns remembering to Memory.

**Alternatives considered**

1. Persist from the LLM adapter.
2. Persist from delivery.
3. Persist from grounding.

**Risks**

Post-generation persistence can drift into arbitrary transcript storage.

**Mitigations**

Bind commits to accepted grounded narration and an already validated scoped
envelope.

**GO / NO-GO impact**

Persistence owned by any other Phase 5.5C.6 component is `NO-GO`.

## 11. Boundary Verdict

```text
BOUNDARY_OWNERSHIP_DECISION: CONDITIONAL_GO
CONDITION: ALL PHASE 5.5C.6 IMPLEMENTATION MUST CONFORM TO THIS MATRIX
EXISTING_ATTEMPTED_IMPLEMENTATION: NO_GO
```
