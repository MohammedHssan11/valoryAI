# ValorAI / Fair Price Egypt

Last updated: 2026-06-01

Primary application path: `pf_scraper/fair-price-eg`

Repository scope: PropertyFinder Egypt scraper/data tooling, deterministic real-estate valuation backend, React/Vite frontend, Docker/PostgreSQL/PostGIS infrastructure, and emerging broker reasoning APIs.

---

# Project Summary

ValorAI is a real-estate intelligence platform combining rigorous deterministic market matching with advanced ML modeling to produce investor-grade property valuations in Egypt.

**Current System Status:**
*   **Deterministic Engine:** Highly stable. Baseline drift is ≈ 12%.
*   **Pure ML Baseline:** Completed but underperforms the deterministic engine due to high market noise and limited generic features.
*   **Phase Pivot:** Because Pure ML is insufficient independently, **Hybrid Architecture (Phase 4)** has been officially selected as the next phase.
*   **Phase 5.5 Pivot:** Evolution to a governed deterministic intelligence platform prototype with a dedicated Copilot Tool Layer, tenant isolation, and Broker Intelligence Terminal.

**Project Health:**
*   Data Pipeline: Production Ready
*   Deterministic Engine: Production Ready
*   Dataset Builder: Production Ready
*   Baseline ML: Research Complete
*   Hybrid AVM: Active Development
*   Copilot Persistence: Production Ready
*   JWT Authentication: Production Ready
*   Tool Layer (Valuation, Explainability, Comparable, Fairness, What-if, Negotiation & Investment): Implemented

**Verified Fixes (Phase 3.5 & 3.6):**
*   H3 versioning bug fixed (0% missing values).
*   Multi-tier dataset duplicate contamination completely eradicated.
*   Temporal listing age leakage fixed.
*   Compound matching/regex collapse hardened.
*   Amenities frequency/vocabulary leakage fixed.
*   CatBoost categorical permutation temporal leakage fixed.

**Dataset Status:**
*   `dataset_v3` = Official Source of Truth
*   `dataset_v1` = Historical / Deprecated
*   `dataset_v2` = Historical / Deprecated
*   `dataset_v1` and `dataset_v2` must never be used for future model training.

---

# System Architecture (Verified System Map)

The ValorAI architecture is cleanly segregated into 6 sequential layers.

| Layer | Component | Status | Description |
| :--- | :--- | :--- | :--- |
| **Layer 1** | **Data Collection** | Implemented | Automated scraping of PropertyFinder Egypt into raw JSONL files. |
| **Layer 2** | **Data Processing** | Implemented | Initial cleaning and normalization scripts. |
| **Layer 3** | **Dataset Builder** | Implemented | Generates `dataset_v3` `.parquet` artifacts with rigorous 4-Tier upstream deduplication, H3 index extraction, and strict out-of-time guardrails. |
| **Layer 4** | **Deterministic Engine** | Implemented | Fast API backend executing PostGIS spatial radius expansion, strict outlier removal (MAD), comparable counting, and confidence scoring. Acts as the architectural anchor. |
| **Layer 5** | **Baseline ML Layer** | Implemented | Pure CatBoost ML pipelines. Evaluated strictly out-of-time. Verified to be free of target leakage, but performance ceilings out without deterministic injection. Metrics: Residential Rent (MAPE ≈ 22.78%, R² ≈ 0.498), Residential Sale (MAPE ≈ 25.87%, R² ≈ 0.782). |
| **Layer 6** | **Future Hybrid Layer** | **Planned (Phase 4)** | Merging Layer 4 deterministic outputs (Comparable Count, Median Price, Tier Reached) directly into the Layer 5 ML models to form a composite Hybrid AVM. |
| **Layer 7** | **Copilot Tool Layer (Phase 5.5)** | **Active Development** | Stateful tenant-isolated tool execution environment (Valuation, Explainability, Comparable, Fairness, What-if, Negotiation, Investment) acting as a governed adapter to the deterministic core. |

### Current Production Architecture

`	ext
Client
  ↓
JWT Authentication
  ↓
Copilot Tool Layer
  ↓
Truth Layer
  ↓
Conditional Router
  ↓
ML OR CMT
  ↓
Explainability
  ↓
Monitoring
`

*(Note: Legacy frontend and NLP Broker Reasoning APIs exist in `pf_scraper/fair-price-eg/` but are considered secondary to the core Valuation Engine logic outlined above.)*

---

# Roadmap & Project Progression

| Phase | Designation | Status | Objective |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Data Audit & Discovery | ✅ Complete | Initial raw data feasibility checks. |
| **Phase 2** | Dataset Builder | ✅ Complete | ETL pipeline formulation. |
| **Phase 2.5** | Dataset Hardening | ✅ Complete | Feature engineering and data robustness. |
| **Phase 3** | Baseline CatBoost | ✅ Complete | Initial ML pipeline execution. |
| **Phase 3.5** | Audit Remediation | ✅ Complete | Fixing temporal leakages, H3 bugs, and FP errors. |
| **Phase 3.6** | Final Deduplication | ✅ Complete | 4-Tier upstream duplicate removal -> `dataset_v3`. |
| **Phase 4** | **Hybrid AVM** | 🟢 **ACTIVE** | Inject Deterministic signals into ML to beat 12% drift. |
| **Phase 5** | Explainability | Planned | Generate SHAP values and human-readable traces for Hybrid AVM. |
| **Phase 6** | Production AVM | Planned | API deployment, MLOps, CI/CD, and real-time inference. |
| **Phase 5.5A** | Broker Copilot Architecture Discovery | ✅ Complete | Workspace Memory, Property/Scenario Memory, Audit Trail Design. |
| **Phase 5.5B.1** | Copilot Persistence Layer | ✅ Complete | Workspace, Chat, Message, Property State, Scenario State persistence. |
| **Phase 5.5B.1R** | Persistence Recovery & Hardening | ✅ Complete | User Ownership, Soft Delete, Audit Trail, Scenario Lineage. |
| **Phase 5.5B.1R.1** | Production Blockers Resolution | ✅ Complete | JWT Auth, Broker Session Ownership, Postgres Bootstrap Fix, Docker Validation. |
| **Phase 5.5B.2** | Tool Layer Tools 1 + 2 | ✅ Complete | Valuation Tool & Explainability Tool implemented. |
| **Phase 5.5B.2A** | Broker Adapter Repair | ✅ Complete | Broker Adapter routed through Tools 1 + 2; direct pricing route usage removed. |
| **Phase 5.5B.3** | Tool Layer Tools 3 + 4 | ✅ Complete | Comparable Tool and Fairness Tool implemented as Truth Layer adapters. |
| **Phase 5.5B.4** | Tool Layer Tool 5 | Complete | What-if Tool implemented as an immutable ephemeral sandbox over TruthLayer adapters. |
| **Phase 5.5B.5** | Tool Layer Tool 6 | Complete | Negotiation Tool implemented with traceable positions, grounded offer bands, optional What-if sensitivity evidence, audit persistence, and Docker validation. |
| **Phase 5.5B.6** | Tool Layer Tool 7 | Complete | Investment Tool implemented with traceable opportunity positions, evidence-backed strengths and risks, optional What-if sensitivity evidence, audit persistence, and Docker validation. |
| **Phase 5.5B.7** | Tool Layer Tool 8 | Complete | Market Insight Tool implemented as traceable descriptive analytics over persisted TruthLayer snapshots, prediction logs, shadow logs, comparable evidence, workspace history, and tool events. |

