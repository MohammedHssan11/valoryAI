# ValorAI Project Master State V2

Authoritative rebuild date: 2026-06-02  
Repository scope: `pf_scraper/fair-price-eg` plus repository-level data tooling  
Governance rule: **CODE > REPORTS > OLD MASTER STATE**

## 1. Executive Summary

ValorAI is an implemented governed real-estate intelligence platform with a
deterministic truth layer, conditional CMT/ML routing, structured
explainability, monitoring, PostgreSQL/PostGIS persistence, JWT-scoped Copilot
memory, and a React/Vite frontend.

The latest completed named phase is **Phase 5.5C.5: Memory Integration**. The
Valuation, Explainability, Comparable, Fairness, What-if, Negotiation, Investment, and Market Insight Tools are
implemented as authenticated, tenant-isolated adapters that preserve Truth
Layer authority. Tool 5 evaluates ephemeral scenario overlays without
mutating the base property or an existing scenario. Tool 6 builds broker-grade
negotiation guidance by orchestrating Tools 1-5. Its offer-band endpoints are
limited to the TruthLayer fair price and returned comparable prices; its
positions, talking points, risks, and optional What-if sensitivity evidence
are traceable. Tool 7 builds evidence-backed opportunity analysis over the
Tool 6 package without generating forecasts, returns, or independent prices.
Tool 8 builds traceable descriptive observations over persisted TruthLayer
snapshots, prediction logs, shadow logs, comparable evidence, workspace
history, and tool events without generating forecasts or synthetic trends.
The Broker Adapter uses Tool 1 and Tool 2 rather than calling
pricing routes directly. Tool snapshots, tool events, and broker sessions
survive restart validation.
The Copilot Orchestrator now has a standalone deterministic rule-based Intent
Engine V1 for the approved ten-intent taxonomy. It returns auditable primary
and secondary intents with explicit clarification behavior and does not call
Tools, databases, models, or external services.
The standalone deterministic Tool Planner converts `IntentResult` into an
auditable `ExecutionPlan`. It maps only the approved Tools 1-8, blocks Tool
selection for clarification plans, represents property comparison as two
parallel Tool 1 invocation slots, and does not execute Tools or access
infrastructure.
The standalone deterministic Tool Executor consumes `ExecutionPlan`, invokes
only the approved Tools 1-8 through the existing tenant-scoped Tool Layer,
supports sequential and parallel execution, preserves raw Tool payloads,
isolates failures and timeouts, and returns auditable `ExecutionResult`
metadata. It contains no Response Composer, comparison arithmetic, evidence
summarization, payload compression, or LLM logic.
The standalone deterministic Response Composer consumes only extended
`ExecutionResult`, normalizes approved Tool 1-8 payloads, calculates governed
property-comparison and comparable-evidence arithmetic, preserves received
citations, and emits bounded `compressed_context` plus complete frontend-safe
`frontend_payload`. It does not receive `ExecutionPlan`, access databases,
execute Tools, integrate memory, create transport wrappers, or call LLMs.
The standalone deterministic Memory Integration layer receives scoped
workspace, optional scenario, optional broker-session, `ExecutionResult`, and
`ComposedResponse` context. It writes one idempotent bounded Composer summary
into existing `decision_history`, rebuilds a governed `MemoryContext` from
existing PostgreSQL persistence only, preserves received and persisted
citations, and emits a content-derived restart-stable `memory_id`. It adds no
new table, vector database, embedding dependency, model call, narration,
prompt building, or frontend transport.

Phase 5.5C.6 LLM Integration is implemented as the single authorized
`COPILOT_ORCHESTRATOR_LLM_V1` narration pipeline after Memory Integration.
The legacy broker LLM runtime, legacy Gemini adapter, legacy OpenAI adapter,
and rejected attempted modern implementation were retired. The implemented
pipeline contains a deterministic Narration Admission Gate, deterministic
Prompt Assembly, a fixed stateless Gemini 2.5 Pro Provider Adapter, strict
Candidate Parser, deterministic fail-closed Grounding Layer, and fallback
handoff to the Composer-owned frontend payload. The LLM may narrate exact
approved upstream facts only. It may not decide, execute, compute, remember,
create citations, rank, forecast, recommend, repair evidence, or become a
provider-side memory system. Activation remains default-off and per-intent.
Phase 5.5C.RUNTIME.1 activates one authenticated modern Copilot transport at
`POST /v1/copilot/orchestrator/respond`. The transport sequences the approved
components only, keeps provider invocation default-off, returns the
Composer-owned deterministic payload when narration is not admitted, and
redacts scoped delivery metadata on access denial.

The system is staging-grade, not fully production-ready. The repaired Broker
Adapter, JWT ownership layer, tenant isolation, durable broker sessions, and
Tool Layer have fresh Docker validation. React frontend JWT/context integration
for P0-1 is now implemented through Firebase Authentication, backend token
exchange, browser-session ValorAI JWT restore, bearer-header injection, 401
recovery, and protected routes. Direct valuation authentication policy,
managed secrets, RBAC, and regression test drift remain production-promotion
blockers.

## Sprint 1 React Authentication Update - 2026-06-10

Status: SPRINT 1 COMPLETE. P0-1 CLOSED.

React is now a first-class authenticated client for protected backend APIs:

- Firebase web sign-in/sign-up/reset is wired through the React frontend.
- React posts Firebase ID tokens to `POST /v1/auth/token-exchange`.
- React stores the returned ValorAI JWT and user metadata for browser-session restore.
- Axios automatically injects `Authorization: Bearer <jwt>`.
- Broker SSE streaming injects the same bearer token for its direct `fetch` path.
- 401 responses renew once and retry; repeated failure expires the session.
- App-shell routes are protected with loading, login, logout, expired-session, and access-denied states.

Broker request contract mismatch was closed in Sprint 2. Backend pytest collection repairs remain a separate P0 item and were not changed in Sprint 2.

## 2. Current Project State

| Area | Current status |
| --- | --- |
| Truth Layer | Implemented |
| Conditional Router | Implemented |
| CMT engine | Implemented |
| ML CatBoost engine | Implemented |
| Explainability | Implemented |
| Monitoring and shadow logging | Implemented |
| JWT authentication | Implemented for Copilot and Broker APIs |
| Copilot persistence | Implemented |
| Tenant isolation | Implemented at API and database boundaries |
| Broker session recovery | Implemented |
| Copilot Tool 1: Valuation | Implemented |
| Copilot Tool 2: Explainability | Implemented |
| Copilot Tool 3: Comparable | Implemented |
| Copilot Tool 4: Fairness | Implemented |
| Copilot Tool 5: What-if | Implemented |
| Copilot Tool 6: Negotiation | Implemented |
| Copilot Tool 7: Investment | Implemented |
| Copilot Tool 8: Market Insight | Implemented |
| Copilot Orchestrator Intent Engine V1 | Implemented and Docker-validated without network or infrastructure dependencies |
| Copilot Orchestrator Tool Planner | Implemented and Docker-validated without network or infrastructure dependencies |
| Copilot Orchestrator Tool Executor | Implemented and Docker-validated against real PostgreSQL/PostGIS, JWT-created tenant state, and Tools 1-8 |
| Copilot Orchestrator Response Composer | Implemented and Docker-validated against real PostgreSQL/PostGIS, Tool Executor output, restart replay, and the `< 15 ms` overhead target |
| Copilot Orchestrator Memory Integration | Implemented and Docker-validated against existing persistence, tenant isolation, backend restart, PostgreSQL restart, container recreation, governed compression, and the `< 25 ms` overhead target |
| Phase 5.5C.6 LLM Integration implementation | Implemented and Docker-validated as one narration-only Copilot Orchestrator pipeline |
| Phase 5.5C.6 Narration Admission Gate | Implemented; deterministic no-I/O fail-closed policy firewall |
| Phase 5.5C.6 Prompt Assembly | Implemented; deterministic bounded representation-only assembly |
| Phase 5.5C.6 Gemini Provider Adapter | Implemented; fixed stateless Gemini 2.5 Pro one-shot transport, default-off |
| Phase 5.5C.6 Candidate Parser | Implemented; strict original-output parsing without repair |
| Phase 5.5C.6 Grounding Layer | Implemented; original-candidate exact-fact and immutable-citation validation |
| Phase 5.5C.6 runtime activation | Default-off and explicit per-intent only |
| Phase 5.5C.RUNTIME.1 orchestrator transport activation | Implemented and Docker-validated at `POST /v1/copilot/orchestrator/respond`; live Gemini traffic remains default-off |
| Frontend JWT/workspace integration | Not implemented |
| Broker valuation-backed orchestration | Implemented and Docker-validated through Tool Layer |
| Production deployment | Not complete |

Current implemented baseline: **through Phase 5.5C.RUNTIME.1**.  

### Current Active Phase

Phase 5.5C.RUNTIME.1 transport activation is complete and Docker-validated.
Narration is default-off and explicit per-intent activation remains required.
Production-hardening work remains active in parallel.

## 3. Current Production Architecture

The institutional architecture is:

```text
User
  -> JWT Authentication
  -> Broker Copilot
  -> Tool Layer
  -> Truth Layer
  -> Conditional Router
  -> ML OR CMT
  -> Explainability
  -> Monitoring
  -> Persistence
  -> Audit Trail
```

Implemented runtime detail:

```text
Authenticated Copilot Tool request
  -> JWT subject provisioning
  -> tenant-scoped workspace/property/scenario lookup
  -> CopilotToolsService
  -> Truth Layer Router
  -> CMT retrieval first
  -> conditional CMT or ML selection with fallback
  -> structured explainability
  -> valuation_snapshots + tool_events
```

Tools 3 and 4 extend that runtime:

```text
Comparable Tool
  -> existing tenant-scoped snapshot OR Valuation Tool
  -> stored Router comparable evidence
  -> normalized real-evidence response

Fairness Tool
  -> Valuation Tool with target_price_egp
  -> existing Router fairness explanation
  -> normalized fairness response
```

Tool 5 extends that runtime:

```text
What-if Tool
  -> current property OR existing scenario lineage
  -> ephemeral scenario overlay
  -> fresh Valuation Tool evaluation for current state
  -> fresh Valuation Tool evaluation for sandbox state
  -> Explainability Tool + Comparable Tool + Fairness Tool
  -> TruthLayer-derived delta aggregation
  -> persisted what_if tool event
```

Tool 6 extends that runtime:

