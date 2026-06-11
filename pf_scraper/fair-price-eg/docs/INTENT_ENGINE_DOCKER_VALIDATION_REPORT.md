# ValorAI Intent Engine Docker Validation Report

Report date: 2026-06-01  
Validator: `scripts/validate_intent_engine.ps1`  
Decision: **GO**

## Validation Scope

Executed against:

```text
Real backend Docker image
Docker network disabled
Real rule definitions
Real IntentResult contract
Real normalization logic
Real deterministic precedence logic
Real multi-intent logic
Real clarification fallback
Real source-boundary scan
Real latency loop
```

Explicitly absent:

```text
PostgreSQL
PostGIS
Router
CMT
ML
OpenAI
Gemini
Anthropic
Embeddings
Vector database
External services
```

## Command

```powershell
.\scripts\validate_intent_engine.ps1
```

The script executes:

```text
docker build --tag valorai-intent-engine-validation:phase-5-5c-1 ./backend
docker run --rm --network none \
  valorai-intent-engine-validation:phase-5-5c-1 \
  python -m app.scripts.validate_intent_engine
```

## Result

```text
image:                       valorai-intent-engine-validation:phase-5-5c-1
network_mode:                none
database_dependency:        false
router_dependency:          false
ml_dependency:              false
cmt_dependency:             false
classified_intent_count:    10
failed_cases:               []
multi_intent_primary:       MARKET_INSIGHT
multi_intent_secondary:     [NEGOTIATION]
clarification_intent:       GENERAL_QUESTION
clarification_confidence:   LOW
clarification_required:     true
misspelling_and_noise_intent: NEGOTIATION
deterministic_output_count: 1
forbidden_references:       0
forbidden_imports:          0
average_latency_ms:         0.042005
latency_target_ms:          5
latency_target_passed:      true
standalone_validation:      PASS
```

## Intent Coverage

The Docker validator classifies one real example for every approved intent:

```text
VALUATION
EXPLAINABILITY
COMPARABLES
FAIRNESS
WHAT_IF
NEGOTIATION
INVESTMENT
MARKET_INSIGHT
PROPERTY_COMPARISON
GENERAL_QUESTION
```

## Multi-Intent Evidence

Input:

```text
What is happening in Mivida and should I negotiate?
```

Result:

```text
primary:   MARKET_INSIGHT
secondary: NEGOTIATION
```

## Clarification Evidence

Input:

```text
Tell me more
```

Result:

```text
intent:                 GENERAL_QUESTION
confidence:             LOW
requires_clarification: true
```

## Negative Boundary Evidence

The validator parses every Python file in:

```text
backend/app/copilot/orchestrator/intents
```

Allowed imports are standard-library modules plus package-relative contracts.
It rejects forbidden source references including:

```text
openai
gemini
anthropic
catboost
sklearn
transformers
embedding
vector
sqlalchemy
requests
httpx
socket
```

Result:

```text
forbidden_source_references: 0
forbidden_imports:           0
```

## Latency Evidence

The container runs `20,000` classifications of:

```text
What is happening in Mivida and should I negotiate?
```

Measured average:

```text
0.042005 ms
```

Target:

```text
< 5 ms average
```

Result:

```text
PASS
```

## Environment Independence

The Docker run uses:

```text
--network none
```

No Compose services are started. No database container, Router request,
Tool Layer request, model file, or external endpoint is required.

## Remaining Risks

1. New vocabulary requires explicit governed rule additions.
2. The standalone engine is intentionally not wired into later orchestrator
   phases yet.
3. The broader backend suite still contains unrelated stale pricing-route
   tests.

## GO / NO-GO

**GO for Intent Engine Docker validation.**

Intent Engine V1 works inside Docker with no network and no infrastructure
dependencies while meeting the deterministic governance and latency targets.