### Latest Tool Layer Baseline

The implemented baseline is now **through Phase 5.5B.7: Market Insight Tool**.
Tools 1-8 are complete. Tool 8 is descriptive analytics only; it does not
forecast future prices or generate synthetic trends.

---

# Repository Architecture Overview

High-level repository tree:

```text
mobile computing project/
├── PROJECT_MASTER_STATE.md                 # This project memory document.
├── TECHNICAL_AUDIT_REPORT.md               # Older audit; partially superseded by current implementation.
├── valorai-runtime-assets*.png             # Visual/runtime asset screenshots.
└── pf_scraper/
    ├── pf_scraper/                         # PropertyFinder scraper package.
    ├── provider/                           # Extraction/probing utilities and sample Next.js payloads.
    ├── data/, data_eg/, csv_output/        # Scraped JSONL/CSV outputs.
    ├── 01_clean_all.py                     # CSV cleaning/consolidation script.
    ├── requirements.txt                    # Scraper Python deps.
    └── fair-price-eg/                      # Main application.
        ├── backend/                        # FastAPI application.
        │   ├── app/api/                    # FastAPI routes and API schemas.
        │   ├── app/broker/                 # Broker orchestration and reasoning engine.
        │   ├── app/comps/                  # Comparable retrieval and outlier guardrails.
        │   ├── app/core/                   # Settings, logging, errors, observability, feature normalization.
        │   ├── app/db/                     # DB session, SQL, migrations.
        │   ├── app/geo/                    # Area resolution.
        │   ├── app/pricing/                # Valuation, confidence, filters, weights, explainability.
        │   ├── app/scripts/                # Import, smoke, performance, query-plan scripts.
        │   └── app/tests/                  # Backend unit/integration/regression tests.
        ├── frontend/                       # Current React/Vite product frontend.
        │   ├── src/api/                    # HTTP client and envelope contracts.
        │   ├── src/app/                    # Providers and routes.
        │   ├── src/components/             # Shared UI, nav, orb, valuation components.
        │   ├── src/features/               # Nexus, Broker, Valuation, Pulse, Assets, Vault screens.
        │   ├── src/hooks/                  # React Query valuation hook.
        │   ├── src/services/               # Valuation service.
        │   ├── src/store/                  # Zustand stores.
        │   └── src/types/                  # Frontend valuation contracts.
        ├── frontend old/                   # Legacy CRA app; appears obsolete.
        ├── data/                           # Clean CSV inputs for bootstrap.
        ├── db/seed/                        # Empty seed CSV placeholders.
        ├── docker/postgres/init/           # Postgres/PostGIS init SQL.
        ├── docs/STAGING_RUNBOOK.md         # Staging operations runbook.
        ├── docker-compose.yml              # db, db-bootstrap, backend, frontend, staging-smoke.
        ├── .env.example                    # Empty root env example; needs correction.
        └── .env.staging.example            # Staging Compose env template.
```

Service boundaries:

| Boundary | Responsibility | Current Status |
|---|---|---|
| Scraper package | Retrieve PropertyFinder Egypt listing/project payloads into JSONL/CSV. | Implemented but operational maturity unclear; many exploratory scripts remain. |
| Backend API | Rent valuation, broker reasoning, health/metrics. | Implemented and tested. |
| Database | PostgreSQL/PostGIS storage of areas/listings and geospatial indexes. | Compose/init SQL implemented. |
| Frontend | Mobile-first valuation workflow and cinematic intelligence UI. | Partially implemented. |
| Broker reasoning | Deterministic tool orchestration and governed analytical narration. | Backend reasoning and initial BrokerScreen stream/reason integration implemented; polish, persistence, and visual QA remain. |
| Deployment | Docker Compose staging-like stack. | Implemented for local/staging; production missing. |

Repository hygiene observations:

- `git status` from the root shows `pf_scraper/`, `TECHNICAL_AUDIT_REPORT.md`, and images as untracked. This may be intentional workspace packaging, but it needs verification before production branching/release management.
- `frontend old/` is likely dead code and should be archived outside the active app or removed after confirmation.
- `db/seed/*.csv` under `fair-price-eg` are empty; actual bootstrapping uses `fair-price-eg/data/*.csv`.

---

# System Architecture

## Runtime Flow: Deterministic Valuation

```text
React ValuationScreen
  -> valuationService.requestFairRentPrice()
  -> Axios HTTP client with X-Request-ID and X-Correlation-ID
  -> FastAPI POST /v1/rent/fair-price
  -> Pydantic validation
  -> nearest_area(PostGIS)
  -> fetch_comps(SQL tier_comps hierarchy/radius retrieval)
  -> hard_guardrails()
  -> mad_filter()
  -> compute_weights()
  -> weighted_median() and weighted_quantile()
  -> compute_confidence()
  -> build_explanation() and build_explanation_trace()
  -> SuccessResponse[RentFairPriceResponse]
  -> Frontend valuation, comparables, confidence, explainability panels
```

## Runtime Flow: Broker Reasoning

```text
POST /v1/broker/reason or /analyze or /chat
  -> BrokerOrchestrator
  -> ReasoningStageRuntime
      1. classify_intent
      2. build_reasoning_plan
      3. execute_tools
      4. assemble_context
      5. generate_narration
      6. validate_grounding
      7. finalize_response
  -> Deterministic broker tools
      - ValuationAnalysisTool
      - ComparableAnalysisTool
      - ExplainabilityTool
      - DistrictIntelligenceTool
      - ConfidenceAnalysisTool
  -> BrokerContextAssembler
  -> LLMNarrationRuntime
      - deterministic formatter by default
      - OpenAI/Gemini provider adapters present but disabled unless configured
  -> GroundingValidator
  -> ResponseGovernanceLayer
  -> BrokerOrchestrationResponse with events and reports

POST /v1/broker/stream
  -> StreamingResponse event generator
  -> async queue for BrokerStageEvent objects
  -> background orchestration worker with SessionLocal DB session
  -> BrokerOrchestrator.reason(..., event_handler=enqueue_trace_event)
  -> BrokerTrace.add_event forwards runtime events immediately
  -> SSE events:
      - stage_started
      - stage_progress
      - tool_started / tool_completed
      - confidence_update
      - narration_chunk
      - validation
      - governance_update / governance_check
      - stream_completed
      - final_response
  -> frontend brokerService parses the stream and BrokerScreen renders pipeline/narration state
```

Current streaming behavior:

- `/v1/broker/stream` now streams runtime trace events through an asyncio queue instead of waiting for a precomputed response.
- Each event receives stream metadata in `payload.stream_event_index` and `payload.stream_elapsed_ms`.
- Final response delivery is separated from `stream_completed`; the final SSE payload is the governed `BrokerOrchestrationResponse`.
- Governance and grounding remain inside the normal orchestrator lifecycle; streaming does not bypass deterministic authority.
- Client disconnect is detected, but orchestration cancellation is not fully propagated into the background worker. This is a remaining implementation limitation.

## Database Flow

```text
CSV data under fair-price-eg/data
  -> app.scripts.load_rent_csv
  -> listings_staging
  -> areas and listings
  -> PostGIS geometry/geography indexes
  -> tier_comps.sql retrieval
  -> API valuation response
```

## Frontend Flow

```text
AppProviders
  -> React Query provider
  -> BrowserRouter
  -> AppShell
      -> TopNav, BottomNav, ScreenTransition
      -> NexusScreen
      -> BrokerScreen
      -> ValuationScreen
      -> PulseScreen
      -> AssetsScreen
      -> VaultScreen
```