```text
Negotiation Tool
  -> current property OR existing scenario lineage
  -> Valuation Tool with asking_price_egp as TruthLayer target
  -> Explainability Tool for the same valuation snapshot
  -> Comparable Tool for the same valuation snapshot
  -> Fairness Tool for the same valuation snapshot
  -> optional What-if Tool sensitivity analysis
  -> traceable negotiation position, offer band, talking points, and risks
  -> persisted negotiation tool event
```

Tool 7 extends that runtime:

```text
Investment Tool
  -> current property OR existing scenario lineage
  -> Negotiation Tool
  -> Tools 1-5 evidence chain through Tool 6
  -> explicit investment position, strengths, risks, and summaries
  -> optional What-if sensitivity evidence OR Insufficient Evidence
  -> persisted investment tool event
```

Current Broker flow:

```text
Broker Chat
  -> Broker Adapter
  -> Valuation Tool
  -> Explainability Tool
  -> Response Builder
  -> User
```

One qualification is mandatory:

1. Direct valuation endpoints currently expose the Router without JWT.

## 4. System Layers

| Layer | Implementation | Status |
| --- | --- | --- |
| Data collection | PropertyFinder Egypt scraper and JSONL/CSV tooling | Implemented, operational maturity not audited |
| Dataset layer | Cleaned datasets, `dataset_v3`, hybrid research artifacts | Implemented |
| Truth Layer | Deterministic CMT valuation, guardrails, MAD filtering, weights, confidence | Implemented |
| ML layer | CatBoost residential rent/sale inference with SHAP contributions | Implemented |
| Router layer | Comparable-density and exposure-aware CMT/ML selection with fallback | Implemented |
| Explainability layer | Router, confidence, fairness, narrative, comparable and feature-driver output | Implemented |
| Monitoring layer | Prediction logs, shadow logs, in-process metrics, health and SLO snapshots | Implemented for staging |
| Copilot memory layer | Workspaces, chats, messages, properties, scenarios, assumptions, lineage | Implemented |
| Tool layer | Copilot valuation, explainability, comparable, fairness, what-if, negotiation, investment, and market-insight adapters | Tools 1-8 complete and operational |
| Existing broker layer | Transitional intent, plan, Tool Layer adapter, context, narration, grounding, governance, SSE | Repaired Tool 1 and Tool 2 valuation and explainability flow Docker-validated; not an approved Phase 5.5C.6 modern LLM path |
| Persistence layer | PostgreSQL/PostGIS plus deterministic migrations `000`-`007` | Implemented |
| Frontend layer | React/Vite screens, evidence UX, broker terminal, local Zustand continuity | Implemented with auth/context gap |

## 5. Historical Architecture Evolution

| Era | Architecture |
| --- | --- |
| Data foundation | Scraper -> cleaning -> dataset builder -> CatBoost baseline |
| Deterministic valuation | PostGIS comparables -> guardrails -> MAD -> weights -> fair price -> confidence |
| Router evolution | CMT retrieval -> exposure/comparable rules -> CMT or ML -> fallback |
| Explainability evolution | Deterministic traces plus ML SHAP feature contributions |
| Broker evolution | Deterministic broker registry -> grounded narration -> SSE reasoning terminal |
| Copilot evolution | JWT tenant boundary -> durable memory -> lineage/audit -> Tool adapters |

The earlier Hybrid AVM roadmap is historical. It is not the current active
architecture.

## 6. Phase Completion History

| Phase | Status | Result |
| --- | --- | --- |
| Data phases 1, 2, 2.5, 3, 3.5, 3.6 | Complete | Data audit, ETL hardening, CatBoost baseline, deduplication |
| Phase 3A.1b and 3B | Complete | Geospatial governance and visual evidence UX |
| Phase 5.1 | Implemented | Optimized conditional Router rules |
| Phase 5.2 | Implemented | Master Router orchestration |
| Phase 5.3A | Implemented | Shadow execution |
| Phase 5.3B | Implemented | Prediction logging |
| Phase 5.4 | Implemented | Structured explainability and ML SHAP path |
| Phase 5.5A | Complete | Broker Copilot architecture discovery |
| Phase 5.5B.1 | Complete | Copilot persistence layer |
| Phase 5.5B.1R | Complete | Persistence recovery and hardening |
| Phase 5.5B.1R.1 | Complete | Production blockers resolution |
| Phase 5.5B.2 | Complete | Valuation and explainability Tool adapters |
| Phase 5.5B.2A | Complete | Broker Adapter repaired: direct pricing route usage removed; Tool 1 and Tool 2 flow Docker-validated |
| Phase 5.5B.3 | Complete | Comparable and Fairness Tool adapters; real CMT evidence, Router-owned fairness, scenario support, tenant isolation, audit persistence, and restart recovery Docker-validated |
| Phase 5.5B.4 | Complete | What-if Tool deterministic sandbox orchestration; immutable base state, scenario-on-scenario overlays, TruthLayer-derived deltas, assumptions disclosure, fresh comparable and fairness evaluation, tenant isolation, audit persistence, and restart recovery Docker-validated |
| Phase 5.5B.5 | Complete | Negotiation Tool deterministic orchestration; five traceable positions, grounded offer bands, evidence-backed talking points and risks, optional What-if sensitivity analysis, tenant isolation, audit persistence, and restart recovery Docker-validated |
| Phase 5.5B.6 | Complete | Investment Tool deterministic orchestration; five traceable opportunity positions, evidence-backed strengths and risks, optional What-if sensitivity evidence, tenant isolation, audit persistence, and restart recovery Docker-validated |
| Phase 5.5B.7 | Complete | Market Insight Tool persisted descriptive analytics; snapshot, prediction-log, shadow-log, comparable, workspace-history, and tool-event grounding; compound, area, property-type, historical, confidence, audit, tenant-isolation, and restart recovery Docker-validated |
| Phase 5.5C.1 | Complete | Rule-based Intent Engine V1; approved ten-intent taxonomy, deterministic audit output, multi-intent support, clarification fallback, explicit misspelling aliases, zero LLM/ML/external-service dependencies, and network-disabled Docker validation |
| Phase 5.5C.2 | Complete | Deterministic Tool Planner; approved intent-to-Tool map, content-derived plan IDs, sequential and parallel plans, clarification blocking, two-Tool-1 property comparison planning, multi-intent planning, zero execution or infrastructure dependencies, and network-disabled Docker validation |
| Phase 5.5C.3 | Complete | Deterministic Tool Executor; approved Tool 1-8 dispatch, isolated per-call sessions, sequential and parallel execution, raw payload preservation, clarification blocking, timeout handling, partial-failure isolation, tenant isolation, audit metadata, restart recovery, and real Docker/PostGIS validation |
| Phase 5.5C.4B | Complete | Deterministic Response Composer; extended ExecutionResult intent metadata, strict Tool 1-8 normalization, reduced Property Comparison V1, approved arithmetic offload, citation pass-through, governed Top-3 compression, dual structured channels, failure semantics, restart-stable response IDs, and real Docker/PostGIS validation |
| Phase 5.5C.5 | Complete | Deterministic Memory Integration; existing persistence only, idempotent bounded Composer audit summary, tenant-scoped MemoryContext rebuild, governed history limits, citation preservation, content-derived memory IDs, fail-closed access handling, backend restart, PostgreSQL restart, container recreation, and real Docker/PostGIS validation |
| Phase 5.5C.6A | Architecture forensic audit complete: `NO-GO` | Unauthorized attempted LLM paths rejected for persistence, citation, tenant-binding, grounding, provider, and runtime-boundary violations. |
| Phase 5.5C.6B | Formal architecture review complete: `CONDITIONAL_GO` | Narration-only target architecture defined after Memory Integration; implementation continuation, runtime activation, and production promotion remain gated. |
| Phase 5.5C.6D | Narration contract architecture complete: `CONDITIONAL_GO` | Exact pass-through narration only; immutable citations; prohibited-claims matrix; nine intent-specific contracts; default-off activation; general-question, clarification, unsupported, and multi-intent flows remain deterministic-only. |
| Phase 5.5C.6F | Narration Admission Gate architecture complete: `CONDITIONAL_GO` | Deterministic no-I/O fail-closed policy firewall defined with `ADMIT_NARRATION`, `DETERMINISTIC_ONLY`, `REJECT_NARRATION`, and `ACCESS_DENIED`. |
| Phase 5.5C.6G | Provider Adapter architecture complete: `CONDITIONAL_GO` | Stateless minimized provider-neutral transport boundary defined; automatic retry and transparent failover forbidden by default; provider-side memory and pre-grounding delivery forbidden. |
| Phase 5.5C.6 | Complete | One default-off `COPILOT_ORCHESTRATOR_LLM_V1` pipeline; legacy-path retirement, Admission Gate, bounded Prompt Assembly, stateless Gemini 2.5 Pro adapter, strict Candidate Parser, deterministic Grounding, fallback handoff, tenant isolation, citation rejection, fail-closed transport, backend restart, and PostgreSQL restart Docker-validated. |
| Phase 5.5C.RUNTIME.1 | Complete | One authenticated modern Copilot endpoint sequences Intent Engine through governed delivery; valuation, Property A/B comparison, Tool 6, Tool 7, Tool 8, clarification, access denial, fake citation, fake value, fake prediction, backend restart replay, and PostgreSQL restart replay Docker-validated. |

Phases 5.1-5.4 are code-derived because standalone reports were not found.
Phases 5.5B.1R, 5.5B.1R.1, 5.5B.2, 5.5B.2A, 5.5B.3, 5.5B.4, 5.5B.5, 5.5B.6, 5.5B.7, 5.5C.1, 5.5C.2, 5.5C.3, 5.5C.4B, and 5.5C.5 also
have repository reports. Phase 5.5C.6A, 5.5C.6B, 5.5C.6D, 5.5C.6F, and
5.5C.6G remain the architecture-governance history that preceded the completed
Phase 5.5C.6 implementation.

### Phase 5.5B.2A: Broker Adapter Repair

Status: **COMPLETE**

Summary:

- Legacy Broker Adapter no longer calls pricing routes directly.
- Direct pricing route usage was eliminated from the Broker Adapter path.
- Broker flow migrated to the Tool Layer.
- Broker now uses the Valuation Tool and Explainability Tool.
- Truth Layer remains authoritative.
- Docker validation passed.
- Restart recovery passed.
- Tenant isolation passed.

### Phase 5.5B.3: Comparable And Fairness Tools

Status: **COMPLETE**

Summary:

- Tool 3 retrieves real comparable evidence from tenant-scoped valuation
  snapshots or invokes Tool 1 for a fresh Router-backed snapshot.
