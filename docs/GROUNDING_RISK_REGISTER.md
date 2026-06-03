# ValorAI Grounding Risk Register

Review date: 2026-06-02  
Phase: 5.5C.6H Grounding Architecture Review  
Status: Architecture only  

## Enterprise Risk Register

| ID | Risk | Severity | Likelihood | Impact | Mitigation | Residual risk |
| --- | --- | --- | --- | --- | --- | --- |
| G-01 | Candidate values are overwritten before validation. | Critical | High in observed path | Model drift is concealed and unsupported claims may pass. | Validate original unmodified candidate only; reject any repair-before-decision path. | Medium until observed path is retired |
| G-02 | Grounding recomputes values and becomes a second Composer. | Critical | Medium | Competing truth systems and arithmetic drift. | Membership and exactness validation only; no recalculation. | Low after conformance evidence |
| G-03 | Citation aliases or fallback IDs create a second evidence system. | Critical | High in observed path | Fabricated provenance and tenant leakage. | Immutable exact scoped tokens only; reject aliases. | Medium until observed path is retired |
| G-04 | Synthetic comparable wrappers corrupt evidence. | High | High in observed path | Grounding validates replacement records instead of received evidence. | Reject synthetic records and zero-price wrappers. | Medium until observed path is retired |
| G-05 | Foreign citation enters candidate narration. | Critical | Medium | Cross-tenant disclosure. | Return `ACCESS_DENIED`; no scoped fallback. | Low after binding evidence |
| G-06 | Missing citation is repaired rather than disclosed. | High | Medium | Unsupported evidence claim. | Reject candidate; preserve honest limitation. | Low |
| G-07 | Prompt injection causes unsupported claims. | High | High | Unsafe narration or authority escalation. | Original-candidate validation, prohibited-claim enforcement, no provider capabilities, deterministic fallback. | Medium |
| G-08 | Memory poisoning influences repeated narration. | High | Medium | Stored injection persists across turns. | Treat provider output as untrusted; Grounding trusts manifest facts, not instructions. | Medium |
| G-09 | Grounding retrieves database rows or Memory context. | Critical | Medium | Hidden scope expansion and leakage. | No-I/O Grounding boundary; manifest only. | Low after conformance evidence |
| G-10 | Adapter retrieves latest chat and persists narration outside Memory. | Critical | High in observed path | Wrong-chat persistence and uncontrolled memory. | Memory-owned post-generation commit only when separately approved. | Medium until observed path is retired |
| G-11 | Legacy grounding schema is reused for all modern intents. | High | High in observed path | Tool 3-8 and comparison claims escape intent-specific enforcement. | Exactly one modern contract per eligible intent. | Medium until observed path is retired |
| G-12 | Generic or multi-intent contracts merge silently. | High | Medium | Authority expands without review. | Deterministic-only handling; reject contract merge. | Low |
| G-13 | General-question LLM narration reaches Grounding. | High | Medium | Ungrounded open-ended provider content. | No provider invocation; reject accidental candidate. | Low |
| G-14 | Grounding ambiguity fails open. | Critical | Medium | Unsupported content reaches users. | Ambiguity returns `REJECT_NARRATION`. | Low |
| G-15 | Grounding repairs a partial candidate. | High | Medium | Validator becomes narrator and conceals provider drift. | Reject entire candidate; no partial delivery. | Low |
| G-16 | Grounding triggers retry or failover. | High | Medium | Duplicate external egress and inconsistent candidate selection. | No retry, failover, or provider call from Grounding. | Low |
| G-17 | Legacy fallback response is regenerated and revalidated as self-healing behavior. | High | High in legacy path | Failure handling becomes hidden narration generation. | Keep deterministic fallback outside candidate Grounding; Grounding outputs decisions only. | Medium until legacy path is retired |
| G-18 | Provider-side memory introduces hidden context. | Critical | Medium | Unreviewed continuity and data leakage. | Provider threads, sessions, memory, retrieval, files, and embeddings forbidden. | Low after provider-profile approval |
| G-19 | Shadow context or hidden retrieval influences candidate. | Critical | Medium | Candidate cannot be deterministically grounded. | Trust one bound manifest only; reject unsupported claims. | Medium |
| G-20 | Audit metadata becomes a transcript store. | High | Medium | Compliance and leakage risk. | Bounded redacted reason metadata only; no content logging by default. | Low |
| G-21 | Delivery bypasses Grounding outcome. | Critical | Medium | Rejected narration reaches users. | Grounding acceptance required before persistence or Delivery. | Low after runtime evidence |
| G-22 | Competing legacy and modern activation paths remain available. | Critical | High | Policy bypass and inconsistent enforcement. | Isolate and retire legacy LLM activation path before modern activation. | Medium until retirement evidence exists |
| G-23 | Policy-version mismatch changes acceptance behavior. | High | Medium | Non-repeatable governance. | Bind contract, manifest, and prohibited-claims policy versions; reject mismatch. | Low |
| G-24 | Numeric pass-through is rounded, converted, or recombined. | High | Medium | Hidden calculation authority. | Exact upstream pass-through only; reject transformed values. | Low |
| G-25 | Sparse evidence language becomes stronger than upstream status. | High | Medium | Misleading certainty. | Validate required limitations and reject strengthening. | Low |

## Risk Decision

Current residual risk remains unacceptable for implementation or activation
because multiple high-severity observed runtime violations remain present.

