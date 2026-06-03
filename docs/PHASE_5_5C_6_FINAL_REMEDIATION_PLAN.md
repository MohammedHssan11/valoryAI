# Phase 5.5C.6 Final Remediation Plan

Review date: 2026-06-02  
Review mode: Final architecture closure review only  
Reference authority: `PROJECT_MASTER_STATE_V2.md`  
Implementation activity: Prohibited  

# STOP CONDITION

The required authority document is incomplete for this closure decision.
`PROJECT_MASTER_STATE_V2.md` was last updated before the later Prompt Assembly
and Grounding artifacts. It still states that Prompt Assembly Architecture is
outstanding, does not record the Phase 5.5C.6H Grounding decision, and contains
no explicit Candidate Parser architecture disposition.

The later repository artifacts were inspected only to identify the missing
authority information and the unresolved forensic blockers. They cannot be
silently promoted into master-state approvals by this report.

Closure review stops with `NO_GO`. The only allowed work is blocker resolution
and authoritative master-state synchronization. This report does not authorize
implementation, prompts, providers, validators, schemas, tests, APIs, runtime
wiring, runtime activation, or production promotion.

# MISSING REQUIRED INFORMATION

The following required information is missing from
`PROJECT_MASTER_STATE_V2.md`:

1. The authoritative disposition of Phase 5.5C.6E Prompt Assembly
   Architecture.
2. The authoritative disposition of Phase 5.5C.6H Grounding Architecture and
   its citation, prohibited-claims, deterministic-validation, failure,
   security, and trust-boundary rules.
3. An explicit Candidate Parser architecture disposition. The master state
   names the layer in the canonical sequence but does not approve its narrow
   parsing-only responsibility.
4. Explicit governance acceptance or rejection for the still-conditional
   Narration Contracts, Narration Admission Gate, Provider Adapter, and Prompt
   Assembly decisions.
5. Approved exact request, response, output-token, character, citation-count,
   and timeout limits.
6. Approved provider-specific governance profiles covering endpoint, model,
   geography, retention, logging, training use, statelessness, and
   credentials.
7. The governed disposition of unauthorized prior Phase 5.5C.6 artifacts.
8. Evidence that the legacy broker LLM activation path is isolated and
   retired from the modern narration-only path.
9. Authoritative resolution of the Grounding forensic blockers: mutation
   before validation, citation synthesis, synthetic comparable wrappers,
   adapter-owned retrieval and persistence, raw Memory coupling, incomplete
   prohibited-claims enforcement, fallback revalidation, and competing
   activatable paths.

# APPROVED

The following authority-held target constraints are safe to keep as-is. They
do not grant implementation authorization.

---

## Issue

Narration Contracts preserve narration-only authority.

## Severity

P2

## Current Design

The master state records nine default-off intent-specific narration contracts:
Valuation, Explainability, Comparables, Fairness, What-if, Negotiation,
Investment, Market Insight, and Property Comparison. Exact upstream facts and
immutable citation tokens may pass through. General-question, clarification,
unsupported, generic catch-all, and multi-intent narration remain
deterministic-only.

## Problem

No design defect is present in this target constraint. It remains conditional
and default-off.

## Recommended Action

KEEP

## Reason

The constraint prevents the LLM from becoming a calculator, planner,
recommender, evidence creator, citation creator, or missing-context repair
layer.

## Blocks Implementation?

NO

---

## Issue

The Narration Admission Gate boundary is correctly narrow.

## Severity

P2

## Current Design

The master state records a deterministic, no-I/O, fail-closed pre-provider
policy firewall with four states: `ADMIT_NARRATION`, `DETERMINISTIC_ONLY`,
`REJECT_NARRATION`, and `ACCESS_DENIED`. Only `ADMIT_NARRATION` may proceed.
`ACCESS_DENIED` permits no scoped disclosure.

## Problem

No design defect is present in this target constraint. It remains
architecture-only and unimplemented.

## Recommended Action

KEEP

## Reason

The gate preserves tenant isolation, deterministic fallback semantics, and a
single pre-provider egress decision.

## Blocks Implementation?

NO

---

## Issue

The Provider Adapter boundary is correctly transport-only.

## Severity

P2

## Current Design