- Tool 4 invokes Tool 1 with `target_price_egp` and returns the existing Router
  fairness explanation.
- Tool Layer pricing calculations, synthetic comparables, and direct CMT/ML
  calls remain absent.
- The previous fabricated comparable `listing_date = "Recent"` marker was
  removed.
- Scenario overlays, JWT tenant isolation, tool-event persistence, backend
  restart recovery, PostgreSQL restart recovery, PostGIS integration, and
  adjacent Docker regressions passed.

### Phase 5.5B.4: What-if Tool

Status: **COMPLETE**

Summary:

- Tool 5 is a deterministic orchestration adapter over existing TruthLayer
  tools. It contains no independent pricing logic and does not call the
  Router, ML, or CMT directly.
- The sandbox applies an in-memory overlay over the base property or an
  existing scenario lineage. It never mutates persisted base property or
  scenario state.
- Supported overlays include size, bedrooms, bathrooms, furnishing,
  finishing, governed amenities, parking, gym, clubhouse, location,
  property type, and property category inputs.
- The response aggregates fresh valuation, explainability, comparable, and
  fairness results with TruthLayer-derived `delta_value` and
  `delta_percentage`.
- Missing tracked scenario facts are disclosed through `assumptions_used`
  rather than silently asserted.
- Scenario-on-scenario overlays, JWT tenant isolation, durable `what_if`
  audit events, backend restart recovery, PostgreSQL restart recovery,
  PostGIS integration, and adjacent Docker regressions passed.

### Phase 5.5B.5: Negotiation Tool

Status: **COMPLETE**

Summary:

- Tool 6 is a deterministic orchestration adapter over existing TruthLayer
  tools. It contains no independent pricing logic and does not call the
  Router, ML, or CMT directly.
- It orchestrates Valuation, Explainability, Comparable, and Fairness for the
  same tenant-scoped valuation snapshot, with optional What-if sensitivity
  analysis.
- All five permitted negotiation positions are implemented:
  `Strong Buy Opportunity`, `Negotiation Recommended`, `Fair Market
  Position`, `Premium Justified`, and `Overpriced`.
- Recommended offer-band endpoints are limited to authoritative `fair_price`
  and returned comparable prices. The Tool does not generate discounts,
  synthetic comparable prices, or hidden pricing formulas.
- Positions, offer bands, broker talking points, and risk notes carry
  structured evidence references.
- Scenario negotiation, comparable grounding, fairness grounding, optional
  What-if integration, JWT tenant isolation, durable `negotiation` audit
  events, backend restart recovery, PostgreSQL restart recovery, PostGIS
  integration, and adjacent Docker regressions passed.

### Phase 5.5B.6: Investment Tool

Status: **COMPLETE**
Decision: **GO**

```text
Phase 5.5B.6
Investment Tool

Status: COMPLETE

Decision: GO

Evidence-backed investment assessment implemented.

No financial forecasting.

No ROI generation.

TruthLayer authority preserved.

Docker validation passed.

Tenant isolation passed.

Audit persistence passed.
```

Summary:

- Tool 7 is a deterministic orchestration adapter over the existing Tool 6
  package and its Tools 1-5 evidence chain. It contains no independent
  valuation logic and does not call the Router, ML, or CMT directly.
- All five permitted investment positions are implemented: `Strong
  Opportunity`, `Moderate Opportunity`, `Fairly Priced`, `Caution`, and `High
  Risk`.
- Strengths, risks, position reasons, evidence summaries, comparable
  summaries, negotiation summaries, and optional What-if summaries carry
  structured evidence references.
- ROI, IRR, CAGR, appreciation forecasts, future-price predictions, rental
  yield estimates, and investment-return generation remain absent.
- Missing optional What-if evidence is returned as `Insufficient Evidence`.
- Scenario investment evaluation, comparable grounding, fairness grounding,
  negotiation grounding, optional What-if integration, JWT tenant isolation,
  durable `investment` audit events, backend restart recovery, PostgreSQL
  restart recovery, PostGIS integration, and adjacent Docker regressions
  passed.

### Phase 5.5B.7: Market Insight Tool

Status: **COMPLETE**
Decision: **GO**

Summary:

- Tool 8 is a read-only descriptive analytics adapter over tenant-scoped
  persisted TruthLayer history. It does not call Router, ML, or CMT.
- Historical observations use valuation snapshots, prediction logs, shadow
  logs, comparable evidence, workspace history, and tool events.
- Compound, H3 area, property-type, historical-window, confidence,
  fair-value, and comparable-density insights are implemented.
- Every generated statement carries persisted evidence references.
- Forecasts, future prices, predicted appreciation, predicted returns, and
  synthetic trends remain absent.
- JWT tenant isolation, durable `market_insight` audit events, backend restart
  recovery, PostgreSQL restart recovery, PostGIS integration, migration
  verification, and adjacent Docker regressions passed.

### Phase 5.5C.1: Intent Engine V1

Status: **COMPLETE**
Decision: **GO**

Summary:

- Intent Engine V1 is a standalone in-process Copilot Orchestrator component.
- It implements only deterministic whole-keyword rules for the approved
  ten-intent taxonomy.
- Results return the primary intent, safe secondary intents, confidence,
  matched rules, matched keywords, clarification flag, and audit reason.
- Low-confidence fallback returns `GENERAL_QUESTION` with
  `requires_clarification = true`.
- Explicit misspelling aliases, mixed casing, whitespace noise, ambiguous
  messages, and multi-intent messages are tested.
- Docker validation runs with `--network none`; PostgreSQL, PostGIS, Router,
  CMT, ML, Tool Layer, vector stores, embeddings, and LLM providers are absent.
- The measured Docker average is `0.042005 ms`, below the `< 5 ms` target.

### Phase 5.5C.2: Tool Planner

Status: **COMPLETE**
Decision: **GO**

Summary:

- The Tool Planner is a standalone in-process Copilot Orchestrator component.
- It converts `IntentResult` into an auditable deterministic `ExecutionPlan`.
- Approved direct intents map only to Tools 1-8. Negotiation selects Tool 6
  alone and Investment selects Tool 7 alone because those Tools already
  orchestrate their required evidence chains.
- Property comparison adds no Tool 9. It plans two explicit parallel Tool 1
  invocation slots for `PROPERTY_A` and `PROPERTY_B`; the future Response
  Composer remains responsible for comparison arithmetic.
- Multi-intent results select independent top-level Tool calls in one parallel
  group.
- Low-confidence, clarification-requested, and `GENERAL_QUESTION` results
  return no Tools with `CLARIFICATION_REQUIRED`.
- Every plan includes `reason`, `selected_tools`, `selection_source`, and
  `intent_source`.
- Docker validation runs with `--network none`; PostgreSQL, PostGIS, Tool
  execution, Router, CMT, ML, HTTP clients, and LLM providers are absent.
- The measured Docker average is `0.009094 ms`, below the `< 1 ms` target.

### Phase 5.5C.3: Tool Executor

Status: **COMPLETE**
Decision: **GO**

Summary:

- The Tool Executor is a standalone in-process Copilot Orchestrator
  component.
- It consumes `ExecutionPlan` and invokes only the approved Tools 1-8 through
  the existing `CopilotToolsService`.
- Each Tool invocation receives an isolated SQLAlchemy session so parallel
  worker threads never share a session.
- Sequential, parallel multi-intent, and parallel two-Tool-1 property
  comparison execution are implemented.
- Property comparison returns two raw Tool 1 payloads. The executor performs
  no comparison arithmetic or interpretation.
- Clarification plans execute nothing.
- Configurable timeouts, structured failure objects, incomplete-payload
  signaling, and partial failure isolation are implemented.
- Raw Tool payloads remain uncompressed, untruncated, and unsummarized.
- Docker validation used real PostgreSQL/PostGIS, JWT-created tenant state,
  Tools 1-8, backend restart, and PostgreSQL restart.
- Measured Docker overhead was `1.427 ms` sequential and `2.190 ms` parallel,
  below the `< 10 ms` target excluding Tool runtime.

### Phase 5.5C.4B: Response Composer

Status: **COMPLETE**
Decision: **GO**

Summary:

- The Response Composer is a standalone in-process deterministic Copilot
  Orchestrator component.
- It consumes only extended `ExecutionResult`; `ExecutionPlan` does not cross
  the Composer boundary.
- `ExecutionResult` now carries copied `primary_intent` and
  `secondary_intents`.
- Strict schema normalizers cover approved Tools 1-8 and fail malformed
  successful payloads closed.
- Property Comparison V1 calculates only `price_delta`,
  `price_percentage_delta`, and label-only `confidence_level_label`.
- Comparable evidence arithmetic calculates only count, average, minimum, and
  maximum received prices.
- Comparable compressed context uses Top `3`, ordered by `distance_km ASC`
  then `comparable_id ASC`.
- Received `valuation_id`, optional `tool_event_id`, and optional
  `comparable_id` citations are preserved without lookup or fabrication.
- `compressed_context` and `frontend_payload` are separate structured data
  channels. No SSE, WebSocket, frontend integration, narration, prompt
  building, or LLM integration exists inside the Composer. Phase 5.5C.5 adds
  Memory Integration as a separate downstream component.
- Docker validation used real PostgreSQL/PostGIS, real Tools 1-8, real
  Executor output, backend restart replay, and PostgreSQL restart replay.
- Measured Docker average Composer overhead was `0.053627 ms`, below the
  `< 15 ms` target excluding Tool runtime.

### Phase 5.5C.5: Memory Integration

Status: **COMPLETE**
Decision: **GO**

Summary:

- The Memory Integration layer is a standalone deterministic Copilot
  Orchestrator component.
- It rebuilds bounded `MemoryContext` from existing approved PostgreSQL
  persistence only. No table, migration, cache, vector database, or embedding
  dependency was added.
- The idempotent `remember()` hook stores only Composer metadata, received
  citations, and active comparison context in existing `decision_history`.
- Workspace, scenario, property, and optional broker-session scope are
  tenant-validated and soft-delete-aware. Foreign and deleted scopes return
  `ACCESS_DENIED` with an empty disclosure.
- Governed limits bound recent Tool events to `10`, decisions to `10`,
  valuations to `5`, active assumptions to `20`, conversation metadata to
  `10`, and scenario lineage nodes to `10`.
- `memory_id` is derived from canonical structured context and remained
  identical after backend restart, PostgreSQL restart, and backend container
  recreation.
- Measured deterministic assembly overhead was `0.225618 ms`, below the
  `< 25 ms` target excluding database latency.
