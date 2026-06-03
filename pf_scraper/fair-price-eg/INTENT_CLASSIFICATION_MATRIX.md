# ValorAI Intent Classification Matrix

Report date: 2026-06-01  
Scope: Phase 5.5C.1 deterministic rule set

## Intent Matrix

| Intent | Explicit high-confidence examples | Medium-confidence keywords | Example message |
| --- | --- | --- | --- |
| `VALUATION` | `fair price`, `price estimate`, `estimate the value`, `property valuation` | `valuation`, `valuate` | `What is the fair price for this property?` |
| `EXPLAINABILITY` | `explain the valuation`, `why this price`, `how was the price calculated`, `what drove the valuation` | `explain`, `price drivers`, `valuation drivers` | `Explain the valuation.` |
| `COMPARABLES` | `comparables`, `comparable properties`, `show comps`, `nearby listings`, `similar properties` | `comps`, `comparable`, `nearby` | `Show me nearby comparable properties.` |
| `FAIRNESS` | `is the asking price fair`, `price fair`, `priced fairly`, `fairness`, `fair market position` | `fairly priced`, `fair market` | `Is the asking price fair?` |
| `WHAT_IF` | `what if`, `add gym`, `add parking`, `add clubhouse`, `renovate`, `scenario`, `simulate` | `furnished`, `furnishing`, `modification`, `modify` | `What if I add a gym?` |
| `NEGOTIATION` | `negotiate`, `negotiation`, `counter offer`, `overpriced`, `underpriced`, `bargain` | `offer`, `asking price` | `Should I negotiate?` |
| `INVESTMENT` | `investment`, `invest`, `opportunity`, `worth buying`, `good investment` | None | `Is this a good investment?` |
| `MARKET_INSIGHT` | `market insight`, `area trend`, `compound trend`, `market activity`, `happening in`, `mivida` | `market`, `trend`, `activity`, `demand`, `supply` | `What is happening in Mivida?` |
| `PROPERTY_COMPARISON` | `compare these two properties`, `property comparison`, `side by side`, `difference between`, `better than`, `versus`, `vs` | None | `Compare these two properties.` |
| `GENERAL_QUESTION` | No fallback rules | No fallback rules | `Hello` |

## Clarification Matrix

| Condition | Intent | Confidence | Requires clarification |
| --- | --- | --- | --- |
| Governed explicit phrase matched | matched intent | `HIGH` | `false` |
| Governed broad keyword matched | matched intent | `MEDIUM` | `false` |
| No governed rule matched | `GENERAL_QUESTION` | `LOW` | `true` |
| Empty after normalization | `GENERAL_QUESTION` | `LOW` | `true` |

## Multi-Intent Matrix

| Message | Primary | Secondary |
| --- | --- | --- |
| `What is happening in Mivida and should I negotiate?` | `MARKET_INSIGHT` | `NEGOTIATION` |
| `Explain the valuation and show comparable properties.` | `EXPLAINABILITY` | `COMPARABLES` |
| `What if I add parking, and is this a good investment?` | `WHAT_IF` | `INVESTMENT` |

The primary intent is selected deterministically by:

```text
confidence
-> keyword specificity
-> matched-keyword count
-> first message position
-> fixed taxonomy precedence
```

A non-primary candidate is preserved as a secondary intent only when it is
safe: it has a `HIGH` confidence match or at least two governed keyword
matches.

## Explicit Misspelling Aliases

| Alias | Intent |
| --- | --- |
| `valution`, `valuaton` | `VALUATION` |
| `comparibles` | `COMPARABLES` |
| `rennovate` | `WHAT_IF` |
| `negociate` | `NEGOTIATION` |
| `investement` | `INVESTMENT` |
| `markit` | `MARKET_INSIGHT` |
| `comparision`, `comparsion` | `PROPERTY_COMPARISON` |

Aliases are explicit and auditable. No fuzzy or semantic classifier is used.