The master state records a stateless, minimized, provider-neutral transport
boundary. Provider-side memory, Tools, functions, browsing, retrieval, files,
embeddings, pre-grounding client streaming, automatic retry, and transparent
failover are forbidden by default.

## Problem

No design defect is present in this target constraint. Exact hard limits and
provider profiles are still unresolved separately.

## Recommended Action

KEEP

## Reason

The transport boundary must not acquire reasoning, memory, persistence,
delivery, retry, failover, or hidden egress authority.

## Blocks Implementation?

NO

---

## Issue

The canonical narration-only sequence preserves existing owners.

## Severity

P2

## Current Design

The master state places the future narration-only path after Memory
Integration and before Delivery:

```text
Intent Engine
  -> Tool Planner
  -> Tool Executor
  -> Response Composer
  -> Memory Integration Pre-Generation
  -> Narration Admission Gate
  -> Prompt Assembly
  -> Stateless Provider Adapter
  -> Candidate Parser
  -> Deterministic Grounding and Governance
  -> Memory Integration Post-Generation, when separately approved
  -> Delivery
```

## Problem

No defect is present in the ordering itself. The named boundaries still
require the blocker resolutions below.

## Recommended Action

KEEP

## Reason

Planner decides, Executor executes, Composer computes, Memory remembers, the
LLM narrates, and Grounding validates.

## Blocks Implementation?

NO

# MUST FIX

---

## Issue

The master-state authority is not synchronized with the completed review set.

## Severity

P0

## Current Design

`PROJECT_MASTER_STATE_V2.md` records Phase 5.5C.6D, 5.5C.6F, and 5.5C.6G as
architecture-only `CONDITIONAL_GO`, but still says Prompt Assembly
Architecture remains a separate required review. It does not include the
later Phase 5.5C.6E Prompt Assembly review or Phase 5.5C.6H Grounding decision
in its status tables, architecture-governance summary, roadmap, or source
index.

## Problem

A final closure decision cannot rely on unstated or stale authority. Silent
promotion of later artifacts would bypass the designated master state.

## Recommended Action

MODIFY

## Reason

Synchronize `PROJECT_MASTER_STATE_V2.md` with explicit accepted or rejected
dispositions before implementation is considered.

## Blocks Implementation?

YES

---

## Issue

The Candidate Parser has no explicit architecture disposition.

## Severity

P1

## Current Design

The master state names `Candidate Parser` in the canonical runtime path but
does not record an approved parser boundary. Later non-authoritative artifacts
refer to a narrow parsing-only role that preserves the original provider
response and forbids repair, enrichment, overwrite, normalization, or
authority mutation.

## Problem

Grounding depends on original-candidate integrity. Without an explicit
authority-held parser disposition, parsing could become an unreviewed repair
or authority-mutation layer.

## Recommended Action

MODIFY

## Reason

Record an explicit acceptance or rejection of the already-described
parsing-only boundary in the master state. Do not implement the parser until
that disposition is authoritative.

## Blocks Implementation?

YES

---

## Issue

Conditional architecture decisions have not been converted into explicit
governance acceptance or rejection.

## Severity

P1

## Current Design

The master state records the Narration Contracts, Narration Admission Gate,
and Provider Adapter as architecture-only `CONDITIONAL_GO`. Its roadmap still
requires explicit governance acceptance or rejection. The later Prompt
Assembly artifact is also conditional and is not synchronized into the master
state.

## Problem

`CONDITIONAL_GO` is not implementation approval. Advancing without explicit
disposition would erase the governance gate that the master state requires.

## Recommended Action

MODIFY

## Reason

Record explicit acceptance or rejection for each conditional boundary without
widening its responsibility.

## Blocks Implementation?

YES

---

## Issue

Prompt Assembly controls are not authoritatively approved.

## Severity

P1

## Current Design

The later Prompt Assembly artifact describes a deterministic
representation-only boundary after `ADMIT_NARRATION`. It also reports
unresolved approvals for the provider-visible allowlist and denylist,
protected context, optional context classes, stable eviction order and
tie-break rules, tokenizer and serializer versions, fixed-overhead and
response-reserve accounting, safe citation-token representability, opaque
internal attestations, bounded redacted metadata retention, single-contract
enforcement, and deterministic-only excluded flows.

