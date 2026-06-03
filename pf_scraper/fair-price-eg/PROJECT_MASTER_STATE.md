# VALORAI: PROJECT MASTER STATE

*This document serves as the single source of authoritative engineering truth for the ValorAI project. It is strictly maintained to reflect implementation reality, not aspirational marketing.*

## 1. System Identity
ValorAI is a **governed deterministic intelligence platform prototype** built around explainable valuation intelligence. It is explicitly *not* a generic chatbot wrapper. It is an institutional-grade analytical system where the deterministic valuation engine acts as the absolute source of truth, and the LLM acts exclusively as a governed analytical explanation layer.

## 2. Final Stabilized System State
The core architecture has reached presentation-ready maturity with a stable, governed implementation layer. Phase 3A.1b added deterministic geospatial governance hardening for institutional address resolution. Phase 3B adds the visual evidence layer that makes comparable intelligence, spatial reasoning, confidence dimensions, and retrieval governance visible without changing valuation authority.

*   **Deterministic Valuation Engine:** Fully implemented and authoritative.
*   **Migration Governance Layer:** Hardened. Replaced legacy volume-initialization mechanics with a Custom Deterministic Migration Runner featuring advisory locking, checksum immutability, atomic transactions, and safe upgrade mechanics for existing environments.
*   **Geospatial Governance Layer:** Hardened. Address normalization, canonical entities, governed aliases, versioned cache keys, explicit location modes, polygon-first area resolution, and spatial confidence caps are implemented.
*   **Comparable Evidence Layer:** Implemented. Backend responses expose enriched weighted comparable metadata, top-level retrieval traces, spatial diagnostics, evidence summaries, and deterministic contribution fields.
*   **Property Matrix + Amenity Intelligence Layer:** Implemented as an additive governed extension. Category-aware contracts now cover residential rent, residential sale, villa sale, office rent, retail rent, commercial rent, and land sale. Canonical amenity symbols remain preserved while governed metadata, aliases, Arabic names, category weights, similarity scoring, confidence contribution, retrieval refinement, comparable weighting, and explainability traces are exposed without allowing amenities or LLM narration to override deterministic pricing.
*   **Visual Evidence UX:** Implemented. The valuation screen now includes institutional comparable cards, exploration-only filters, spatial evidence map, confidence stack, filtering stages, and retrieval timeline.
*   **Governed Orchestration Runtime:** Fully integrated. The orchestration enforces strict boundaries on provider generation.
*   **Live SSE Streaming:** Stabilized. Stream lifecycle, stale event suppression, and graceful interruptions are safely handled.
*   **Broker Intelligence Terminal (UX):** Highly polished, cinematic, and institutional. Features presentation-safe scenario seeds and clear explainability visualizations.
*   **Provider Runtime Hardening:** Completed. Strict markdown stripping and schema overwrites guarantee the LLM cannot invent prices, comparables, or override deterministic outputs.
*   **Session Continuity:** Lightweight continuity achieved via Zustand state management without distributed database overhead.
*   **Edge-Case QA:** Hardened. The UI gracefully and explicitly handles low-confidence scores, empty comparable data, orchestration timeouts, and user-initiated pipeline aborts.

## 3. Final Verified Status
*   **Frontend Stability:** Verified. Vitest, TypeScript typecheck, and Vite production build complete successfully.
*   **Backend Stability:** Verified. 98 backend tests pass with 1 PostGIS integration test skipped unless a seeded PostGIS stack is explicitly enabled.
*   **Spatial Determinism:** Verified through regression coverage for Arabic normalization, Franco/English aliases, cache replay, canonical entity matching, explicit location modes, ambiguity rejection, and confidence capping.
*   **Evidence Determinism:** Verified through coverage for comparable sorting, filtering behavior, retrieval trace status, map selection synchronization, confidence visualization, and enriched evidence payloads.
*   **Category/Amenity Determinism:** Verified. Backend tests cover category contracts, category retrieval parameters, amenity normalization, amenity weighting, amenity similarity, category-aware confidence contribution, and deterministic explanation traces. Frontend typecheck, tests, and production build pass with category selection and amenity governance rendering.

## 4. Technical Debt & Current Limitations
*   No distributed session persistence (relies on frontend local state/lightweight store).
*   No production authentication or RBAC (Role-Based Access Control).
*   Single-node streaming (not yet tested under high-concurrency horizontal scaling).
*   Provider fallback paths are currently synchronous and block until completion if the primary SSE stream fails entirely.
*   The Phase 3A.1b canonical gazetteer is a deterministic seed layer, not yet a licensed national polygon dataset.
*   Polygon-aware area resolution is implemented, but full production border accuracy depends on authoritative polygons being loaded into `areas.geom`.
*   Evidence-map visual regression is verified by component tests and browser smoke, not pixel-diff screenshot automation.

## 5. Remaining Production Gaps (Future Work)
*   **Security:** Implementation of enterprise-grade AuthN/AuthZ.
*   **Infrastructure:** Kubernetes/Docker Swarm deployment hardening, distributed caching (Redis) for session state.
*   **Provider Ops:** Multi-region LLM provider failovers, token usage tracking, and latency optimization.
*   **Data Persistence:** Migration from lightweight state to a persistent PostgreSQL/NoSQL data layer for historical valuation tracking.
*   **Geospatial Data Governance:** Replace seeded centroids with a curated, versioned Egypt gazetteer and authoritative polygons.
*   **Spatial Operations:** Add restricted admin workflows for alias approval, cache invalidation, and resolver-version rollouts.
*   **Evidence Audit Artifacts:** Add exportable valuation evidence packets for investment committee or underwriting review.

## 6. Current Operational Priorities
*Major implementation expansion should remain governance-led and additive.*
1. Demo preparation around the Phase 3B visual evidence flow.
2. Walkthrough quality and advisor presentation readiness.
3. Final documentation polish (README, architecture diagrams).
4. Capturing screenshots and video recordings of the stabilized evidence views.
