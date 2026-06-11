# ValorAI Phase 5.5C.4 Response Composer Architecture Blocker Report

Report date: 2026-06-01  
Scope: Mandatory pre-implementation review only  
Decision: **NO-GO - ARCHITECTURE CLARIFICATION REQUIRED**

## Executive Result

No Response Composer code was implemented.

The Phase 5.5C.4 brief requires implementation to stop immediately if any
architecture ambiguity or documentation conflict exists. The mandatory review
found multiple blockers that cannot be resolved without changing an upstream
contract, choosing between conflicting responsibilities, or inventing an
unapproved frontend contract.

## Mandatory References Reviewed

Read completely:

```text
../../PROJECT_MASTER_STATE_V2.md
../../COPILOT_ORCHESTRATOR_ARCHITECTURE.md
PHASE_5_5C_1_INTENT_ENGINE_IMPLEMENTATION_REPORT.md
PHASE_5_5C_2_TOOL_PLANNER_IMPLEMENTATION_REPORT.md
PHASE_5_5C_3_TOOL_EXECUTOR_IMPLEMENTATION_REPORT.md
../../COPILOT_ORCHESTRATOR_COMPOSER_ARCHITECTURE.md
../../COPILOT_ORCHESTRATOR_CONTEXT_COMPRESSION.md
../../COPILOT_ORCHESTRATOR_TOOL_CHAINING_MATRIX.md
```

Relevant implemented contracts were also inspected:

```text
EXECUTION_RESULT_CONTRACT.md
backend/app/copilot/orchestrator/planner/contracts.py
backend/app/copilot/orchestrator/executor/contracts.py
backend/app/copilot/orchestrator/executor/executor.py
backend/app/api/schemas/copilot_tools.py
backend/app/services/copilot_tools_service.py
backend/app/broker/schemas/contracts.py
frontend/src/types/broker.ts
```

## Architecture Understanding

The approved pipeline is:

```text
Intent Engine
  -> Tool Planner
  -> Tool Executor
  -> ExecutionResult
  -> Response Composer
  -> ComposedResponse
  -> Future LLM Narrator
```

The Response Composer is intended to be deterministic infrastructure. It may:

```text
normalize Tool outputs
calculate approved arithmetic
calculate property-comparison deltas
aggregate evidence
apply Top-N compression
preserve citations
produce an LLM-safe channel
produce a frontend-safe evidence channel
```

It must not:

```text
execute Tools
classify intents
plan Tools
query PostgreSQL or PostGIS
call Router, CMT, or ML
call an LLM provider
generate narrative language
```

The existing executor correctly returns raw Tool payload envelopes and
structured failures without composition.

## Blocking Architecture Conflicts

### Blocker 1: Required intent metadata is absent from `ExecutionResult`

The required `ComposedResponse` output includes:

```text
primary_intent
secondary_intents
```

The approved Composer input is:

```text
ExecutionResult
Raw Tool Payloads
Nothing else
```

However, `ExecutionResult` contains `plan_id`, execution status, Tool result
envelopes, failures, timing, and audit metadata only. It does not contain
`primary_intent` or `secondary_intents`.

The planner contract does contain both fields, but passing `ExecutionPlan` to
the Composer would violate the currently stated input boundary unless that
boundary is revised.

Required decision:

```text
A. Add primary_intent and secondary_intents to ExecutionResult.
B. Approve ExecutionPlan as an additional Composer input.
C. Remove those fields from ComposedResponse.
```

### Blocker 2: Approved property-comparison metrics cannot be computed from Tool 1 payloads

The architecture requires native Composer comparison of:

```text
price
size
features
confidence
```

The implemented Tool 1 response contains:

```text
valuation_id
fair_price
price_range
confidence_level
engine_used
routing_reason
timestamp
source
```

It does not contain property size, property features, or a numeric confidence
value. The Composer can compute price deltas, but it cannot truthfully compute
`sqm_delta`, feature deltas, or a numeric `confidence_delta` from the approved
input.

Required decision:

```text
A. Extend Tool 1 response with a governed property-facts snapshot and numeric
   confidence metric.
B. Extend the executor envelope with governed invocation facts approved for
   Composer comparison.
C. Limit the approved property-comparison output to fields already available
   in Tool 1 responses.
```

### Blocker 3: Required citation identifiers are not exposed at the Composer boundary

The architecture requires preservation of:

```text
snapshot_id
tool_event_id
comparable_ids
```

The phase brief additionally requires:

```text
valuation_ids
audit_ids
evidence_ids
```

Tool events are persisted by `CopilotToolsService._event`, but their IDs are
not returned in Tool responses or executor envelopes. Tool 1 exposes a
`valuation_id`, not an explicit `snapshot_id`. Comparable IDs are available
only in payloads that include comparable evidence. `audit_id` and
`evidence_id` do not have a canonical Phase 5.5C.4 definition.

The Composer cannot preserve identifiers it never receives, and it must not
query the database to recover them.

Required decision:

```text
A. Define whether valuation_id is the canonical snapshot citation.
B. Expose tool_event_id in Tool responses or executor envelopes.
C. Define audit_id and evidence_id semantics, including which Tools emit them.
D. Define behavior when an optional citation category is unavailable.
```

### Blocker 4: Composer responsibility conflicts with the no-LLM phase boundary

`../../COPILOT_ORCHESTRATOR_COMPOSER_ARCHITECTURE.md` assigns the Composer a
"Final Broker Response Assembly" responsibility that orchestrates LLM
generation and streams the response.