## Problem

Prompt Assembly cannot safely serialize tenant-scoped context or enforce
budgets until these decisions are explicit and authority-held. Ambiguity could
create hidden side inputs, silent truncation, citation leakage, or a widened
external egress surface.

## Recommended Action

MODIFY

## Reason

Resolve and record the existing Prompt Assembly approval checklist. Preserve
the representation-only boundary.

## Blocks Implementation?

YES

---

## Issue

Exact provider hard limits and provider-specific governance profiles are
undecided.

## Severity

P1

## Current Design

The master state explicitly records this open risk. Exact request, response,
output-token, character, citation-count, and timeout limits are not approved.
Provider-specific endpoint, model, geography, retention, logging, training
use, statelessness, and credential controls are also not approved.

## Problem

The Provider Adapter cannot prove minimized egress, deterministic budget
behavior, retention posture, or bounded failure behavior without fixed
limits and an approved profile.

## Recommended Action

MODIFY

## Reason

Approve and record the exact limits and provider-specific governance profile
before any provider implementation or integration.

## Blocks Implementation?

YES

---

## Issue

Unauthorized prior Phase 5.5C.6 artifacts and the legacy broker LLM activation
path remain unresolved.

## Severity

P0

## Current Design

The master state records unauthorized attempted modern LLM paths outside the
canonical target and a legacy broker LLM activation path that can conflict
with the narration-only design. It requires a governed disposition and
isolation or retirement before implementation resumes.

## Problem

Competing activatable paths can bypass Prompt Assembly, tenant-safe admission,
original-output Grounding, Memory ownership, and the approved canonical
sequence.

## Recommended Action

REPLACE

## Reason

Keep unauthorized paths non-canonical and non-activatable, record their
governed disposition, and isolate and retire the legacy activation path from
the modern narration-only runtime.

## Blocks Implementation?

YES

---

## Issue

Observed Grounding-related paths violate original-candidate integrity and
locked ownership boundaries.

## Severity

P0

## Current Design

The later Grounding artifacts report these forensic findings in observed
unauthorized and legacy paths:

1. Parsed authoritative values are overwritten before validation.
2. Citation aliases and fallback evidence IDs are synthesized.
3. Synthetic zero-price comparable wrappers are created.
4. Raw Memory context is consumed by an unapproved prompt path.
5. The adapter queries latest workspace chat directly.
6. The adapter persists narration outside Memory ownership.
7. The legacy validator does not enforce the full prohibited-claims matrix or
   all nine narration contracts.
8. Legacy finalization creates and revalidates fallback narration after
   Grounding failure.
9. Competing activatable LLM paths remain present.

## Problem

These behaviors create authority drift, hidden retrieval, hidden
calculations, hidden memory usage, citation fabrication, Grounding repair,
Grounding self-healing, and bypass risk. A validator cannot prove that an
altered candidate was originally grounded.

## Recommended Action

REPLACE

## Reason

Resolve the forensic blockers so that only the documented narrow
Grounding boundary can remain eligible for later implementation. Do not reuse
the legacy Grounding behavior as the modern boundary.

## Blocks Implementation?

YES

---

## Issue

Grounding Architecture is not authority-held as implementation-ready.

## Severity

P0

## Current Design

The master state does not record Phase 5.5C.6H. The later Grounding decision
artifact states `ARCHITECTURE_DECISION: NO_GO`,
`GROUNDING_ARCHITECTURE: NO_GO`, `IMPLEMENTATION: NO_GO`, and
`NEXT_ALLOWED_WORK: GOVERNANCE RESOLUTION OF FORENSIC BLOCKERS ONLY`.

## Problem

Grounding is the mandatory trust boundary between untrusted provider output
and persistence or Delivery. Implementation cannot proceed while the boundary
is absent from the authority document and the observed runtime is rejected.

## Recommended Action

MODIFY

## Reason

Resolve the documented forensic blockers and synchronize the resulting
explicit Grounding disposition into the master state. No implementation may
precede that disposition.

## Blocks Implementation?

YES

# OPTIONAL

No optional Phase 5.5C.6 architecture improvements are proposed. Optional
expansion would be inappropriate while the authority document is incomplete
and mandatory blockers remain unresolved.