Architecture components:

| Component | Present? | Status |
|---|---:|---|
| FastAPI backend | Yes | Production-shaped, tested. |
| PostgreSQL | Yes | Compose-backed. |
| PostGIS | Yes | Used for area resolution and comparable distance/radius queries. |
| Vector DB | No | Not implemented. |
| Graph DB | No | Not implemented. |
| Redis/cache | No | Not implemented. |
| Queue/background workers | No | No Celery/RQ/Sidekiq-style system; only scripts and Compose bootstrap. |
| RAG | No | Not implemented. |
| LLM providers | Partial | OpenAI/Gemini adapters exist; disabled by default; needs mocked and live verification. |
| Streaming | Partial | Runtime SSE streaming is implemented for broker reasoning; WebSocket support, provider-native token streaming, and cancellation-aware worker execution remain incomplete. |
| Authentication | No | Not implemented. |
| Authorization/RBAC | No | Not implemented. |
| Observability | Partial | In-process metrics/tracing/logging; no external stack. |

---

# Backend Status

Backend root: `pf_scraper/fair-price-eg/backend`

Runtime dependencies:

| Dependency | Version |
|---|---|
| FastAPI | `0.115.6` |
| Uvicorn | `0.34.0` |
| SQLAlchemy | `2.0.36` |
| psycopg | `3.2.3` |
| python-dotenv | `1.0.1` |
| pydantic-settings | `>=2.0.0` |

## API Layer

| Item | Status | Notes |
|---|---|---|
| `GET /health` | Complete | Liveness envelope. |
| `GET /health/ready` | Complete | DB readiness with standard error envelope. |
| `GET /health/metrics` | Complete | In-process metrics snapshot. |
| `GET /health/operational` | Complete | SLO summary, recent events, distributions. |
| `POST /v1/rent/fair-price` | Complete | Main deterministic valuation API. |
| `POST /v1/broker/analyze` | Complete | Backward-compatible broker analysis. |
| `POST /v1/broker/chat` | Complete | Broker chat turn. |
| `POST /v1/broker/intent` | Complete | Lightweight intent classification. |
| `POST /v1/broker/reason` | Complete | Structured reasoning pipeline endpoint. |
| `POST /v1/broker/stream` | Complete initial | Runtime SSE stream forwards live broker trace events and final governed response. |
| `GET /v1/broker/session/{session_id}` | Complete | In-memory broker session snapshot. |

Production readiness: 78%

Risks:

- `POST /v1/rent/fair-price` still contains dense business orchestration in the route function.
- No authentication/authorization around broker or pricing endpoints.
- Rate limiting is in-process only and not suitable for multi-instance production without external coordination.

## Deterministic Valuation Engine

Purpose: produce fair monthly rent estimates from comparable evidence.

Implemented:

- Area resolution through PostGIS nearest-area lookup.
- Hierarchy-aware comparable retrieval through `tier_comps.sql`.
- Guardrails for price, size, and price-per-sqm.
- MAD outlier filtering.
- Weighted median fair price.
- Weighted quantile fair range.
- Confidence scoring.
- Structured explanation traces.
- Feature similarity support for amenities, furnishing, floor, compound, view, and building quality.
- Regression and hardening tests.

Implementation level: HIGH

Production readiness: 80%

Missing or partial:

- No persisted valuation audit table.
- No model/version stamp in valuation response beyond code behavior.
- No admin tooling for area/listing data quality inspection.
- No service-layer extraction from route orchestration.
- Market coverage quality needs verification against real production data volumes.

## Comparable Retrieval Engine

Implemented:

- `fetch_comps()` loads SQL and runs deterministic tiers.
- `tier_comps.sql` supports scopes: same area, same district, nearby districts, same city, same governorate.
- Uses PostGIS `ST_DWithin` and `ST_Distance`.
- Deterministic ordering by distance, recency, price, listing id.
- Tests verify fallback sequence, tier parameters, and deterministic behavior.

Production readiness: 78%

Risks:

- Query-plan performance under production-scale data needs ongoing verification.
- Cache layer absent; repeated hot-area queries will hit DB directly.
- Data quality depends heavily on scraper/import normalization.

## Pricing, Filters, and Weighting

Implemented modules:

| Module | Purpose | Status |
|---|---|---|
| `pricing/weights.py` | Weighted quantile and weighted median. | Complete. |
| `pricing/estimator.py` | Comparable weights from distance, size, recency, bathrooms, same-area, required match, features. | Complete. |
| `pricing/filters.py` | MAD filtering, including price-per-sqm preference. | Complete. |
| `comps/outliers.py` | Hard guardrails. | Complete. |
| `pricing/confidence.py` | Confidence score/label. | Complete. |
| `pricing/explain.py` | Human and structured explanation output. | Complete. |
| `pricing/feature_similarity.py` | Feature-level similarity scoring. | Complete. |

Risks:

- The system is deterministic, not statistically trained; do not describe it as ML model pricing.
- Confidence is heuristic/deterministic and should be framed as operational confidence, not probabilistic certainty.

## Broker Orchestration and Reasoning

Implemented Phase 2A/2B backend systems:

| Subsystem | Status | Notes |
|---|---|---|
| BrokerOrchestrator | Complete for current reasoning pipeline | Central pipeline in `broker/orchestrator/core.py`; accepts a trace event handler for live streaming. |
| Typed tool registry | Complete | Tools are selected by intent and valuation request presence. |
| Context assembler | Complete | Builds token-budgeted deterministic context and evidence refs. |
| Grounding validator | Complete | Checks authoritative values and evidence/comparable references. |
| Session store | Partial | In-memory only; not persistent or distributed. |
| Intent classifier | Complete initial | Rule-assisted, low latency; no LLM routing. |
| Reasoning plan builder | Complete initial | Emits typed stages, selected tools, governance checks. |
| Stage runtime | Complete initial | Emits stage start/progress/completion/failure events, timings, and metrics; soft timeout only. |
| Narration runtime | Partial | Emits safe narration progress chunks and final validated response chunks; deterministic formatter default; LLM adapters present but not live-verified. |
| Prompt system | Partial | Modular prompt catalog exists. |
| Governance layer | Complete initial | Checks forbidden output, numeric consistency, confidence consistency, grounding. |
| Dialogue engine | Minimal | Supplies continuity metadata; no rich conversation policy yet. |
| Streaming event system | Complete initial for SSE | `/v1/broker/stream` forwards live `BrokerTrace` events through an async queue and emits `stage_progress`, `confidence_update`, `narration_chunk`, `governance_update`, `stream_completed`, and `final_response`. WebSocket support is not implemented. |

Production readiness: 60%

Key deterministic authority rule:

- LLMs must not call tools.
- LLMs must not generate valuations independently.
- LLMs must not invent comparables, confidence, or pricing facts.
- The deterministic backend remains the authoritative valuation source.

## Authentication and Authorization

Status: Not implemented.

Missing:

- User identity.
- API keys or OAuth/JWT.
- RBAC.
- Tenant isolation.
- Broker/investor workspace boundaries.
- Audit trails by actor.

Production readiness: 10%

Risk: CRITICAL for any public/shared environment.

## Telemetry, Logging, and Metrics

Implemented:

- Request IDs and correlation IDs.
- Structured JSON logging option.
- Middleware latency logging.
- Request body size enforcement.
- Request timeout handling.
- In-process rate limiter.
- In-process metrics registry.
- Endpoint/stage/tool timing.
- Slow request and slow query events.
- Broker reasoning stage events.
- Broker stream event counters, duration metrics, completion/failure/disconnect counters.
- Operational summary endpoint.

Production readiness: 72%

Missing:

- OpenTelemetry exporter.
- Prometheus endpoint/exporter.
- Log aggregation.
- Alerting.
- Distributed tracing.
- Persistent audit logs.

## Background Jobs and Queues

Status: Mostly absent.

Implemented:

- Compose `db-bootstrap` one-shot import service.
- Python scripts for import, smoke, performance baseline, and query-plan audit.
- In-process background orchestration worker is used only inside `/v1/broker/stream`; it is not a durable job system.

Missing:

- Job queue.
- Scheduled scrapes/imports.
- Durable async background worker.
- Retry/dead-letter handling.
- Operational job dashboard.

Production readiness: 25%

---

# Frontend Status

Frontend root: `pf_scraper/fair-price-eg/frontend`

Stack:

| Technology | Usage |
|---|---|
| React 19 | Main UI framework. |
| Vite 6 | Build/dev server. |
| TypeScript | Type checking. |
| React Router | Client routing. |
| TanStack React Query | Valuation mutation/retry/cancel flow. |
| Zustand | Local state stores. |
| Axios | Standard JSON API client. |
| Fetch/ReadableStream | Broker SSE streaming client. |
| Framer Motion | Cinematic transitions. |
| Tailwind CSS v4 | Styling. |
| Vitest + Testing Library | Frontend tests. |

Implemented screens:

| Screen | Path | Status | Integration |
|---|---|---|---|
| Nexus | `/nexus` | Partial | Cinematic home/status screen; mostly static, links to valuation. |
| Broker | `/broker` | Integrated initial | Broker Intelligence Terminal calls `/v1/broker/stream`, falls back to `/v1/broker/reason`, renders staged pipeline events, partial narration chunks, confidence, governance, and comparable evidence. |
| Valuation | `/valuation` | Strongest screen | Real API integration with `/v1/rent/fair-price`. |
| Pulse | `/pulse` | Placeholder | Simulated map/zone intelligence with hardcoded data and external image URL. |
| Assets | `/assets` | Thin alias | Renders `ValuationScreen`; not a true asset management screen. |
| Vault | `/vault` | Placeholder | Static intelligence/report UI; no persistence/API integration. |

Frontend completed work:

- API envelope contracts.
- Axios client with request/correlation headers.
- Error normalization.
- Valuation service and React Query hook.
- Cancellable valuation mutation.
- Zustand valuation/broker/navigation/overlay stores.
- Responsive valuation input form.
- Result card with confidence visualization.
- Comparable evidence panel.
- Explainability panel.
- Broker TypeScript contracts for Phase 2B response and stream event shapes.
- Broker service methods for `/v1/broker/reason`, `/v1/broker/chat`, and `/v1/broker/stream`.
- Fetch-based SSE parser with final-response callback and stream event callbacks.
- Broker Intelligence Terminal with command input, cancellation, staged reasoning pipeline, partial narration compatibility, confidence visualization, governance checks, and `/v1/broker/reason` fallback.
- Tests for contracts, valuation service, broker service, store, hook, valuation card, comparable panel, explainability panel.
- Production build passes.

Frontend missing work:

- Broker screen does not fetch `/v1/broker/session/{session_id}`; it passes a local session id but does not render persisted session history.
- Broker streaming UI is implemented infrastructure, not yet fully polished cinematic UX.
- No browser/mobile visual QA was executed in the current verification pass.
- No WebSocket streaming client; current implementation is SSE over `fetch`.
- No map/location picker; lat/lng are manual numeric inputs.
- React authentication UI is implemented for Sprint 1 P0-1. Enterprise RBAC/admin policy remains future work.
- No saved assets/portfolio persistence.
- No report generation/download integration.
- No real Pulse market/district data integration.
- No admin or data quality UI.
- No accessibility audit found.

Production readiness: 56%

Risk notes:

- Some UI copy implies live intelligence or synced systems that are not backed by APIs. Treat those screens as prototype/cinematic placeholders.
- `PulseScreen` references a remote Googleusercontent image. Production should own or proxy critical assets.
- `BrokerScreen` is now interactive, but its staged terminal should still be treated as an initial implementation until visual QA, accessibility review, and production session persistence are added.

---

# AI/ML Systems

## Deterministic Valuation Logic

Status: Implemented.

This is the project’s mature intelligence core. It is deterministic and evidence-based, not a trained ML model.

Implemented:

- Comparable retrieval.
- Outlier filtering.
- Weighted median pricing.
- Quantile range.
- Confidence score.
- Explanation trace.
- Feature similarity.
- Deterministic regression tests.

Limitations:

- No trained ML model.
- No continuous learning pipeline.
- No backtesting dashboard.
- No model registry.
- No calibration monitoring against closed transactions.

## Broker Reasoning/NLP

Status: Partial.

Implemented:

- Rule-assisted intent classifier.
- Typed reasoning plan.
- Stage execution runtime.
- Runtime `stage_progress`, `confidence_update`, `governance_update`, and `narration_chunk` events.
- Live SSE orchestration stream for broker reasoning.
- Governed narration boundary.
- Prompt catalog.
- Deterministic fallback formatter.
- Response governance.
- OpenAI and Gemini HTTP provider adapters.

Missing:

- Live integration tests for providers.
- Provider-native token streaming to frontend. Current stream chunks are orchestrator/narration lifecycle chunks and validated final response fragments.
- Conversation memory beyond lightweight in-memory session snapshot.
- Production prompt evaluation suite.
- Red-team tests for LLM hallucination beyond current governance unit tests.

## Embeddings and RAG

Status: Not implemented.

No embedding model, vector database, document chunking, semantic retrieval, or RAG pipeline was found.

## Reranking

Status: Not implemented.

Comparable ranking is deterministic weighted scoring, not neural reranking.

## Recommendation Systems

Status: Not implemented.

No personalized investment recommendation engine is present. Vault and Pulse UI elements suggest future intent but are static.

## Explainability

Status: Implemented for deterministic valuation; partial for broker reasoning.

Implemented:

- Human-readable valuation explanation.
- Structured `explanation_trace`.
- Reason codes.
- Feature similarity traces.
- Broker grounding report.
- Broker governance report.

Missing:

- SHAP or model explainability, because no trained model exists.
- Explainability audit persistence.

---

# Database Architecture

Database: PostgreSQL with PostGIS.

Implemented tables from SQL:

| Table | Purpose |
|---|---|
| `areas` | Hierarchical geographic areas, levels 1-4, parent relationship, center geometry, optional polygon geometry. |
| `listings_staging` | Import staging for CSV/listing data. |
| `listings` | Normalized listing table with price, category, period, property details, geometry, area, features. |

Important columns:

- `areas.area_id`, `name`, `level`, `parent_area_id`, `geom`, `center_geom`, `fallback_radius_m`
- `listings.listing_id`, `category`, `period`, `price_egp`, `property_type`, `bedrooms`, `bathrooms`, `size_sqm`, `lat`, `lng`, `geom`, `area_id`, `scraped_at_utc`
- Feature columns: `amenities`, `normalized_amenities`, `unknown_amenity_codes`, `furnishing_status`, `floor_number`, `compound_name`, `view_type`, `building_quality`, `feature_raw`

Indexes:

| Index | Purpose |
|---|---|
| `ux_areas_parent_level_name` | Unique area hierarchy names. |
| `ix_areas_parent` | Area hierarchy traversal. |
| `ix_areas_center_gist` | Geometry nearest-area support. |
| `ix_areas_center_geog_gist` | Geography distance support. |
| `ix_areas_geom_gist` | Polygon geometry support when present. |
| `ix_listings_geom_gist` | Listing geometry search. |
| `ix_listings_geom_geog_gist` | Listing geography radius search. |
| `ix_listings_category_period_area` | Market/category/area filtering. |
| `ix_listings_area_type_bedrooms` | Area/type/bedroom matching. |
| `ix_listings_match_area_recency` | Tier 1 matching and recency. |
| `ix_listings_market_snapshot` | Market snapshot/as-of query support. |
| `ix_listings_scraped_at_utc` | Recency/as-of support. |

Constraints:

- `areas.level` check.
- `areas.parent_area_id` self-reference guard and FK.
- `listings.listing_id` primary key.
- `listings.price_egp > 0`.
- `listings.area_id` FK to `areas`.

Vector DB: Not present.

Graph DB: Not present.

Caching: Not present.

Query optimization status:

- SQL and indexes are intentionally designed for PostGIS retrieval.
- `query_plan_audit.py` exists to inspect plan health.
- Production-scale query performance still needs continuous verification.

---

# Infrastructure & DevOps

## Docker/Compose

`docker-compose.yml` defines:

| Service | Status | Purpose |
|---|---|---|
| `db` | Implemented | PostGIS 16-3.4 database with healthcheck and persisted volume. |
| `db-bootstrap` | Implemented | Runs `python -m app.scripts.load_rent_csv` against `./data`. |
| `backend` | Implemented | FastAPI app served by Uvicorn, waits for DB/bootstrap. |
| `frontend` | Implemented | Nginx-served Vite build, proxies `/v1` and health routes. |
| `staging-smoke` | Implemented | Optional profile to run smoke script. |

## Environments

| File | Status | Notes |
|---|---|---|
| `fair-price-eg/.env.example` | Weak | Empty; should be fixed. |
| `fair-price-eg/.env.staging.example` | Good | Contains staging Compose settings. |
| `backend/.env.example` | Good | Backend runtime settings. |
| `frontend/.env.example` | Good | Vite API settings. |

## CI/CD

Status: Not found.

No `.github/workflows`, GitLab CI, Azure Pipelines, or equivalent CI/CD config was found.

Required:

- Backend unit/integration test job.
- Frontend typecheck/test/build job.
- Docker image build job.
- Migration/schema verification job.
- Security/dependency scanning.

## Deployment Readiness

Staging-like local deployment: 70%

Production deployment: 35%

Missing:

- Managed secrets strategy.
- TLS/ingress config.
- Production database migration workflow.
- Rollback strategy.
- Horizontal scaling plan.
- External monitoring/logging.
- Auth service.
- Backup/restore runbook.

---

# APIs & Contracts

## Public API Routes

| Method | Path | Contract Status | Frontend Integration |
|---|---|---|---|
| GET | `/health` | Stable | Proxied by nginx; not directly surfaced as UI status except static text. |
| GET | `/health/ready` | Stable | Proxied by nginx. |
| GET | `/health/metrics` | Internal/staging | Not integrated. |
| GET | `/health/operational` | Internal/staging | Not integrated. |
| POST | `/v1/rent/fair-price` | Stable and tested | Integrated in frontend valuation flow. |
| POST | `/v1/broker/analyze` | Stable enough for backend clients | Not integrated in frontend. |
| POST | `/v1/broker/chat` | Stable enough for backend clients | Not integrated in frontend. |
| POST | `/v1/broker/intent` | New Phase 2B | Not integrated in frontend. |
| POST | `/v1/broker/reason` | New Phase 2B | Integrated as non-streaming fallback in `BrokerScreen`. |
| POST | `/v1/broker/stream` | Runtime SSE implemented and tested | Integrated in `BrokerScreen` through `streamBrokerReason` fetch/ReadableStream parser. |
| GET | `/v1/broker/session/{session_id}` | New/partial | Not integrated in frontend. |

Contract strengths:

- Pydantic schemas.
- Standard success/error envelopes.
- Stable enum tests.
- OpenAPI examples for pricing.
- Frontend TypeScript valuation contracts match pricing response shape.
- Frontend TypeScript broker contracts mirror the current Phase 2B response/event shape.
- Backend streaming lifecycle test covers broker SSE event types and final response delivery.
- Frontend broker service test covers POST SSE parsing and final response callback.

Contract gaps:

- No generated client from OpenAPI.
- No end-to-end browser contract test between a running backend and running frontend.
- `/v1/broker/intent` and `/v1/broker/session/{session_id}` are not yet surfaced in the UI.
- No WebSocket contract exists.
- API versioning strategy beyond `/v1` not documented.

---

# Observability & Monitoring

Implemented:

- Request/correlation ID middleware.
- JSON log mode.
- Request completion logs.
- Standard error envelopes with request metadata.
- Request timeout and oversized body handling.
- Slow request events.
- DB query timing via SQLAlchemy events.
- Slow query events.
- In-process counters/histograms/events.
- `/health/metrics`.
- `/health/operational`.
- Broker stage events, tool events, grounding validation events, governance events.
- Broker stream metrics for event counts, duration, completion, failures, and disconnects.
- Frontend propagates request/correlation IDs and displays errors/request IDs.
- Frontend broker service sets `X-Request-ID` for SSE stream requests.

Operational maturity: 72%

Limitations:

- Metrics reset on process restart.
- No external metrics backend.
- No traces across services.
- No alerting.
- No audit retention.
- No dashboard config.

Recommended next observability step:

- Add OpenTelemetry instrumentation and export traces/metrics/log correlation to a real backend such as Prometheus/Grafana plus OTLP collector, or another selected observability stack.

---

# Security Review

Implemented protections:

- Pydantic request validation.
- Standardized error responses.
- CORS validation and production wildcard guard.
- In-process rate limiting.
- Request body size limit.
- Request timeout.
- Security headers in frontend nginx:
  - `X-Content-Type-Options`
  - `X-Frame-Options`
  - `Referrer-Policy`
  - `Permissions-Policy`
- Backend hides stack traces via error handler.

Major gaps:

| Risk | Severity | Notes |
|---|---|---|
| JWT Authentication | RESOLVED | HS256 Bearer JWT verifies sub, iss, aud, iat, exp claims. (Fixed Phase 5.5B.1R.1) |
| No authorization/RBAC | CRITICAL | Tenant API isolation exists via JWT, but future explicit organization membership tables are required. |
| No user/tenant model | HIGH | Cannot safely support multi-user workflows. |
| No secrets manager | HIGH | Env files only; staging example contains placeholder password. |
| In-process rate limiter | MEDIUM | Not correct for multi-instance production. |
| No data privacy model | HIGH | Listings may contain scraped URLs/images/location data; compliance needs review. |
| No dependency scanning | MEDIUM | No CI/security tooling found. |
| External image in Pulse UI | LOW-MEDIUM | Production asset control and privacy should be reviewed. |

Security production readiness: 75%

---

# Technical Debt