- Final source-level consistency review found no architectural drift across
  Intent Engine -> Tool Planner -> Tool Executor -> Response Composer ->
  Memory Integration. Each component retains its approved responsibility and
  dependency direction.

### Phase 5.5C.6 Narration Layer

Status: **COMPLETE**

Implementation: **GO**  
Provider integration: **IMPLEMENTED, DEFAULT-OFF**  
Runtime activation: **EXPLICIT PER-INTENT ONLY**  
Production promotion: **NO-GO**

Summary:

- Phase 5.5C.6A forensic review rejected the unauthorized attempted modern LLM
  package and live legacy LLM activation path. Both paths are retired.
- The implemented canonical target sequence is:

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

- Phase 5.5C.6D defined exact pass-through narration only. The LLM may narrate
  approved upstream facts and immutable citation tokens but may not create
  prices, arithmetic, rankings, winner declarations, offers, strategies,
  forecasts, predictions, ROI, IRR, CAGR, yield, appreciation, returns,
  synthetic trends, synthetic evidence, synthetic assumptions, or synthetic
  citations.
- Phase 5.5C.6D defined nine default-off intent-specific narration contracts:
  Valuation, Explainability, Comparables, Fairness, What-if, Negotiation,
  Investment, Market Insight, and Property Comparison. General-question,
  clarification, unsupported, generic catch-all, and multi-intent narration
  remain deterministic-only.
- Phase 5.5C.6F defined the Narration Admission Gate as a deterministic no-I/O
  pre-provider policy firewall. Only `ADMIT_NARRATION` may proceed toward
  Prompt Assembly. `ACCESS_DENIED` permits no scoped disclosure.
  `DETERMINISTIC_ONLY` and authorized `REJECT_NARRATION` use deterministic
  Composer-owned fallback behavior.
- Phase 5.5C.6G defined the Provider Adapter as a stateless, minimized
  transport boundary. Gemini 2.5 Pro receives only Prompt Assembly output
  derived from an approved provider-safe projection.
  Provider-side memory, Tools, functions, browsing, retrieval, files,
  embeddings, pre-grounding client streaming, automatic retry, and
  transparent failover remain forbidden unless separately reviewed and
  approved.
- Prompt Assembly is implemented with compact canonical JSON, protected
  context enforcement, deterministic optional eviction, a `12000` request
  token ceiling, `1500` response reserve, `1500` output token ceiling,
  `50` citation ceiling, `12000` narration-character ceiling, and a `20`
  second one-shot provider timeout.

## 7. Current Backend Status

The FastAPI backend exposes:

| Surface | Routes | Status |
| --- | --- | --- |
| Health | `/health`, `/health/ready`, `/health/metrics`, `/health/operational` | Implemented |
| Valuation | `/v1/valuation/fair-price`, `/v1/rent/fair-price` | Implemented |
| Copilot memory | `/v1/copilot/users/me`, workspace, chat, message, property, scenario, assumption, tool-event, decision routes | Implemented |
| Copilot tools | `/v1/copilot/tools/valuation`, `/explainability`, `/comparable`, `/fairness`, `/what-if`, `/negotiation`, `/investment`, `/market-insight` | Tools 1-8 implemented |
| Copilot orchestrator | `POST /v1/copilot/orchestrator/respond` | Activated; governed deterministic fallback with optional default-off per-intent narration |
| Broker | `/v1/broker/analyze`, `/chat`, `/intent`, `/reason`, `/stream`, `/session/{session_id}` | Implemented; valuation and explainability adapter flow repaired |

Backend control evidence through 2026-06-01:

- Direct Mivida valuation: `HTTP 200`, `CMT`, `GoldilocksZone`, `49` comparables,
  explainability present.
- Copilot Tool Docker validation: PASS for CMT, scenario modification, ML
  fallback, tenant isolation, snapshot recovery, and tool-event recovery.
- Copilot Tools 3 + 4 Docker validation: PASS for real comparable retrieval,
  snapshot replay, scenario overlays, all three fairness statuses, tenant
  isolation, tool-event persistence, backend restart recovery, PostgreSQL
  restart recovery, and static Truth Layer boundary scans.
- Live PostGIS Tools 3 + 4 integration suite: `3 passed`.
- Copilot What-if Docker validation: PASS for immutable base state, ephemeral
  overlays, size, bedroom, amenity, and scenario-on-scenario modifications,
  TruthLayer-derived delta calculation, fresh comparable and fairness
  evaluation, assumptions disclosure, tenant isolation, audit persistence,
  backend restart recovery, PostgreSQL restart recovery, and static Truth
  Layer boundary scans.
- Live PostGIS What-if plus adjacent integration suite: `5 passed`.
- Copilot Negotiation Docker validation: PASS for below, within, and above
  fair-value positions, scenario negotiation, comparable-grounded offer
  endpoints, fairness reuse, traceable talking points, traceable risks,
  traceable position rules, optional What-if integration, tenant isolation,
  audit persistence, backend restart recovery, PostgreSQL restart recovery,
  and static Truth Layer boundary scans.
- Live PostGIS Negotiation plus adjacent integration suite: `7 passed`.
- Copilot Investment Docker validation: PASS for all five investment
  positions, evidence-backed strengths and risks, absent optional What-if
  disclosure, scenario investment evaluation, comparable grounding, fairness
  grounding, negotiation grounding, optional What-if integration, tenant
  isolation, audit persistence, backend restart recovery, PostgreSQL restart
  recovery, zero forbidden metric fields, and static Truth Layer boundary
  scans.
- Live PostGIS Investment plus adjacent integration suite: `9 passed`.
- Copilot Tool Executor Docker validation: PASS for approved Tool 1-8
  dispatch, sequential execution, parallel property comparison, parallel
  multi-intent execution, raw payload preservation, clarification blocking,
  timeout handling, partial failure isolation, JWT-created tenant state,
  tenant isolation, audit metadata, backend restart recovery, PostgreSQL
  restart recovery, static executor boundary scans, and `< 10 ms` executor
  overhead.
- Live PostGIS Tool Executor suite: `2 passed`; adjacent Tools 3-8 plus
  executor sweep: `11 passed`.
- Copilot Response Composer Docker validation: PASS for reduced Property
  Comparison V1, approved comparable arithmetic, governed Top-3 compression,
  citation preservation, citation de-duplication, dual structured channels,
  five-status failure semantics, deterministic response IDs, backend restart
  replay, PostgreSQL restart replay, static boundary scans, and `< 15 ms`
  Composer overhead.
- Live PostGIS Response Composer plus Tool Executor suite: `4 passed`;
  adjacent Tools 3-8 plus Executor plus Composer sweep: `13 passed`.
- Copilot Memory Integration Docker validation: PASS for existing-persistence
  rebuild, tenant isolation, deleted-scope denial, empty context, governed
  compression, citation preservation, idempotent remember, deterministic
  memory IDs, backend restart, PostgreSQL restart, backend container
  recreation, zero forbidden dependencies, and `< 25 ms` overhead.
- Live PostGIS Memory Integration plus adjacent Tools 3-8, Executor, and
  Composer sweep: `14 passed`.
- Broker Adapter Docker validation: PASS for valuation chat, explainability
  chat, scenario overlay, workspace context, backend restart recovery, tenant
  isolation, persisted Tool 1/Tool 2 events, and zero direct pricing route
  references.
- Broker valuation-backed chat: non-degraded, grounded, and sourced from the
  Truth Layer through the Tool Layer.

## 8. Current Frontend Status

The active frontend is React 19 + Vite + TypeScript + Zustand.

| Screen | Status |
| --- | --- |
| Nexus | Implemented |
| Broker | Implemented initial SSE reasoning terminal |
| Valuation | Implemented |
| Pulse | Implemented presentation surface |
| Assets | Implemented presentation surface |
| Vault | Placeholder/presentation surface |
| Comparable evidence | Implemented |
| Explainability panel | Implemented |

Fresh frontend verification:

| Check | Result |
| --- | --- |
| `npm test` | `25 passed` |
| `npm run lint` | PASS |
| `npm run build` | PASS |

Remaining frontend integration gap:

- Axios requests do not attach `Authorization: Bearer ...`.
- Streaming fetch requests do not attach bearer tokens.
- `BrokerScreen` sends a local `session_id` and optional valuation request but
  not required `workspace_id` and `scenario_id`.
- Persisted broker session retrieval is not surfaced in the UI.

## 9. Current Copilot Status

| Copilot capability | Status | Persistence |
| --- | --- | --- |
| Workspace Memory | Implemented | `workspaces` |
| Chat Memory | Implemented | `chats`, `messages` |
| Property Memory | Implemented | `property_states` |
| Scenario Memory | Implemented | `scenario_states` |
| Assumptions Engine | Implemented | `assumptions` |
| Audit Trail | Implemented | `decision_history` |
| Tool Events | Implemented | `tool_events` |
| Valuation Snapshots | Implemented | `valuation_snapshots` |
| Scenario Lineage | Implemented | `scenario_lineage` |
| JWT Ownership | Implemented | JWT `sub` -> provisioned `users.external_subject` |
| Tenant Isolation | Implemented | API filtering plus composite foreign keys |
| Broker Session Recovery | Implemented | `broker_sessions` |
| Tool Layer | Operational | Valuation, Explainability, Comparable, Fairness, What-if, Negotiation, Investment, and Market Insight Tools |
| Orchestrator Intent Engine V1 | Implemented | Standalone in-process deterministic rules; no persistence required |
| Orchestrator Tool Planner | Implemented | Standalone deterministic `IntentResult` to `ExecutionPlan`; no persistence or execution required |
| Orchestrator Tool Executor | Implemented | Standalone `ExecutionPlan` to raw `ExecutionResult`; approved Tools 1-8 only, with failure isolation and no composition |
| Orchestrator Response Composer | Implemented | Standalone extended `ExecutionResult` to structured `ComposedResponse`; governed math, citations, compression, dual channels, and no persistence or LLM dependencies |
| Orchestrator Memory Integration | Implemented | Standalone deterministic `MemoryContext` rebuild from existing persistence; bounded history, citations, tenant isolation, idempotent Composer summary, restart-stable memory IDs, and no LLM dependencies |
| Phase 5.5C.6 target LLM path | Implemented | One default-off narration-only runtime after Memory Integration |
| Narration Contracts | Implemented | Nine default-off intent-specific contracts; exact pass-through narration only; immutable citations; deterministic-only general, clarification, unsupported, and multi-intent flows |
| Narration Admission Gate | Implemented | Deterministic no-I/O pre-provider policy firewall with four explicit states |
| Provider Adapter | Implemented | Fixed stateless Gemini 2.5 Pro one-shot transport; no automatic retry, transparent failover, provider memory, or pre-grounding delivery |
| Prompt Assembly | Implemented | Deterministic bounded representation-only packaging with protected context and stable optional eviction |
| Candidate Parser | Implemented | Strict two-field original-output parsing without repair or enrichment |
| Grounding Layer | Implemented | Exact upstream fact and immutable citation validation with `ACCEPT_NARRATION`, `REJECT_NARRATION`, and `ACCESS_DENIED` only |
| LLM runtime activation | Default-off | Explicit approved per-intent allowlist plus credential and provider data-governance acknowledgement required |
| Modern orchestrator transport | Implemented | Authenticated `POST /v1/copilot/orchestrator/respond`; approved component sequencing only; access-denied delivery redaction |
| Broker Adapter | Implemented | Tool 1 -> Tool 2 -> response builder; no direct pricing route usage |

