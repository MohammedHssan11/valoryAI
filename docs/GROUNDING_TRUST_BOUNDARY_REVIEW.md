# ValorAI Grounding Trust Boundary Review

Review date: 2026-06-02  
Phase: 5.5C.6H Grounding Architecture Review  
Status: Architecture only  

## Grounding Position

Grounding sits after Candidate Parser and before optional Memory-owned
accepted-narration commit and Delivery.

Its position is security-critical:

1. External provider output has already arrived.
2. No candidate narration is yet trusted.
3. No candidate narration may persist or reach users before acceptance.

## Trust Matrix

| Artifact or layer | Trust level | Grounding treatment |
| --- | --- | --- |
| Provider | Untrusted external processor | Never trusted as an authority source. |
| Provider response | Untrusted | Preserve original response linkage; validate parsed candidate without repair. |
| Candidate Parser | Conditionally trusted boundary | Trusted only to parse and preserve, never to repair or enrich. |
| Prompt Assembly | Conditionally trusted boundary | Trusted only to serialize admitted provider-safe context. Its output is not truth. |
| Narration Admission Gate | Trusted deterministic policy firewall | Grounding trusts only request-bound attestations and manifest versions. |
| Narration contracts | Trusted normative policy | Exactly one approved version must apply. |
| Prohibited-claims matrix | Trusted normative policy | Applies to every candidate. |
| Composer | Trusted upstream arithmetic owner | Grounding validates manifest-exposed Composer facts; it does not recompute them. |
| Memory | Trusted upstream memory owner | Grounding does not retrieve or reinterpret Memory. |
| Immutable citation package | Trusted only when bound and scoped | Validate exact candidate references only. |
| Grounding | Narrow acceptance authority | Validate or reject only. |
| Optional post-generation Memory commit | Downstream trusted owner when separately approved | May receive accepted grounded narration only. |
| Delivery | Downstream trusted transport owner | Must honor Grounding outcome and never override rejection. |

## Trust Boundary Rules

1. Trust never flows backward from the provider.
2. Prompt compliance is not enforcement.
3. Schema compliance is not grounding.
4. Citation syntax is not citation validity.
5. Deterministic fallback is not repaired provider narration.
6. A rejected candidate remains rejected.
7. `ACCESS_DENIED` permits no scoped disclosure.
8. No layer may override Grounding acceptance or rejection.

## Forbidden Trust Shortcuts

Grounding must reject architectures that:

1. Trust structured provider output automatically.
2. Trust prompt instructions as sufficient enforcement.
3. Trust a citation because its syntax looks valid.
4. Trust a candidate after overwriting its values.
5. Trust a generic contract for modern intents.
6. Trust provider-side memory.
7. Trust hidden retrieval.
8. Trust legacy fallback regeneration as Grounding.

## Forensic Finding

The observed runtime overwrites parsed authoritative values before validation
and relies on incomplete legacy checks. That is hidden provider trust and
repair behavior. It is `NO_GO`.