| Item | Severity | Evidence | Recommended Action |
|---|---|---|---|
| No authn/authz | CRITICAL | No auth modules/routes/config found. | Add authentication, authorization, tenant model, and API protection. |
| LLM provider not live-verified | HIGH | Adapters exist; no mocked/live tests found. | Add mocked provider tests and feature-flagged staging smoke. |
| No CI/CD | HIGH | No workflow files found. | Add automated test/build/security gates. |
| Streaming worker cancellation gap | MEDIUM-HIGH | `/v1/broker/stream` detects disconnects but does not propagate a cancellation token into the background orchestration worker. | Add cancellation-aware execution context or cooperative cancellation checks. |
| Broker streaming UX polish | MEDIUM | Broker terminal is integrated and tested at service level, but no browser/mobile visual QA was run. | Add Playwright/mobile verification, accessibility review, and motion polish. |
| Empty root `.env.example` | MEDIUM | `fair-price-eg/.env.example` has no content. | Populate with Compose defaults or remove in favor of staging template. |
| Legacy frontend archive | MEDIUM | `frontend old/` contains CRA app. | Move outside repo or document as archived. |
| Scraper experimental scripts | MEDIUM | `provider/test3.py`, probe scripts, duplicate HTTP clients. | Separate production scraper package from research utilities. |
| In-memory sessions/metrics | MEDIUM | Broker session and metrics not persisted/distributed. | Move to Redis/Postgres or explicit single-instance note. |
| Dense pricing route | MEDIUM | `/fair-price` route orchestrates many business steps. | Extract service layer for valuation pipeline. |
| No migration framework | MEDIUM | SQL files exist, no Alembic workflow. | Add Alembic or documented migration runner. |
| No cache | MEDIUM | Hot queries hit DB repeatedly. | Add Redis or DB-level materialization after profiling. |
| Static/cinematic UI claims | LOW-MEDIUM | Pulse/Vault show hardcoded metrics. | Gate behind "prototype" state or integrate real APIs. |

---

# Known Issues

| Issue | Status | Impact |
|---|---|---|
| Root project git state shows main app as untracked | Needs Verification | Release/branch discipline may be broken in this workspace. |
| Empty seed CSVs under `fair-price-eg/db/seed` | Confirmed | Could confuse future agents; actual bootstrap uses `fair-price-eg/data`. |
| `frontend old` remains in repo | Confirmed | Increases confusion and audit noise. |
| No auth/security boundary | Confirmed | Blocks production exposure. |
| No vector/RAG/ML systems | Confirmed | Do not claim semantic AI market search or learned valuation. |
| LLM adapters lack test coverage | Confirmed by inspected tests | Risk of runtime integration mismatch. |
| Provider token streaming is not verified | Needs Verification | Current frontend stream consumes broker runtime chunks, not proven provider-native token deltas. |
| Broker stream worker is not cancellation-aware after disconnect | Confirmed by route code | Disconnected clients stop receiving events, but the worker may continue until orchestration completes. |
| Broker sessions are in-memory and `/session` is not frontend-integrated | Confirmed | Analytical continuity is single-process only and not production durable. |
| PostGIS integration test is skipped unless env is set | Confirmed by test marker/run result | Local green suite does not prove live DB integration by default. |

---

# Missing Features

Required for production:

- Authentication and authorization.
- Tenant/user/workspace model.
- Persistent broker sessions.
- Persistent valuation/audit history.
- CI/CD.
- Production migration workflow.
- Secrets management.
- External observability stack.
- Backup/restore.
- Production deployment manifests.
- API abuse protection beyond in-process rate limiting.

Required for scalability:

- Distributed cache or query result cache.
- Multi-instance-safe rate limiting.
- Background job system.
- Incremental data ingestion.
- Query performance monitoring on production-size data.
- Database partitioning/materialization strategy if listing volume grows.

Required for enterprise readiness:

- Admin/data quality dashboard.
- Audit log by actor.
- Role-based access control.
- Data lineage from scrape to valuation.
- Report generation.
- SLA/SLO dashboard.
- Compliance/privacy review.

Required for AI quality:

- Broker prompt/evaluation suite.
- Mocked and live provider tests.
- Token accounting integration tests.
- Hallucination/red-team test cases.
- Provider-native streaming support and token accounting.
- More complete frontend broker evidence overlays and governance status UX.

Required for UX quality:

- Broker chat/reasoning UI polish beyond the current integrated terminal.
- Staged reveal UX refinement and optional WebSocket support if SSE is insufficient.
- Location picker/map.
- Portfolio/assets screens backed by API.
- Pulse screen backed by district/market data.
- Vault/report workflows backed by storage.
- Accessibility audit and improvements.

---

# Production Readiness Assessment

| Area | Score | Rationale |
|---|---:|---|
| Backend | 80% | Strong deterministic API, tests, contracts, observability, and live broker SSE stream. Missing auth, persistence for broker sessions, production ops. |
| Frontend | 56% | Valuation workflow works and builds; broker terminal is integrated with stream/reason endpoints; several screens remain placeholders and broker UX still needs polish. |
| AI systems | 47% | Deterministic reasoning is solid and governed streaming chunks exist; LLM/RAG/ML production maturity is low. |
| Database | 72% | Good schema/index posture; production data quality and migration process need work. |
| Infrastructure | 62% | Compose stack/runbook exists; no CI/CD or production platform config. |
| Observability | 72% | In-process observability strong for staging, now including stream event metrics; no external monitoring/tracing. |
| Security | 35% | Validation/rate limits exist; no authn/authz/secrets maturity. |
| Deployment | 55% | Dockerized staging path; production readiness incomplete. |

Overall production readiness: 85%

Readiness classification: Stable governed deterministic intelligence platform. Foundation (persistence, auth, docker) highly mature. Frontend and LLM integration pending.

---

# Roadmap

## Immediate Next Steps

1. Add mocked OpenAI/Gemini provider tests and feature-flagged staging smoke checks.
2. Add browser/mobile visual QA for the Broker Intelligence Terminal streaming states.
3. Add cancellation-aware broker stream execution.
4. Add authentication/authorization and tenant/API protection.
5. Add GitHub Actions or equivalent CI for backend and frontend checks.
6. Persist broker sessions and valuation history.
7. Populate root `.env.example`.
8. Remove/archive `frontend old` after confirmation.

## Short-Term Roadmap

- Copilot Orchestrator
- LLM Integration
- Flutter Frontend
- Production Launch
- Update pre-existing valuation regression tests and collection-broken spatial confidence test.
- Integrate frontend web clients to send bearer JWTs and broker workspace context.
- Inject JWT_SECRET from a managed secret store for production.
- Implement explicit workspace cascade restore semantics for child messages and assumptions.

## Mid-Term Roadmap

- Add user accounts, RBAC, workspace/tenant boundaries.
- Add saved assets/portfolio workflows.
- Add report generation and storage.
- Add data quality/admin dashboard.
- Add scheduled scraper/import pipeline with job tracking.
- Add production observability stack.
- Add evaluation suite for broker narration and hallucination prevention.

## Long-Term Roadmap

- Expand from residential rent to buy, commercial rent, and commercial sale using separate deterministic contracts.
- Build district intelligence APIs from real aggregated market metrics.
- Add optional learned models only after deterministic baselines and audit trails are stable.
- Add retrieval/semantic systems only where evidence corpus exists and can be governed.
- Build enterprise deployment with compliance, audit logs, backups, and incident response.

---

# Phase Completion History

## Pre-Phase / Data Collection

Completed:

- PropertyFinder scraper package.
- Egypt-specific provider extraction utilities.
- JSONL and CSV scraped data outputs.
- Cleaning script for CSV normalization.