Broker session rows require user, workspace, and scenario ownership. Fresh
Docker recovery validation confirms retrieval after backend restart,
PostgreSQL restart, and backend recreation. Fresh Phase 5.5B.2A Docker
validation also confirms non-degraded broker valuation and explainability
turns, scenario overlay handling, and cross-tenant concealment. Fresh Phase
5.5B.4 validation confirms immutable sandbox orchestration and durable What-if
audit events after restart. Fresh Phase 5.5B.5 validation confirms grounded
negotiation guidance, optional What-if sensitivity integration, and durable
Negotiation audit events after restart. Fresh Phase 5.5B.6 validation confirms
evidence-backed opportunity analysis, explicit insufficient-evidence handling,
and durable Investment audit events after restart.
Fresh Phase 5.5B.7 validation confirms persisted descriptive Market Insight
analytics, traceable statements, explicit sparse-evidence handling, and
durable Market Insight audit events after restart.
Fresh Phase 5.5C.1 validation confirms deterministic primary and secondary
intent classification, auditable matches, clarification fallback, zero
forbidden dependencies, and network-disabled Docker execution.
Fresh Phase 5.5C.2 validation confirms approved Tool selection, deterministic
plan equality, parallel property comparison, parallel multi-intent planning,
clarification blocking, zero forbidden dependencies, and network-disabled
Docker execution.
Fresh Phase 5.5C.3 validation confirms approved Tool execution, raw payload
preservation, parallel property comparison, parallel multi-intent execution,
clarification blocking, timeout handling, partial-failure isolation,
tenant isolation, audit metadata, and restart recovery.
Fresh Phase 5.5C.4B validation confirms approved arithmetic offload, reduced
Property Comparison V1, received citation preservation, Top-3 compression,
dual structured channels, five-status semantics, deterministic response IDs,
backend and PostgreSQL restart recomposition, zero forbidden dependencies,
and no database access or Tool execution.
Fresh Phase 5.5C.5 validation confirms existing-persistence-only context
rebuild, idempotent bounded Composer-summary persistence, scenario-scoped
retrieval, broker-session continuity, citation preservation, compression,
empty-context handling, fail-closed tenant isolation, deterministic memory
IDs, backend restart recovery, PostgreSQL restart recovery, backend container
recreation recovery, zero forbidden dependencies, and no model integration.
Fresh Phase 5.5C.6 validation confirms one authorized narration runtime,
retired legacy provider paths, deterministic admission and assembly,
immutable-citation rejection, fail-closed tenant isolation before provider
egress, one-shot transport failure handling, backend restart stability, and
PostgreSQL restart stability. Live Gemini activation remains default-off.
Fresh Phase 5.5C.RUNTIME.1 validation confirms one authenticated modern
orchestrator endpoint, Intent-to-final-response execution for valuation,
Property A/B comparison, Tool 6, Tool 7, Tool 8, and clarification, scoped
access-denied redaction, explicit fake-citation, fake-value, and
fake-prediction rejection, backend restart replay equality, and PostgreSQL
restart replay equality.

## 10. Tool Layer Status

| Tool | Name | Status | Notes |
| --- | --- | --- | --- |
| Tool 1 | Valuation Tool | COMPLETE | Authenticated adapter to Truth Layer Router; persists snapshots and events |
| Tool 2 | Explainability Tool | COMPLETE | Retrieves persisted explainability payload; persists events |
| Tool 3 | Comparable Tool | COMPLETE | Retrieves real CMT evidence from a tenant-scoped snapshot or Tool 1 valuation; persists events |
| Tool 4 | Fairness Tool | COMPLETE | Invokes Tool 1 with target price and normalizes existing Router fairness output; persists events |
| Tool 5 | What-if Tool | COMPLETE | Applies an ephemeral overlay over a base property or existing scenario; orchestrates Tools 1-4; returns TruthLayer-derived deltas, assumptions, feature changes, fresh evidence, and persisted audit events |
| Tool 6 | Negotiation Tool | COMPLETE | Orchestrates Tools 1-5; returns traceable positions, grounded offer bands, evidence-backed talking points and risks, optional What-if sensitivity evidence, and persisted audit events |
| Tool 7 | Investment Tool | COMPLETE | Orchestrates Tool 6 and its Tools 1-5 evidence chain; returns traceable positions, evidence-backed strengths and risks, optional What-if sensitivity evidence or Insufficient Evidence, and persisted audit events |
| Tool 8 | Market Insight Tool | COMPLETE | Reads tenant-scoped persisted snapshots, prediction logs, shadow logs, comparable evidence, workspace history, and tool events; returns traceable descriptive market observations only |

The repaired Broker Adapter still selects only the Valuation Tool and
Explainability Tool path. Tools 3, 4, 5, 6, 7, and 8 are implemented as
standalone Copilot Tool APIs but have not been added to the Broker registry.
No later Tool Layer implementation exists.

## 11. Explainability Status

Explainability is implemented, not planned.

Implemented forms:

- Deterministic CMT explanation strings and structured traces.
- Retrieval timeline, filtering stages, spatial diagnostics, evidence summary,
  amenity intelligence, and confidence dimensions.
- Router explanation, fairness explanation, narrative explanation, comparable
  evidence, and feature drivers.
- ML SHAP positive and negative feature contributions.
- Frontend explainability panel.
- Copilot Tool 2 retrieval from persisted valuation snapshots.

Remaining work:

- External audit analytics and long-term explainability reporting.

## 12. Monitoring Status

Implemented:

- `prediction_logs`.
- `shadow_logs`.
- Shadow alternative-engine execution.
- In-process counters, histograms, and recent event buffers.
- Request, valuation, broker, tool, latency, confidence, tier, and flag metrics.
- `/health/metrics`.
- `/health/operational`.
- Slow request and slow query telemetry.

Limitations:

- Metrics are process-local.
- No external APM, alerting, metrics backend, or distributed tracing backend.
- In-process rate limiting is not distributed.

## 13. Persistence Status

Canonical migrations:

| Migration | Purpose |
| --- | --- |
| `000_baseline.sql` | Baseline schema |
| `001_database_stabilization.sql` | Database stabilization |
| `002_address_resolution_cache.sql` | Address resolution cache |
| `003_geospatial_governance.sql` | Geospatial governance |
| `004_property_matrix_amenity_governance.sql` | Property matrix and amenities |
| `005_copilot_persistence_hardening.sql` | Copilot memory, audit, broker sessions, monitoring logs |
| `006_production_blockers_resolution.sql` | Ownership, restore provenance, tenant constraints |
| `007_copilot_tools_valuation_explainability.sql` | Valuation snapshots and tool input extension |

The canonical runner is `python -m app.scripts.run_migrations`. It uses ordered
forward-only SQL, checksums, advisory locking, and atomic application.
`python -m app.scripts.run_migrations --verify` passed during this rebuild.

The Alembic directory remains for historical inspection only.

## 14. Security Status

Implemented:

- HS256 bearer JWT validation.
- Required `sub`, `iat`, and `exp` claims plus issuer and audience checks.
- Trusted-subject user provisioning.
- JWT ownership on Copilot and Broker routes.
- Composite foreign keys for tenant-scoped entities.
- Cross-tenant API concealment using not-found responses.
- Explicit `JWT_SECRET` requirement in Docker Compose.
- Staging/production config guard against the development JWT secret.

Remaining:

- Web client token acquisition and attachment.
- Organization membership and role authorization.
- Managed secret storage and rotation.
- Authentication policy decision for direct valuation routes.

## 15. Production Readiness

Classification: **staging-grade governed platform with unresolved production
integration work**.

Fresh Docker evidence through 2026-06-01:

| Validation | Result |
| --- | --- |
| Compose config | PASS |
| `db`, `db-bootstrap`, `backend`, `frontend` runtime | PASS |
| Migration replay `000`-`007` | PASS |
| Health/readiness/metrics/operational | PASS |
| Staging smoke | PASS |
| Copilot recovery validator | PASS |
| Copilot Tools 1 + 2 validator | PASS |
| Copilot Tools 3 + 4 validator | PASS |
| Tools 3 + 4 live PostGIS integration suite | PASS: `3 passed` |
| Copilot What-if validator | PASS |
| What-if plus adjacent live PostGIS integration suite | PASS: `5 passed` |
| Copilot Negotiation validator | PASS |
| Negotiation plus adjacent live PostGIS integration suite | PASS: `7 passed` |
| Copilot Investment validator | PASS |
| Investment plus adjacent live PostGIS integration suite | PASS: `9 passed` |
| Broker Adapter validator | PASS |
| Broker valuation query | PASS |
| Broker explainability query | PASS |
| Broker scenario valuation query | PASS |
| Broker workspace context query | PASS |
| Broker restart recovery | PASS |
| Broker tenant isolation | PASS |
| Copilot Intent Engine validator | PASS |
| Copilot Tool Planner validator | PASS |
| Copilot Tool Executor validator | PASS |
| Tool Executor live PostGIS integration suite | PASS: `2 passed` |
| Tools 3-8 plus Tool Executor live PostGIS regression sweep | PASS: `11 passed` |
| Copilot Response Composer validator | PASS |
| Response Composer plus Tool Executor live PostGIS integration suite | PASS: `4 passed` |
| Tools 3-8 plus Tool Executor plus Response Composer live PostGIS regression sweep | PASS: `13 passed` |
| Copilot Memory Integration validator | PASS |
| Memory Integration plus Tool Executor plus Response Composer live PostGIS integration suite | PASS: `5 passed` |
| Tools 3-8 plus Tool Executor plus Response Composer plus Memory Integration live PostGIS regression sweep | PASS: `14 passed` |
| Copilot Orchestrator LLM V1 validator | PASS: one runtime, legacy retirement, grounding, citations, fail-closed behavior, tenant isolation, backend restart, PostgreSQL restart |
| Copilot Orchestrator runtime validator | PASS: authenticated endpoint, valuation, Property A/B comparison, Tool 6, Tool 7, Tool 8, clarification, access-denied redaction, fake citation, fake value, fake prediction, backend restart replay, PostgreSQL restart replay |

