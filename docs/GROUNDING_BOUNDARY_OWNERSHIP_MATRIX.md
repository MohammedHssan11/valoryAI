# ValorAI Grounding Boundary Ownership Matrix

Review date: 2026-06-02  
Phase: 5.5C.6H Grounding Architecture Review  
Status: Architecture only  

## Locked Rule

```text
Planner decides.
Executor executes.
Composer computes.
Memory remembers.
LLM narrates.
Grounding validates.
```

## Normative Ownership Matrix

| Layer | Owns | May read | Must never own | Must never read |
| --- | --- | --- | --- | --- |
| Prompt Assembly | Deterministic request serialization, approved optional-context eviction, final exact budget decision, bounded redacted assembly metadata. | One admitted envelope, provider-safe projection, approved assembly policy. | Candidate parsing, grounding, provider invocation, retrieval, calculation, persistence, delivery. | Provider response, raw Memory context, raw Composer response, Tool payloads, database rows, JWT claims. |
| Provider Adapter | Approved-profile stateless transport, out-of-band credential use, timeout and response-size enforcement, original-response preservation, bounded transport metadata. | One assembled request artifact and approved provider profile. | Prompt construction, retry or failover unless separately approved, parsing, grounding, persistence, delivery. | Raw scoped envelope, raw Memory context, raw Composer response, Tool payloads, tenant identifiers in prompt content. |
| Candidate Parser | Parse original provider response without repair, enrichment, normalization that changes meaning, or authority mutation. | Original unmodified provider response. | Grounding approval, value overwrite, citation synthesis, narration repair, persistence, delivery. | Database, Memory retrieval, Tool payloads, secrets, provider-side memory. |
| Grounding | Validate original candidate against one bound grounding manifest, immutable scoped citations, one narration contract, prohibited-claims policy, and evidence limitations. | Original parsed candidate, manifest, immutable citation package, bounded assembly metadata, approved policy versions, opaque binding attestations. | Calculation, narration, repair, summarization, inference, retrieval, provider calls, prompt assembly, persistence, delivery. | Raw Memory context, raw Composer response, ExecutionResult, ExecutionPlan, raw Tool payloads, database rows, ORM entities, JWT claims, raw frontend payload. |
| Memory Integration | Pre-generation governed retrieval and bounded persistence; optional separately approved post-generation accepted-narration commit. | Validated scope, approved upstream artifacts, accepted grounded narration only when separately approved. | Grounding acceptance, provider calls, prompt assembly, narration generation, delivery. | Rejected candidate as accepted memory, foreign context, provider credentials. |
| Delivery | Deliver Composer-owned deterministic payload and optional accepted grounded narration under authorization policy. | Authorized deterministic payload, Grounding outcome, optional accepted grounded narration, approved citations. | Grounding override, value mutation, citation mutation, persistence, prompt assembly, provider calls. | Rejected candidate, provider secrets, foreign context. |

## Grounding Exclusive Ownership

Grounding exclusively owns:

1. Original-candidate acceptance or rejection.
2. Exact pass-through validation.
3. Intent-contract compliance validation.
4. Prohibited-claim enforcement.
5. Citation-reference validation.
6. Evidence-limitation preservation validation.
7. Binding and policy-version continuity checks at the post-provider boundary.
8. Bounded redacted decision metadata.

## Grounding Prohibited Ownership

Grounding must never:

1. Calculate or recompute values.
2. Narrate.
3. Repair or sanitize candidate text.
4. Summarize.
5. Infer intent, facts, or meaning beyond deterministic contract validation.
6. Retrieve from any store.
7. Call a provider.
8. Trigger retry or failover.
9. Reassemble a prompt.
10. Create evidence or citations.
11. Persist accepted or rejected text.
12. Deliver text.

## Overlap Decision

Any overlap between Grounding and Prompt Assembly, Provider Adapter, Candidate
Parser, Memory Integration, or Delivery is `NO_GO`.

Observed legacy and unauthorized paths do overlap these responsibilities.
They are not approved Grounding architecture.