The Phase 5.5C.4 brief explicitly prohibits:

```text
Generate Narratives
Generate Natural Language
Call LLMs
Call OpenAI
Call Gemini
Call Anthropic
```

Required decision:

```text
A. Remove Final Broker Response Assembly from Phase 5.5C.4 and defer all LLM
   invocation and streaming to a later narrator phase.
B. Revise the Phase 5.5C.4 boundary to permit a narrowly defined integration.
```

### Blocker 5: The frontend evidence-channel contract is explicitly unresolved

The architecture documents explicitly leave this open:

```text
What is the exact payload structure expected by the frontend for citation
tracking in the SSE stream?
```

The brief requires:

```text
citation_package
frontend_payload
dual-channel delivery
frontend-safe context
```

The active frontend has a legacy Broker SSE contract with `evidence_ids`, but
no Phase 5.5C.4 `citations_payload` event or `ComposedResponse` contract.

Required decision:

```text
A. Define a new versioned ComposedResponse frontend contract.
B. Define whether the Composer emits a pure data object only or also an SSE
   event wrapper.
C. Define whether the legacy Broker evidence types are reused, migrated, or
   left untouched until frontend integration.
```

### Blocker 6: Top-N comparable ordering is not fully specified

The compression architecture requires Top 3 comparables sorted
deterministically by spatial/feature distance.

The normalized Comparable Tool item exposes:

```text
distance_km
similarity_reason
```

It does not expose a canonical numeric feature-distance or relevance score.
Sorting only by `distance_km` would be a new interpretation of "most
relevant." Stable tie-breaking is also unspecified.

Required decision:

```text
A. Approve distance_km ascending with comparable_id tie-break as the canonical
   Top-N comparator.
B. Expose an authoritative relevance score from the Tool Layer.
C. Define another governed comparator and tie-break order.
```

### Blocker 7: Failure, conflict, and recovery output schemas are undefined

The brief requires deterministic composition for:

```text
partial success
timeouts
missing evidence
sparse evidence
tool failures
conflicting evidence
restart recovery
```

The executor provides structured Tool failures, but no approved
`ComposedResponse` status taxonomy, conflict-detection rules, sparse-evidence
normalization rules, or Composer restart-recovery meaning are defined.

Required decision:

```text
A. Define ComposedResponse statuses and per-tool failure normalization.
B. Define which payload conditions count as sparse, missing, or conflicting.
C. Define whether restart recovery means deterministic replay of a supplied
   ExecutionResult or persistence of ComposedResponse artifacts.
```

## Risk Analysis

| Risk | Severity | Reason implementation is blocked |
| --- | --- | --- |
| Citation integrity loss | P0 | Required persisted IDs are inaccessible at the Composer boundary. |
| Invented comparison facts | P0 | Size, feature, and numeric confidence deltas cannot be derived from Tool 1 payloads. |
| Boundary violation | P0 | The draft assigns LLM orchestration to a phase that explicitly forbids LLM calls. |
| Frontend contract drift | P1 | Implementing `frontend_payload` now would invent an SSE or data schema. |
| Incorrect Top-N evidence | P1 | "Most relevant" has no approved numeric ordering contract. |
| Unverifiable recovery claim | P1 | Restart recovery semantics are undefined for a currently pure component. |

## Edge Case Analysis

The final contract must explicitly govern:

```text
one successful comparison valuation and one failed valuation
two successful valuations with only label-based confidence
zero comparable rows
fewer than three comparable rows
duplicate comparable IDs
equal comparable distances
missing optional citation categories
Tool 8 sparse evidence
multi-intent success plus timeout
payloads containing raw geometry or tenant-sensitive identifiers
```

## Failure Mode Analysis

| Failure mode | Required deterministic behavior |
| --- | --- |
| Partial property comparison | Preserve the successful property payload and failed slot metadata; do not emit deltas requiring both values. |
| Total Tool failure | Return a structured failed composition with no fabricated evidence. |
| Timeout | Preserve timeout type and planned Tool slot. |
| Sparse evidence | Preserve an approved sparse-evidence marker without generating replacement evidence. |
| Missing citations | Return an explicit citation-integrity status; do not silently omit required IDs. |
| Conflicting evidence | Apply only approved conflict rules; otherwise preserve both values without resolution. |

These behaviors require a concrete `ComposedResponse` contract before code can
be written.

## Boundary Validation

The proposed component boundary remains valid only if the unblocked design
continues to enforce:

```text
NO Tool execution
NO Intent Engine calls
NO Tool Planner calls
NO Router calls
NO CMT calls
NO ML calls
NO database queries
NO HTTP clients
NO embeddings
NO vector database
NO OpenAI
NO Gemini
NO Anthropic
NO LLM SDK
NO narrative generation
```

## Required Resolution Package

Before implementation resumes, approve:

```text
1. The exact Composer input contract.
2. The exact ComposedResponse schema.
3. The approved property-comparison metric set and upstream source fields.
4. Canonical citation ID definitions and exposure rules.
5. The frontend evidence-channel payload shape.
6. Top-N comparators and tie-break rules per evidence category.
7. Failure, sparse-evidence, conflict, and restart-recovery semantics.
8. Removal or deferral of LLM orchestration from Phase 5.5C.4.
```

## Validation Status

Not run for Phase 5.5C.4.

Per the mandatory stop rule, no Composer implementation, tests, Docker
validator, Docker execution, or success deliverables were created.

