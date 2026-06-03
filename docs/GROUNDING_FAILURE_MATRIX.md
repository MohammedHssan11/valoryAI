# ValorAI Grounding Failure Matrix

Review date: 2026-06-02  
Phase: 5.5C.6H Grounding Architecture Review  
Status: Architecture only  

## Failure Principle

Grounding failure is fail-closed. No failure may trigger repair, provider
retry, failover, prompt reassembly, partial narration delivery, or accepted
memory persistence.

## Complete Failure Matrix

| Failure condition | Grounding outcome | Provider called again | Narration delivered | Accepted-memory persistence | Deterministic fallback |
| --- | --- | --- | --- | --- | --- |
| Fabricated citation | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| Citation alias or modified token | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| Missing required citation | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| Extra unsupported citation | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| Foreign-tenant citation | `ACCESS_DENIED` | No | No | No | No scoped fallback |
| Cross-workspace citation | `ACCESS_DENIED` | No | No | No | No scoped fallback |
| Unsupported claim | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| Hidden calculation | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| New forecast or prediction | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| New ranking, recommendation, or winner declaration | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| Invented evidence or assumption | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| Missing evidence repaired by provider | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| Malformed candidate | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| Unknown candidate field | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| Provider hallucination | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| Invalid narration contract | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| Contract merge or generic substitution | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| Policy-version mismatch | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| Grounding ambiguity | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| Missing grounding manifest | `REJECT_NARRATION` | No | No | No | Allowed when authorization remains valid |
| Manifest and candidate binding mismatch | `ACCESS_DENIED` when scope trust is lost; otherwise `REJECT_NARRATION` | No | No | No | No scoped fallback for `ACCESS_DENIED` |
| Foreign tenant, workspace, scenario, or session binding | `ACCESS_DENIED` | No | No | No | No scoped fallback |
| `GENERAL_QUESTION` candidate reaches Grounding | `REJECT_NARRATION` | No | No | No | Deterministic-only behavior |
| Multi-intent candidate reaches Grounding without approved combined contract | `REJECT_NARRATION` | No | No | No | Deterministic-only behavior |

## Output Rule

Grounding emits a decision and bounded reason categories only. It emits no
replacement candidate.

## Forbidden Failure Handling

Grounding must never:

1. Remove an unsupported sentence and deliver the rest.
2. Replace a hallucinated value with an upstream value.
3. Add a missing citation.
4. Ask the same provider for a repair.
5. Ask another provider for a repair.
6. Reassemble a prompt.
7. Retrieve more evidence.
8. Recompute a value.
9. Persist rejected content as accepted memory.

