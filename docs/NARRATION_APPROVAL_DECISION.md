# ValorAI Narration Approval Decision

Decision date: 2026-06-02  
Phase: 5.5C.6D Narration Contract Architecture  
Decision scope: Governance decision before Phase 5.5C.6E Prompt Assembly
Architecture  

## 1. Decision

```text
ARCHITECTURE_DECISION: CONDITIONAL_GO
PHASE_5_5C_6D_NARRATION_CONTRACT_ARCHITECTURE: APPROVABLE
PHASE_5_5C_6E_PROMPT_ASSEMBLY_ARCHITECTURE: NO_GO UNTIL REQUIRED APPROVALS
LLM_IMPLEMENTATION: NO_GO
LLM_RUNTIME_ACTIVATION: NO_GO
PRODUCTION_PROMOTION: NO_GO
```

## 2. Decision Reason

The narration contract architecture can preserve the locked rule:

```text
Planner decides.
Executor executes.
Composer computes.
Memory remembers.
LLM narrates.
```

It does so by limiting the LLM to exact pass-through narration of approved
deterministic facts, immutable citation references, and explicit evidence
limitations. It grants the LLM no authority to calculate, infer, predict,
recommend, rank, create evidence, or repair missing context.

## 3. Alternatives Considered

1. Permit one generic narration contract for all intents.
2. Permit model calculations when upstream values are cited.
3. Permit general real-estate answers through an LLM fallback.
4. Permit multi-intent narration by automatically merging contracts.
5. Permit LLM-friendly citation aliases.
6. Keep narration entirely disabled.

The first five alternatives are rejected because they create hidden authority
or ungrounded response surfaces. Keeping narration disabled remains an
acceptable operational fallback.

## 4. Risks

1. A model can phrase a new inference as if it were a summary.
2. Numeric pass-through can become accidental recomputation through rounding,
   conversion, or recombination.
3. Sparse evidence can be described with unjustified confidence.
4. Citation syntax can be misused to invent evidence.
5. Default-off intent configuration can drift toward broad activation.
6. Prompt Assembly architecture can accidentally introduce hidden side
   inputs.

## 5. Mitigations

1. Ground original unmodified candidate output deterministically.
2. Permit numeric repetition only as exact upstream pass-through.
3. Reject stronger language than the upstream evidence status permits.
4. Accept exact scoped citation tokens only.
5. Require per-intent default-off activation.
6. Keep general, clarification, unsupported, and multi-intent flows
   deterministic-only.
7. Review Prompt Assembly architecture separately in Phase 5.5C.6E.

## 6. Contract Decisions

| Contract | Decision | Scope |
| --- | --- | --- |
| `NARRATION_CONTRACT_ARCHITECTURE.md` | `CONDITIONAL_GO` | Global narration boundary. |
| `VALUATION_NARRATION_CONTRACT.md` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | Upstream valuation narration only. |
| `EXPLAINABILITY_NARRATION_CONTRACT.md` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | Upstream explanation narration only. |
| `COMPARABLES_NARRATION_CONTRACT.md` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | Received comparable evidence narration only. |
| `FAIRNESS_NARRATION_CONTRACT.md` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | Router-owned fairness narration only. |
| `WHAT_IF_NARRATION_CONTRACT.md` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | Tool 5 output narration only. |
| `NEGOTIATION_NARRATION_CONTRACT.md` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | Tool 6 output narration only. |
| `INVESTMENT_NARRATION_CONTRACT.md` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | Tool 7 output narration only. |
| `MARKET_INSIGHT_NARRATION_CONTRACT.md` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | Tool 8 descriptive output narration only. |
| `PROPERTY_COMPARISON_NARRATION_CONTRACT.md` | `CONDITIONALLY_ELIGIBLE_DEFAULT_OFF` | Composer-owned neutral comparison narration only. |
| `NARRATION_PROHIBITED_CLAIMS_MATRIX.md` | `APPROVABLE` | Normative generated-claim prohibitions. |
| `NARRATION_ACTIVATION_POLICY.md` | `CONDITIONAL_GO` | Default-off activation policy. |

## 7. Minimum Required Narration-Governance Approvals Before Phase 5.5C.6E

Prompt Assembly Architecture may begin only after explicit approval of:

1. Exact pass-through narration as the maximum LLM authority.
2. The global Narration Contract Architecture.
3. All nine intent-specific narration contracts.
4. The Prohibited Claims Matrix.
5. Default-off per-intent activation.
6. Deterministic-only treatment for `GENERAL_QUESTION`, clarification,
   unsupported, and multi-intent flows.
7. Immutable, pass-through-only, non-generated citations.
8. Legal citation syntax using exact received IDs only.
9. Sparse evidence language.
10. Insufficient evidence language.
11. Partial-success language.
12. Failure and deterministic fallback language.
13. Original-output grounding requirements.
14. Narration rejection conditions.
15. The rule that Phase 5.5C.6E is architecture-only and cannot activate or
    implement an LLM runtime.

## 8. Phase Boundary

Approval of Phase 5.5C.6D permits only Phase 5.5C.6E Prompt Assembly
Architecture review. It does not permit code, prompts, APIs, schemas,
providers, tests, validators, patches, runtime wiring, legacy-runtime
activation, or production promotion.

## 9. Final Verdict

```text
ARCHITECTURE_DECISION: CONDITIONAL_GO
NEXT_ALLOWED_PHASE_AFTER_EXPLICIT_APPROVAL: PHASE 5.5C.6E PROMPT ASSEMBLY ARCHITECTURE
```