The JWT ownership layer is implemented, tenant isolation is validated, broker
session recovery is validated, Tools 1-8 are operational, the Broker Adapter is
repaired, and Docker validation passed.

Production promotion remains **NO-GO** until frontend JWT integration, direct
valuation auth policy, managed secrets, RBAC, and test drift are resolved.
Phase 5.5C.6 implementation does not change this classification. Live Gemini
traffic remains default-off until operational credentials and provider data-
governance acknowledgement are configured.

## 16. Open Risks

| Priority | Risk | Required action |
| --- | --- | --- |
| P0 | Frontend does not send JWT or broker workspace/scenario context | Implement authenticated client session bootstrap |
| P1 | Direct valuation routes remain unauthenticated | Decide and enforce intended public/internal policy |
| P1 | Backend suite has one stale collection import and 8 stale executed monkeypatch failures | Update tests to patch service boundaries |
| P1 | Production secret rotation is not implemented | Integrate managed secret store and runbook |
| P1 | Organization membership/RBAC is absent | Add organization and role authorization model |
| P2 | Metrics and rate limits are process-local | Externalize telemetry and shared rate limiting |
| P2 | CI/CD and production orchestration are incomplete | Add pipeline and deployment target |
| P2 | Licensed national polygon/gazetteer source is absent | Plan data-governance upgrade |
| P2 | Feature-rich What-if overlays can truthfully produce sparse or zero retained comparable evidence | Preserve evidence-depth disclosure and define product UX for sparse sandbox results |
| P2 | Sparse TruthLayer comparable results can truthfully limit Negotiation Tool comparable support | Preserve evidence-depth disclosure; never invent comparable replacements or offer prices |
| P2 | Sparse TruthLayer comparable results can truthfully limit Investment Tool opportunity confidence | Preserve evidence-depth disclosure and return Moderate Opportunity or explicit risks without inventing evidence |
| P2 | Immediate Market Insight telemetry persistence adds Tool Layer valuation latency | Measure latency under production-like load and move persistence to a durable queue if required |
| P2 | Sparse persisted Market Insight history can truthfully limit descriptive coverage | Return Sparse or Insufficient Evidence without inventing trends |
| P1 | Live Gemini activation requires an operational provider data-governance acknowledgement and out-of-band credential | Configure the approved operational controls before enabling any intent |
| P2 | Strict exact-fact Grounding intentionally rejects free-form provider prose | Measure rejection rate before widening any narration grammar |

## 17. Remaining Roadmap

Immediate:

1. Update stale backend tests and restore a clean broad suite.
2. Add frontend JWT, workspace, scenario, and recovered-session integration.
3. Decide direct valuation endpoint authentication policy.
4. Decide when Tools 3, 4, 5, 6, 7, and 8 should enter the Broker registry.
5. Keep Phase 5.5C.1 Intent Engine vocabulary additions, Phase 5.5C.2 Tool
   Planner mapping additions, Phase 5.5C.3 Tool Executor dispatch changes,
   Phase 5.5C.4B Response Composer arithmetic and compression boundaries, and
   Phase 5.5C.5 Memory Integration retrieval limits explicitly governed.
6. Keep Phase 5.5C.6 narration default-off until an operational Gemini
   credential and data-governance acknowledgement are configured.
7. Monitor exact-fact Grounding rejection rates before considering any
   separately governed narration-grammar expansion.

Next:

1. Add organization membership and RBAC.
2. Externalize monitoring, alerting, and shared rate limiting.
3. Add CI/CD and managed deployment.

## 18. Future Architecture

The future production architecture should preserve Truth Layer authority:

```text
Web / Mobile Client
  -> Identity Provider
  -> JWT + organization claims
  -> API Gateway / shared rate limit
  -> Broker Copilot Orchestrator
       -> Intent Engine
       -> Tool Planner
       -> Tool Executor
       -> Response Composer
       -> Memory Integration Pre-Generation
       -> Narration Admission Gate
       -> Prompt Assembly
       -> Stateless Provider Adapter
       -> Candidate Parser
       -> Deterministic Grounding and Governance
       -> Memory Integration Post-Generation, when approved
       -> Delivery
  -> Copilot Tool Registry
       -> Valuation Tool
       -> Explainability Tool
       -> Comparable Tool
       -> Fairness Tool
       -> What-if Tool
       -> Negotiation Tool
       -> Investment Tool
       -> Market Insight Tool
  -> Truth Layer Router
       -> CMT
       -> ML
  -> PostgreSQL/PostGIS
  -> shared cache / queue where justified
  -> external telemetry, alerts, and audit analytics
```

LLM narration may summarize locked deterministic context only after a
fail-closed Narration Admission Gate and before deterministic original-output
grounding. It must not become a valuation, planning, execution, arithmetic,
memory, citation, tenant-binding, persistence, or delivery authority.

## Source Index

Primary code sources:

- `pf_scraper/fair-price-eg/backend/app/core/auth.py`
- `pf_scraper/fair-price-eg/backend/app/services/router_service.py`
- `pf_scraper/fair-price-eg/backend/app/services/monitoring_service.py`
- `pf_scraper/fair-price-eg/backend/app/services/copilot_service.py`
- `pf_scraper/fair-price-eg/backend/app/services/copilot_tools_service.py`
- `pf_scraper/fair-price-eg/backend/app/copilot/orchestrator/intents/`
- `pf_scraper/fair-price-eg/backend/app/copilot/orchestrator/planner/`
- `pf_scraper/fair-price-eg/backend/app/copilot/orchestrator/executor/`
- `pf_scraper/fair-price-eg/backend/app/copilot/orchestrator/composer/`
- `pf_scraper/fair-price-eg/backend/app/copilot/orchestrator/memory/`
- `pf_scraper/fair-price-eg/backend/app/copilot/orchestrator/runtime.py`
- `pf_scraper/fair-price-eg/backend/app/api/routes/copilot_orchestrator.py`
- `pf_scraper/fair-price-eg/scripts/validate_orchestrator_runtime.ps1`
- `pf_scraper/fair-price-eg/backend/app/broker/sessions/state.py`
- `pf_scraper/fair-price-eg/backend/app/broker/tools/valuation.py`
- `pf_scraper/fair-price-eg/backend/app/db/migrations/`
- `pf_scraper/fair-price-eg/docker-compose.yml`
- `pf_scraper/fair-price-eg/frontend/src/`

Supporting reports:

- `pf_scraper/fair-price-eg/docs/COPILOT_PHASE_5_5B_1R_PERSISTENCE_RECOVERY_REPORT.md`
- `pf_scraper/fair-price-eg/docs/COPILOT_PHASE_5_5B_1R_FINAL_DOCKER_VALIDATION.md`
- `pf_scraper/fair-price-eg/docs/COPILOT_PHASE_5_5B_1R_1_PRODUCTION_BLOCKERS_RESOLUTION.md`
- `pf_scraper/fair-price-eg/PHASE_5_5B_2_TOOLS_1_2_IMPLEMENTATION_REPORT.md`
- `pf_scraper/fair-price-eg/BROKER_ADAPTER_ROOT_CAUSE.md`
- `pf_scraper/fair-price-eg/PHASE_5_5B_2A_BROKER_ADAPTER_REPAIR_REPORT.md`
- `pf_scraper/fair-price-eg/PHASE_5_5B_3_TOOLS_3_4_IMPLEMENTATION_REPORT.md`
- `pf_scraper/fair-price-eg/TOOLS_3_4_DOCKER_VALIDATION_REPORT.md`
- `pf_scraper/fair-price-eg/PHASE_5_5B_4_WHAT_IF_IMPLEMENTATION_REPORT.md`
- `pf_scraper/fair-price-eg/WHAT_IF_DOCKER_VALIDATION_REPORT.md`
- `pf_scraper/fair-price-eg/PHASE_5_5B_5_NEGOTIATION_TOOL_IMPLEMENTATION_REPORT.md`
- `pf_scraper/fair-price-eg/NEGOTIATION_TOOL_DOCKER_VALIDATION_REPORT.md`
- `pf_scraper/fair-price-eg/PHASE_5_5C_1_INTENT_ENGINE_IMPLEMENTATION_REPORT.md`
- `pf_scraper/fair-price-eg/INTENT_ENGINE_DOCKER_VALIDATION_REPORT.md`
- `pf_scraper/fair-price-eg/INTENT_ENGINE_ARCHITECTURE_DIAGRAM.md`
- `pf_scraper/fair-price-eg/INTENT_CLASSIFICATION_MATRIX.md`
- `pf_scraper/fair-price-eg/PHASE_5_5C_2_TOOL_PLANNER_IMPLEMENTATION_REPORT.md`
- `pf_scraper/fair-price-eg/TOOL_PLANNER_DOCKER_VALIDATION_REPORT.md`
- `pf_scraper/fair-price-eg/TOOL_PLANNER_ARCHITECTURE_DIAGRAM.md`
- `pf_scraper/fair-price-eg/EXECUTION_PLAN_MATRIX.md`
- `pf_scraper/fair-price-eg/PHASE_5_5C_3_TOOL_EXECUTOR_IMPLEMENTATION_REPORT.md`
- `pf_scraper/fair-price-eg/TOOL_EXECUTOR_DOCKER_VALIDATION_REPORT.md`
- `pf_scraper/fair-price-eg/TOOL_EXECUTOR_ARCHITECTURE_DIAGRAM.md`
- `pf_scraper/fair-price-eg/EXECUTION_RESULT_CONTRACT.md`
- `pf_scraper/fair-price-eg/PHASE_5_5C_4B_RESPONSE_COMPOSER_IMPLEMENTATION_REPORT.md`
- `pf_scraper/fair-price-eg/RESPONSE_COMPOSER_DOCKER_VALIDATION_REPORT.md`
- `pf_scraper/fair-price-eg/RESPONSE_COMPOSER_ARCHITECTURE_DIAGRAM.md`
- `pf_scraper/fair-price-eg/COMPOSED_RESPONSE_EXAMPLES.md`
- `pf_scraper/fair-price-eg/COMPOSER_GOVERNANCE_AUDIT.md`
- `pf_scraper/fair-price-eg/PHASE_5_5C_5_MEMORY_INTEGRATION_IMPLEMENTATION_REPORT.md`
- `pf_scraper/fair-price-eg/MEMORY_INTEGRATION_DOCKER_VALIDATION_REPORT.md`
- `pf_scraper/fair-price-eg/MEMORY_ARCHITECTURE_DIAGRAM.md`
- `pf_scraper/fair-price-eg/MEMORY_CONTEXT_CONTRACT.md`
- `pf_scraper/fair-price-eg/MEMORY_GOVERNANCE_AUDIT.md`
- `pf_scraper/fair-price-eg/MEMORY_INTEGRATION_FINAL_READINESS_REPORT.md`
- `LLM_INTEGRATION_FORENSIC_AUDIT.md`
- `LLM_INTEGRATION_BOUNDARY_VIOLATIONS.md`
- `LLM_INTEGRATION_ARCHITECTURE_DECISION.md`
- `PHASE_5_5C_6B_FORMAL_ARCHITECTURE_REVIEW.md`
- `PHASE_5_5C_6B_RUNTIME_DECISION.md`
- `PHASE_5_5C_6B_BOUNDARY_OWNERSHIP_MATRIX.md`
- `PHASE_5_5C_6B_CANONICAL_RUNTIME_PATH.md`
- `PHASE_5_5C_6B_APPROVAL_REQUIREMENTS.md`
- `NARRATION_CONTRACT_ARCHITECTURE.md`
- `VALUATION_NARRATION_CONTRACT.md`
- `EXPLAINABILITY_NARRATION_CONTRACT.md`
- `COMPARABLES_NARRATION_CONTRACT.md`
- `FAIRNESS_NARRATION_CONTRACT.md`
- `WHAT_IF_NARRATION_CONTRACT.md`
- `NEGOTIATION_NARRATION_CONTRACT.md`
- `INVESTMENT_NARRATION_CONTRACT.md`
- `MARKET_INSIGHT_NARRATION_CONTRACT.md`
- `PROPERTY_COMPARISON_NARRATION_CONTRACT.md`
- `NARRATION_PROHIBITED_CLAIMS_MATRIX.md`
- `NARRATION_ACTIVATION_POLICY.md`
- `NARRATION_APPROVAL_DECISION.md`
- `PHASE_5_5C_6FG_ARCHITECTURE_REVIEW.md`
- `MASTER_STATE_5_5B_3_UPDATE_REPORT.md`
- `MASTER_STATE_5_5B_5_UPDATE_REPORT.md`