Remaining:

- Production scraper scheduling.
- Scraper monitoring.
- Data lineage and quality dashboards.
- Separation of production scraper code from exploratory scripts.

## Phase 1: Deterministic Valuation Foundation

Completed:

- FastAPI application.
- PostgreSQL/PostGIS schema.
- Docker Compose stack.
- CSV bootstrap script.
- Area resolver.
- Comparable retrieval engine.
- Hierarchy-aware `tier_comps.sql`.
- Hard guardrails.
- MAD filtering.
- Weighted scoring.
- Weighted median and quantile valuation.
- Confidence scoring.
- Explainability and explanation traces.
- Feature normalization/similarity.
- Structured API envelopes.
- Error handling.
- Rate limiting/request limits/timeouts.
- Health/metrics/operational endpoints.
- Regression, hardening, and contract tests.

Remaining:

- Service-layer refactor.
- Production migrations.
- Persistent audit/history.
- External observability.
- Authentication.

## Phase 2A: Broker Orchestration Foundation

Completed:

- Broker routes.
- Broker orchestrator.
- Typed tool registry.
- Valuation/comparable/explainability/district/confidence broker tools.
- Controlled context assembler.
- Grounding validator.
- Lightweight session state.
- Broker telemetry events.
- Deterministic authority enforcement.
- Structured broker contracts.

Remaining:

- Persistent session storage.
- Superseded by Phase 2B live broker streaming integration; richer session workflows and persistence remain.

## Phase 2B: Structured Reasoning Engine

Completed:

- Typed intent classification engine.
- Reasoning plan generation.
- Formal stage runtime.
- Structured stage events.
- Governed narration runtime.
- Modular institutional prompt catalog.
- OpenAI/Gemini provider adapters.
- Response governance checks.
- Analytical dialogue continuity metadata.
- New endpoints: `/v1/broker/intent`, `/v1/broker/reason`, `/v1/broker/stream`.
- Reasoning observability counters/timings.
- Tests for broker reasoning and governance.

### Live Broker Streaming Integration

Completed in the current verified slice:

- `/v1/broker/stream` now performs true runtime SSE delivery through an async queue and background orchestration worker.
- `BrokerTrace` accepts an event handler and forwards live runtime events from the orchestrator.
- Streamed event lifecycle includes `stage_started`, `stage_progress`, `confidence_update`, `narration_chunk`, `governance_update`, `stream_completed`, and `final_response`.
- Narration runtime emits governance-safe progress chunks, and finalization emits validated narration chunks from the governed response.
- Frontend broker service parses POST SSE streams and returns the final `BrokerOrchestrationResponse`.
- `BrokerScreen` is integrated as a Broker Intelligence Terminal with live stage visualization, partial narration compatibility, cancellation, confidence/governance widgets, and `/v1/broker/reason` fallback.
- Backend and frontend tests verify the stream lifecycle and SSE parsing behavior.

Remaining:

- Provider integration tests.
- Token usage validation in staging.
- Provider-native token streaming validation.
- Cancellation-aware stream worker execution.
- Persistent broker sessions and session-history UI.
- Browser/mobile visual QA and streaming UX polish.
- Prompt evaluation suite.
- Advanced dialogue workflows.



## Phase 3A.1b & 3B: Governance and Visual Evidence

Completed:

- Deterministic geospatial governance hardening (Address normalization, aliases, canonical entities, polygon-first area resolution).
- Custom Deterministic Migration Runner (Replaced legacy volume-initialization).
- Visual Evidence Layer (Institutional comparable cards, confidence stack, spatial evidence map).
- Live SSE Streaming stabilization.

## Phase 5.5A: Broker Copilot Architecture Discovery

Completed:

- Workspace Memory
- Property Memory
- Scenario Memory
- Conversation Memory
- Assumptions Engine
- Audit Trail Design
- Future Organization Layer
- Future Tool Layer
- Future Copilot Orchestrator

## Phase 5.5B.1: Copilot Persistence Layer

Completed:

- Workspace
- Chat
- Message
- Property State
- Scenario State

## Phase 5.5B.1R: Persistence Recovery & Hardening

Completed:

- User Ownership (Tenant scoping for all Copilot entities)
- Soft Delete (for Workspaces, chats, scenarios, etc.)
- Audit Trail (decision_history, tool_events)
- Scenario Lineage (scenario_lineage durable append record)
- Durable Broker Session Storage (BrokerSessionStore)
- Recovery Design

## Phase 5.5B.1R.1: Production Blockers Resolution

Completed:

- Historical Migration Compatibility (005 and 006 idempotent preflights)
- JWT Authentication (HS256 Bearer Identity)
- Broker Session Ownership (Bound user, workspace, scenario)
- Workspace Cascade Restore (Child entity provenance)
- PostGIS Bootstrap Race Condition Fix
- Tenant Isolation (API and DB enforcement pass)
- Docker Validation

## Phase 5.5B.2: Tool Layer

Completed:

- Tool 1: Valuation Tool
- Tool 2: Explainability Tool
- Tool Audit Events (Persisted to tool_events)
- Valuation Snapshots (Tenant-scoped context saving)
- Scenario Overlay
- Truth Layer Integration (Router fallback hardening)
- Docker Validation (PASS)

## Phase 5.5B.2A: Broker Adapter Repair

Completed:

- Broker Adapter migrated to Tool 1 and Tool 2
- Direct pricing route usage removed from Broker Adapter path
- Grounded Truth Layer response flow
- Scenario Overlay
- Tenant Isolation
- Restart Recovery
- Docker Validation (PASS)

## Phase 5.5B.3: Comparable And Fairness Tools

Completed:

- Tool 3: Comparable Tool
- Tool 4: Fairness Tool
- Real Comparable Evidence Retrieval
- Existing Valuation Snapshot Replay
- Scenario Overlay Support
- Router-Owned Fairness Assessment
- Below / Within / Above Fair Value Statuses
- Tool Audit Events persisted to `tool_events`
- Tenant Isolation
- Backend and PostgreSQL Restart Recovery
- Fabricated comparable `listing_date = "Recent"` marker removed
- Live PostGIS Integration (`3 passed`)
- Docker Validation (PASS)

## Phase 5.5B.4: What-if Tool

Completed:

- Tool 5: What-if Tool
- Deterministic orchestration over Tools 1-4
- Immutable ephemeral overlays over base property or existing scenario state
- TruthLayer-derived delta calculation
- Assumptions disclosure and feature-change summaries
- Fresh Comparable and Fairness Tool evaluation
- Tenant Isolation
- Durable `what_if` audit events
- Backend and PostgreSQL Restart Recovery
- Live PostGIS Integration (`5 passed` with adjacent coverage)
- Docker Validation (PASS)

## Phase 5.5B.5: Negotiation Tool

Completed:

- Tool 6: Negotiation Tool
- Deterministic orchestration over Tools 1-5
- No Tool Layer pricing formulas, direct Router calls, direct ML calls, or direct CMT calls
- Five traceable positions: Strong Buy Opportunity, Negotiation Recommended, Fair Market Position, Premium Justified, and Overpriced
- Offer-band endpoints limited to TruthLayer `fair_price` and returned comparable prices
- Evidence-backed broker talking points and risk notes
- Optional What-if sensitivity analysis
- Scenario negotiation
- Tenant Isolation
- Durable `negotiation` audit events
- Backend and PostgreSQL Restart Recovery
- Live PostGIS Integration (`7 passed` with adjacent coverage)
- Docker Validation (PASS)