# GROUNDING REVIEW

GROUNDING_NOT_READY_FOR_IMPLEMENTATION

## Citation Integrity

The target rule is correct: citations are immutable scoped pass-through
tokens only; fabricated, aliased, modified, missing, unsupported, or
mismatched citations reject narration; foreign or cross-workspace citations
return `ACCESS_DENIED`. The observed paths synthesize aliases, fallback IDs,
and comparable wrappers. Citation integrity is not implementation-ready.

## Prohibited Claims Enforcement

The target rule is correct: unsupported generated prices, arithmetic,
forecasts, predictions, ROI, IRR, CAGR, yield, appreciation, returns, new
offers, new strategies, rankings, winner declarations, recommendations,
synthetic trends, synthetic evidence, synthetic assumptions, and synthetic
citations reject the entire candidate. The observed legacy validator does not
enforce the full matrix or all nine contracts. Enforcement is not
implementation-ready.

## Exact Pass-Through Rules

The target rule is correct: only exact upstream values may be restated where
the selected contract permits them. Rounding, conversion, normalization,
recombination, enrichment, repair, and replacement are forbidden. The
observed path overwrites parsed authoritative values before validation. Exact
pass-through is not implementation-ready.

## Deterministic Validation

The target rule is correct: Grounding must be deterministic, no-I/O,
repeatable, restart-stable, provider-independent, manifest-bound,
immutable-citation-bound, single-contract-bound, and decision-only. The
observed path relies on incomplete legacy checks and fallback revalidation.
Deterministic validation is not implementation-ready.

## Fail-Closed Behavior

The target rule is correct: ambiguity rejects narration; Grounding failure
must not trigger repair, provider retry, failover, prompt reassembly,
partial delivery, or accepted-memory persistence. The observed legacy path
creates and revalidates fallback narration after failure. Fail-closed
behavior is not implementation-ready.

## Tenant Isolation

The target rule is correct: foreign, ambiguous, untrusted, or cross-scope
bindings return `ACCESS_DENIED`, with no scoped fallback. Grounding itself
must perform no retrieval. Competing activatable paths and adapter-owned
latest-chat retrieval prevent a closed tenant-isolation proof. Tenant
isolation is not implementation-ready.

## No Hidden Authority

The target rule is correct: Grounding validates only. It must not calculate,
retrieve, narrate, repair, persist, deliver, retry, fail over, or self-heal.
The observed paths contain mutation, retrieval, persistence, citation
synthesis, synthetic wrappers, and fallback revalidation. No-hidden-authority
compliance is not implementation-ready.

# NON-PHASE PRODUCTION NOTE

The master state also retains separate production-promotion blockers,
including frontend JWT integration, direct valuation authentication policy,
managed secrets, RBAC, test drift, process-local metrics and rate limits, and
incomplete CI/CD. This closure review does not reclassify or redesign them.

IMPLEMENTATION_READY_ITEMS

* Keep the nine default-off exact pass-through Narration Contracts.
* Keep deterministic-only handling for general-question, clarification, unsupported, generic catch-all, and multi-intent flows.
* Keep the deterministic no-I/O fail-closed Narration Admission Gate target.
* Keep the stateless minimized provider-neutral Provider Adapter target.
* Keep the canonical narration-only sequence and existing Planner, Executor, Composer, Memory, Grounding, and Delivery ownership boundaries.

BLOCKING_ITEMS

* Synchronize `PROJECT_MASTER_STATE_V2.md` with explicit Prompt Assembly and Grounding dispositions.
* Record an explicit Candidate Parser architecture disposition.
* Convert all conditional architecture decisions into explicit governance acceptance or rejection.
* Resolve and record the Prompt Assembly approval checklist.
* Approve exact provider hard limits and provider-specific governance profiles.
* Record the governed disposition of unauthorized prior Phase 5.5C.6 artifacts.
* Isolate and retire the legacy broker LLM activation path from the modern narration-only path.
* Resolve all Grounding forensic blockers before any implementation.

OPTIONAL_IMPROVEMENTS

* None before blocker resolution.

FINAL_DECISION:
NO_GO

NEXT_ALLOWED_STEP:

* FIX_BLOCKERS_FIRST