## PX-1A Property Context Bridge Update - 2026-06-09

Status: Implemented for the React frontend only.

Scope completed:

- Direct valuation success now silently starts a backend property-context bridge.
- `propertyContextService.ts` reuses an active workspace when available, otherwise reuses the first backend workspace, creates `ValorAI Active Valuations` only when needed, binds to an existing matching property context, creates one when needed, and records a scoped `direct_valuation` tool event.
- `propertyContextStore.ts` persists `activeWorkspaceId`, `activePropertyId`, and nullable `activeScenarioId` for future intelligence tools.
- `property_context_bridge.md` documents the flow, backend endpoints used, binding rules, and limitations.

Scope explicitly not changed:

- No What-if UI, Negotiation, Investment, Market Intelligence, Copilot, Dashboard, backend API, database migration, auth, deployment, or infrastructure changes.

Known limitation:

- The bridge uses authenticated Copilot persistence endpoints. React JWT acquisition remains outside this PX-1A bridge and is still a separate integration gap.

## PX-0 Frontend Product Completion Planning Update - 2026-06-09

Scope: React frontend product completion planning only. No frontend code, backend code, auth, security, deployment, infrastructure, or production-hardening work was performed.

Product positioning clarification:

- ValorAI is primarily a Real Estate Valuation Platform and Real Estate Intelligence Platform.
- The core product is the Fair Price Engine, Valuation Engine, Explainability, Comparables, Market Intelligence, Negotiation Intelligence, Investment Intelligence, and Scenario Analysis.
- Copilot is an intelligence layer on top of these capabilities, not the primary product architecture.

Current React frontend status:

- Direct valuation is exposed through `POST /v1/valuation/fair-price`.
- Fair price, price range, confidence, direct explainability, and direct comparable evidence are visible.
- Explainability, comparables, and fairness are partially exposed through the direct valuation response.
- Pulse, Assets, and Vault remain concept surfaces: Pulse and Vault are static; Assets aliases the Valuation screen.
- The React frontend does not expose Tool 5 What-if, Tool 6 Negotiation, Tool 7 Investment, Tool 8 Market Insight, scenario lineage, decision history, tool events, property comparison, or the modern Copilot orchestrator.

Current backend status:

- Backend business capabilities are substantially ahead of the React frontend.
- Direct valuation, Tools 1-8, workspace/property/scenario state, assumptions, tool events, decision history, scenario lineage/tree, response composer, memory integration, and orchestrator transport are implemented.
- Backend readiness is sufficient to begin frontend product exposure without redesigning backend architecture.

Verified gaps:

- Real gaps: What-if Scenario Analysis, Market Intelligence, Negotiation Intelligence, Investment Intelligence, Property Intelligence, Scenario Library/Lineage, Decision History/Tool Events, Copilot Orchestrator Integration, Property Comparison.
- Partial gaps: Explainability, Comparables, Fairness, Broker business-context alignment.
- False positives: Direct valuation missing, core fair-price display missing, Broker screen absent, direct comparables completely hidden, direct explainability completely hidden.

Recommended implementation order:

1. What-if Scenario Analysis on the valuation result surface.
2. Negotiation Intelligence using the same active property context.
3. Market Insight binding for Pulse after valuation history exists.
4. Investment Intelligence after negotiation output is visible.
5. Scenario Library and Decision History to make analysis durable.
6. Copilot orchestrator integration as a contextual layer over active property/scenario data.

Next phase recommendation:

- PX-1 should implement What-if Scenario Analysis only.
- Highest ROI rationale: backend Tool 5 is ready, the existing valuation UI already captures baseline property data, and the frontend can reuse current valuation, comparable, and explainability surfaces to expose a major new business capability with contained effort.

Planning artifacts created:

- `pf_scraper/fair-price-eg/feature_gap_verification.md`
- `pf_scraper/fair-price-eg/frontend_product_completion_roadmap.md`
- `pf_scraper/fair-price-eg/next_implementation_plan.md`

## PX-1 What-if Scenario Analysis Completion (2026-06-09)

Status: Completed and frontend-reachable.

Current status:

- Implemented complete What-if Scenario Analysis vertical slice on top of the existing Property Context Bridge.
- Added typed Tool 5 contracts, runtime-safe service parsing, Zustand scenario store, embedded valuation-workflow UI, scenario comparison, delta summary, assumptions, explainability, comparables, and reset flow.
- Updated PX-1 audit and implementation reports under `pf_scraper/fair-price-eg/docs/`.

Known limitations:

- Backend Tool 5 does not expose scenario price ranges; the UI displays the base valuation range and marks scenario range unavailable rather than inventing fields.
- Runtime scenario execution still depends on authenticated Copilot persistence/property-context requests.
- The UI keeps the latest scenario response active; persisted scenario history and lineage browsing remain PX-2 scope.

Recommended PX-2:

- Add persisted scenario history and scenario-lineage browsing inside the existing property context workflow.

Verification:

- `npm test` passed: 15 files, 46 tests.
- `npm run build` passed.
- `npm run lint` passed.

## PX-2 Negotiation Intelligence Completion (2026-06-09)

Status: Completed and frontend-reachable inside Valuation -> What-if -> Scenario Comparison -> Negotiation Intelligence.

Files created:

- `pf_scraper/fair-price-eg/frontend/src/types/negotiation.ts`
- `pf_scraper/fair-price-eg/frontend/src/services/negotiationService.ts`
- `pf_scraper/fair-price-eg/frontend/src/services/negotiationService.test.ts`
- `pf_scraper/fair-price-eg/frontend/src/store/negotiationStore.ts`
- `pf_scraper/fair-price-eg/frontend/src/store/negotiationStore.test.ts`
- `pf_scraper/fair-price-eg/frontend/src/features/what-if/NegotiationIntelligencePanel.tsx`
- `pf_scraper/fair-price-eg/frontend/src/features/what-if/NegotiationIntelligencePanel.test.tsx`

Files modified:

- `pf_scraper/fair-price-eg/frontend/src/features/what-if/WhatIfScenarioPanel.tsx`
- `pf_scraper/fair-price-eg/frontend/src/features/what-if/WhatIfScenarioPanel.test.tsx`
- `pf_scraper/fair-price-eg/frontend/src/test/fixtures.ts`
- `PROJECT_MASTER_STATE_V2.md`
- `PROJECT_MASTER_STATE_v3.md`
- `docs/PROJECT_MASTER_STATE.md`
- `docs/PROJECT_MASTER_STATE_BACKUP.md`
- `docs/PROJECT_MASTER_STATE_V2.md`
- `docs/PROJECT_MASTER_STATE_v3.md`
- `pf_scraper/fair-price-eg/PROJECT_MASTER_STATE.md`

Business impact:

- Users can run Tool 6 Negotiation Intelligence from the existing valuation what-if workflow without a new route or page.
- The UI shows fair price, asking price, recommended offer, negotiation range, buyer position, seller position, strengths, risks, talking points, evidence, confidence, and scenario sensitivity.
- Negotiation can target the base valuation, the latest active what-if scenario, or a selected/restored persisted scenario.
- The store preserves recent negotiation runs so base and scenario outcomes can be compared.

Known limitations:

- Runtime execution still depends on authenticated Copilot property/scenario persistence endpoints.
- For unsaved active what-if changes, the backend contract accepts `what_if_modifications` as sensitivity evidence; it does not replace the authoritative fair price unless the scenario has been persisted and supplied as `scenario_id`.
- No backend contracts were modified, and no Market Intelligence or Investment Intelligence work was started.

Verification:

- `npm run lint` passed.
- `npm test` passed: 20 files, 72 tests.
- `npm run build` passed.
- Browser smoke check rendered `http://localhost:3001/valuation` with no console warnings or errors.

## PX-3 Investment Intelligence Completion (2026-06-09)

Status: Completed and frontend-reachable inside Valuation -> What-if -> Negotiation Intelligence -> Investment Intelligence.