## Phase 5.5B.6: Investment Tool

Completed:

- Tool 7: Investment Tool
- Deterministic orchestration over Tool 6 and its Tools 1-5 evidence chain
- No Tool Layer pricing formulas, direct Router calls, direct ML calls, or direct CMT calls
- No ROI, IRR, CAGR, appreciation forecast, future-price prediction, rental-yield estimate, or investment-return generation
- Five traceable positions: Strong Opportunity, Moderate Opportunity, Fairly Priced, Caution, and High Risk
- Evidence-backed strengths, visible risks, comparable summary, negotiation summary, and optional What-if sensitivity summary
- Explicit `Insufficient Evidence` response when optional What-if evidence is unavailable
- Scenario investment evaluation
- Tenant Isolation
- Durable `investment` audit events
- Backend and PostgreSQL Restart Recovery
- Live PostGIS Integration (`9 passed` with adjacent coverage)
- Docker Validation (PASS)

## Phase 5.5B.7: Market Insight Tool

Completed:

- Tool 8: Market Insight Tool
- Descriptive analytics over persisted TruthLayer snapshots, prediction logs, shadow logs, comparable evidence, workspace history, and tool events
- Compound, H3 area, property-type, historical-window, confidence-distribution, fair-value-distribution, and comparable-density insights
- No forecasting, future-price generation, predicted appreciation, predicted returns, or synthetic trends
- Traceable evidence references for every generated statement
- Tenant Isolation
- Durable `market_insight` audit events
- Backend and PostgreSQL Restart Recovery
- Live PostGIS Integration (`10 passed` with adjacent coverage)
- Docker Validation (PASS)

---

# Current Priorities

Ordered by impact:

1. Frontend JWT/workspace/scenario integration and explicit RBAC policy.
2. LLM provider verification: mocked OpenAI/Gemini tests, staging smoke, token metrics validation.
3. Broker streaming UX refinement: mobile/browser QA, motion polish, accessibility, governance overlays.
4. CI/CD: automated backend/frontend checks.
5. Persistence: broker sessions, valuation history, audit trail.
6. Stream cancellation and operational hardening.
7. Production migrations: Alembic or migration runner.
8. Observability externalization: OpenTelemetry/metrics/log aggregation.
9. Data quality/admin tooling.
10. Cache/rate-limit externalization for scaling.

---

# Recommended Next Actions

## Stability

- Add CI running:
  - backend `pytest app/tests`
  - frontend `npm run lint`
  - frontend `npm test -- --run`
  - frontend `npm run build`
- Add a backend smoke job for Compose.
- Add a migration/schema verification job.

## Correctness

- Add broker provider tests with mocked OpenAI/Gemini HTTP responses.
- Add governance tests for fabricated comparable IDs, confidence drift, and unsupported percentages.
- Expand `/v1/broker/stream` contract tests to cover disconnect/error paths and event ordering under failure.

## Architecture

- Extract `rent_fair_price` orchestration into a valuation service class.
- Move broker sessions from in-memory store to persistent storage.
- Add cancellation-aware broker stage execution for streaming clients.
- Decide whether `frontend old` remains archived or is removed.

## Observability

- Add OpenTelemetry spans around valuation stages, DB queries, and broker reasoning stages.
- Export metrics to a real backend.
- Add request/valuation audit IDs to responses.

## Scalability

- Add Redis or another shared infrastructure for rate limits, session/cache, and hot valuation caching.
- Profile tier retrieval with production-like data volume.
- Add query-plan regression thresholds.

## AI Quality

- Build a prompt and narration evaluation suite.
- Add red-team cases for hallucinated prices/comps/confidence.
- Validate provider-native token usage and streaming behavior before claiming production LLM streaming.
- Keep deterministic authority as a hard invariant.

## Production Readiness

- Add authentication and RBAC before public exposure.
- Add secrets management.
- Add backup/restore procedure.
- Add deployment runbook beyond local Compose.
- Add data privacy/compliance review for scraped listings and images.

---

# Update Protocol for Future Agents

When future work is completed:

1. Re-scan changed backend, frontend, infrastructure, docs, tests, and configs.
2. Update status tables in this document.
3. Add a changelog entry under Phase Completion History.
4. Update Production Readiness percentages only when verified by code/tests/configs.
5. Mark uncertain claims as `Needs Verification`.
6. Never mark a feature complete unless it is implemented and reachable through code or documented operational workflows.
7. Record verification commands and results in the Executive Summary.

This document is intended to be the single source of truth for current project state.

---

## PX-0 React Frontend Product Completion Planning Update - 2026-06-09

Scope: React frontend product completion planning only for `pf_scraper/fair-price-eg/frontend`. No frontend code, backend code, auth, security, deployment, infrastructure, or production-hardening work was performed.

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

## PX-1A React Property Context Bridge - 2026-06-09

Scope: React frontend bridge only. No What-if UI, Negotiation, Investment, Market Intelligence, Copilot, Dashboard, backend route, backend schema, migration, auth, deployment, or infrastructure work was performed.

Implemented:

- A silent valuation-success bridge from direct valuation results to backend Copilot property context persistence.
- `pf_scraper/fair-price-eg/frontend/src/types/propertyContext.ts` for backend workspace, property context, and tool-event contracts.
- `pf_scraper/fair-price-eg/frontend/src/services/propertyContextService.ts` to reuse an active workspace, reuse the first backend workspace when available, create `ValorAI Active Valuations` when needed, bind to a matching property profile, create a property context when no match exists, and persist a scoped `direct_valuation` tool event.
- `pf_scraper/fair-price-eg/frontend/src/store/propertyContextStore.ts` to expose and persist `activeWorkspaceId`, `activePropertyId`, and nullable `activeScenarioId` for future intelligence tools.
- Silent integration in `pf_scraper/fair-price-eg/frontend/src/features/valuation/ValuationScreen.tsx` after successful `POST /v1/valuation/fair-price`.
- Documentation in `pf_scraper/fair-price-eg/property_context_bridge.md`.

Validation:

- Added service tests for workspace creation, property binding, abort-signal propagation, and malformed backend payload rejection.
- Added store tests for active ID persistence and bridge error handling.

Known limitations:

- The bridge depends on authenticated Copilot persistence endpoints and does not implement React JWT acquisition.
- `activeScenarioId` remains `null`; scenario creation is explicitly out of scope for PX-1A.
- No visible UI was added by design.

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

## Sprint 1 React Authentication Integration - 2026-06-10

Status: SPRINT 1 COMPLETE. P0-1 CLOSED.

React now authenticates through Firebase web auth, exchanges Firebase ID tokens
at `POST /v1/auth/token-exchange`, stores the returned ValorAI JWT for
browser-session restore, injects `Authorization: Bearer <jwt>` into protected
Axios calls, injects the same bearer token into broker SSE `fetch`, renews once
after a 401 response, cleans up logout state, and guards protected app routes.

Sprint 2 closed the Broker request contract mismatch. Sprint 3 closed the
remaining backend pytest collection and execution blocker.

## Sprint 2 Broker Contract Alignment - 2026-06-11

Status: SPRINT 2 COMPLETE. P0-2 CLOSED.

React Broker reason, chat, and stream payloads now include validated
`workspace_id` and `scenario_id`, bind to active workspace/property/scenario
context, and preserve authenticated protected-API execution.

Verification:

- `npm run lint` passed.
- `npm test` passed: 35 files, 144 tests.
- `npm run build` passed.

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
