# ValorAI Grounding Determinism Review

Review date: 2026-06-02  
Phase: 5.5C.6H Grounding Architecture Review  
Status: Architecture only  

## Decision

Grounding must be:

| Property | Decision | Consequence |
| --- | --- | --- |
| Deterministic | `REQUIRED` | Same governed inputs and policy versions produce the same decision. |
| Repeatable | `REQUIRED` | Re-evaluation cannot change outcome without an input or policy-version change. |
| Restart-stable | `REQUIRED` | Process restart cannot change outcome. |
| Provider-independent | `REQUIRED` | Provider identity cannot change acceptance rules. |
| No-I/O | `REQUIRED` | No database, Tool, provider, Memory, or external retrieval call may influence evaluation. |
| Fail-closed | `REQUIRED` | Ambiguity rejects narration. |

## Deterministic Inputs

Grounding decision depends only on:

1. Original parsed candidate narration linked to preserved original response.
2. One bound internal grounding manifest.
3. One immutable scoped citation package.
4. One approved intent contract version.
5. One approved prohibited-claims policy version.
6. Bounded assembly and binding attestations.

## Deterministic Outputs

Grounding emits:

1. One outcome: `ACCEPT_NARRATION`, `REJECT_NARRATION`, or `ACCESS_DENIED`.
2. Bounded reason categories.
3. Checked policy versions.
4. Bounded redacted audit metadata.

## Forbidden Sources of Nondeterminism

Grounding must not depend on:

1. Provider retries.
2. Provider failover.
3. Model-based review.
4. Human-in-the-loop review during request execution.
5. Random sampling.
6. Current time except prevalidated request-bound attestations.
7. Database state fetched during validation.
8. Hidden retrieval.
9. Network availability.
10. Prompt reassembly.
11. Candidate repair.
12. Previous Grounding outcome.

## Ambiguity Rule

If deterministic validation cannot decide whether a claim is legal exact
pass-through narration, Grounding returns `REJECT_NARRATION`.

## Restart Stability

Restart stability means:

1. The same candidate and manifest remain the same decision.
2. No process-local state changes policy.
3. No provider-specific heuristic changes policy.
4. No retrieved state changes policy after candidate generation.

## Forensic Finding

Observed legacy fallback regeneration and revalidation behavior must not
define the modern Grounding boundary. It creates a self-healing pattern
outside the required decision-only model.