Recovery summary:

- PX-3 was already partially implemented before recovery.
- Existing Investment types, service, store, UI, fixtures, and tests were audited instead of recreated.
- The only code-level gap found was a failing Investment UI test assertion that expected a single `High Risk` node even though the complete UI intentionally renders the position in multiple cards.

Files present from recovered PX-3 work:

- `pf_scraper/fair-price-eg/frontend/src/types/investment.ts`
- `pf_scraper/fair-price-eg/frontend/src/services/investmentService.ts`
- `pf_scraper/fair-price-eg/frontend/src/services/investmentService.test.ts`
- `pf_scraper/fair-price-eg/frontend/src/store/investmentStore.ts`
- `pf_scraper/fair-price-eg/frontend/src/store/investmentStore.test.ts`
- `pf_scraper/fair-price-eg/frontend/src/features/investment/InvestmentIntelligencePanel.tsx`
- `pf_scraper/fair-price-eg/frontend/src/features/investment/InvestmentIntelligencePanel.test.tsx`

Files modified for completion:

- `pf_scraper/fair-price-eg/frontend/src/features/investment/InvestmentIntelligencePanel.test.tsx`
- `pf_scraper/fair-price-eg/frontend/src/features/what-if/WhatIfScenarioPanel.tsx`
- `pf_scraper/fair-price-eg/frontend/src/test/fixtures.ts`
- `PROJECT_MASTER_STATE_V2.md`
- `PROJECT_MASTER_STATE_v3.md`
- `docs/PROJECT_MASTER_STATE.md`
- `docs/PROJECT_MASTER_STATE_BACKUP.md`
- `docs/PROJECT_MASTER_STATE_V2.md`
- `docs/PROJECT_MASTER_STATE_v3.md`
- `pf_scraper/fair-price-eg/PROJECT_MASTER_STATE.md`

Documentation created:

- `pf_scraper/fair-price-eg/docs/PX3_RECOVERY_AUDIT.md`
- `pf_scraper/fair-price-eg/docs/PX3_GAP_ANALYSIS.md`
- `pf_scraper/fair-price-eg/docs/PX3_COMPLETION_REPORT.md`

Business impact:

- Users can run Tool 7 Investment Intelligence from the existing valuation what-if workflow without a new route or architecture change.
- Investment analysis can target the base valuation, active unsaved what-if modifications, a selected/restored scenario, or compared saved scenarios.
- The UI shows investment recommendation, scorecard, risks, strengths/opportunities, upside/downside, evidence, confidence, and scenario outcome comparison.
- Recent investment runs are preserved for comparing base and scenario outcomes.

Known limitations:

- Runtime execution still depends on authenticated Copilot property/scenario persistence endpoints.
- The scorecard reflects backend evidence, position, confidence, fairness, and price-gap data. No ROI, IRR, CAGR, rental yield, future-price forecast, or synthetic return score is generated.
- No backend contracts were modified, and no Market Intelligence, Copilot, Dashboard, or PX-4 work was started.

Verification:

- `npm run lint` passed.
- `npm test` passed: 23 files, 90 tests.
- `npm run build` passed.

## PX-4 Market Intelligence Completion (2026-06-10)

Status: Completed and frontend-reachable in Pulse.

Implemented:

- Replaced the static Pulse concept screen with a real Market Intelligence surface backed by existing backend Tool 8.
- Added frontend Market Insight contracts, service validation, store state, fixtures, and tests.
- Added `MarketIntelligencePanel` with workspace awareness, Tool 8 filters, success, empty, sparse, loading, and error states.
- Removed unsupported static Pulse claim cards and rendered only backend-supported Market Insight fields.

Files created:

- `pf_scraper/fair-price-eg/frontend/src/types/marketInsight.ts`
- `pf_scraper/fair-price-eg/frontend/src/services/marketInsightService.ts`
- `pf_scraper/fair-price-eg/frontend/src/services/marketInsightService.test.ts`
- `pf_scraper/fair-price-eg/frontend/src/store/marketInsightStore.ts`
- `pf_scraper/fair-price-eg/frontend/src/store/marketInsightStore.test.ts`
- `pf_scraper/fair-price-eg/frontend/src/features/pulse/MarketIntelligencePanel.tsx`
- `pf_scraper/fair-price-eg/frontend/src/features/pulse/MarketIntelligencePanel.test.tsx`
- `pf_scraper/fair-price-eg/docs/PX4_COMPLETION_REPORT.md`

Files modified:

- `pf_scraper/fair-price-eg/frontend/src/features/pulse/PulseScreen.tsx`
- `pf_scraper/fair-price-eg/frontend/src/test/fixtures.ts`
- `pf_scraper/fair-price-eg/PROJECT_MASTER_STATE.md`
- `PROJECT_MASTER_STATE_V2.md`
- `PROJECT_MASTER_STATE_v3.md`
- `docs/PROJECT_MASTER_STATE.md`
- `docs/PROJECT_MASTER_STATE_BACKUP.md`
- `docs/PROJECT_MASTER_STATE_V2.md`
- `docs/PROJECT_MASTER_STATE_v3.md`

Business impact:

- Pulse is now a truthful workspace market history surface.
- Users can inspect observed persisted TruthLayer valuations, evidence quality, comparable density, active compounds, active areas, source counts, filters used, data sources, and traceability notes.
- Empty and sparse evidence states are explicit and do not invent conclusions.

Known limitations:

- Runtime execution depends on an active workspace context created by prior valuation flow.
- New or filtered-empty workspaces correctly show no matching persisted TruthLayer valuations.
- No backend contracts, backend code, Copilot UI, orchestrator UI, dashboard, or PX-5 work was started.

Verification:

- `npm run lint` passed.
- `npm test` passed: 26 files, 110 tests.
- `npm run build` passed.

## PX-5 Copilot Orchestrator Layer Completion (2026-06-10)

Status: Completed and frontend-reachable through the global property-aware Copilot drawer.

Implemented:

- Added frontend Copilot orchestrator contracts, service validation, store state, fixtures, and tests.
- Added `CopilotDrawer`, `CopilotPanel`, `ContextSummaryBar`, `EvidenceDrawer`, `CitationViewer`, and `ToolExecutionTimeline`.
- Wired the drawer into `AppShell` without creating a standalone chatbot route or redesigning ValorAI.
- Copilot now builds orchestrator inputs from active workspace, property, selected scenario, latest valuation, what-if, negotiation, investment, and market insight state.
- Structured responses render answer, reasoning summary, evidence, citations, tool usage, confidence/status, and human-readable memory context.

Files created:

- `pf_scraper/fair-price-eg/frontend/src/types/copilot.ts`
- `pf_scraper/fair-price-eg/frontend/src/services/copilotService.ts`
- `pf_scraper/fair-price-eg/frontend/src/services/copilotService.test.ts`
- `pf_scraper/fair-price-eg/frontend/src/store/copilotStore.ts`
- `pf_scraper/fair-price-eg/frontend/src/store/copilotStore.test.ts`
- `pf_scraper/fair-price-eg/frontend/src/features/copilot/`
- `pf_scraper/fair-price-eg/docs/PX5_ORCHESTRATOR_AUDIT.md`
- `pf_scraper/fair-price-eg/docs/PX5_TYPES_AUDIT.md`
- `pf_scraper/fair-price-eg/docs/PX5_SERVICE_AUDIT.md`
- `pf_scraper/fair-price-eg/docs/PX5_STORE_AUDIT.md`
- `pf_scraper/fair-price-eg/docs/PX5_ARCHITECTURE_SUMMARY.md`
- `pf_scraper/fair-price-eg/docs/PX5_COMPLETION_REPORT.md`

Files modified:

- `pf_scraper/fair-price-eg/frontend/src/layouts/AppShell.tsx`
- `pf_scraper/fair-price-eg/frontend/src/test/fixtures.ts`
- `pf_scraper/fair-price-eg/PROJECT_MASTER_STATE.md`
- `PROJECT_MASTER_STATE_V2.md`
- `PROJECT_MASTER_STATE_v3.md`
- `docs/PROJECT_MASTER_STATE.md`
- `docs/PROJECT_MASTER_STATE_BACKUP.md`
- `docs/PROJECT_MASTER_STATE_V2.md`
- `docs/PROJECT_MASTER_STATE_v3.md`

Business impact:

- Users can ask natural-language property questions from the existing workflow and receive composed, evidence-backed intelligence.
- Copilot exposes existing ValorAI valuation, scenario, negotiation, investment, and market intelligence rather than replacing them.

Known limitations:

- Runtime execution still depends on authenticated Copilot persistence endpoints.
- The orchestrator response exposes memory ID/status, not the full backend `MemoryContext`; the frontend renders human-readable active workflow context.
- Property comparison still requires a future frontend property-B capture flow.

Verification:

- `npm run lint` passed.
- `npm test` passed: 30 files, 123 tests.
- `npm run build` passed.

PX-5 COMPLETE.

## Sprint 2 Broker Contract Alignment - 2026-06-11

Status: SPRINT 2 COMPLETE. P0-2 CLOSED.

React Broker payloads now match backend `BrokerChatRequest` and
`BrokerReasonRequest` contracts. Broker reason, chat, and stream requests carry
validated `workspace_id`, `scenario_id`, `message`, optional `session_id`,
optional `valuation_request`, and optional `investor_preferences` only.

Implemented:

- Required Broker request ids in frontend types.
- Runtime Broker request validation and payload sanitization in the service layer.
- Active workspace/property/scenario resolution before Broker execution.
- Baseline scenario creation through existing scenario APIs when no active scenario exists.
- Scenario history synchronization into active property context.

Verification:

- `npm run lint` passed.
- `npm test` passed: 35 files, 144 tests.
- `npm run build` passed.

Sprint 3 closed backend pytest collection repairs. No P0 backend test blocker remains in the default local suite.

## Sprint 3 Backend Test Suite Recovery - 2026-06-11

Status: SPRINT 3 COMPLETE. P0-3 CLOSED.

Backend pytest now collects, executes, and passes in the default local
environment.

Verification:

- `pytest --collect-only -q` passed: 207 tests collected.
- `pytest -q` passed: 205 passed, 11 skipped.
- `pytest app/tests -q` passed: 205 passed, 9 skipped.
- Targeted Sprint 3 regression command passed: 10 passed, 2 skipped.

Remaining skips are explicit PostGIS integration gates requiring
`RUN_POSTGIS_INTEGRATION=1` and seeded PostgreSQL/PostGIS data.
