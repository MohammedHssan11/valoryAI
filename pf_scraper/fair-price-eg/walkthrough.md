# ValorAI Phase 3B Walkthrough

## Purpose

Phase 3B upgrades ValorAI from a valuation-output screen into an institutional visual evidence system. The deterministic valuation engine remains authoritative; the new layer makes comparable evidence, spatial grounding, confidence dimensions, and retrieval governance visible to the user.

## Evidence Flow

1. Client submits an explicit governed valuation request.
2. Backend resolves the subject location through the Phase 3A.1b geospatial authority layer.
3. Comparable retrieval runs through deterministic tier/radius expansion.
4. Each retrieval attempt is recorded in top-level `retrieval_trace` with attempt order, radius, threshold, shortfall, status, and selected stage.
5. Hard guardrails and MAD filtering run before valuation weighting.
6. Weighted comparables are ranked with deterministic tie breakers.
7. Response returns enriched `top_comps`, `spatial_diagnostics`, `evidence_summary`, confidence dimensions, and explanation trace.
8. Frontend renders cards, map, confidence stack, filtering stages, and retrieval timeline from returned evidence only.

## Frontend Evidence UX

- Comparable evidence cards show listing id, price, sqm, bedrooms, bathrooms, distance, recency, similarity, confidence contribution, area, property type, weighted contribution, and retrieval tier.
- The evidence map plots subject and comparable coordinates from governed payloads, retrieval radius, distance lines, distance bands, zoom, pan, and comparable selection.
- Exploration filters support radius tightening, stricter similarity, newer comps, premium comps, and same-type comps.
- Filters only change the visual/analytical scenario. They do not mutate the frozen authoritative valuation result.
- Confidence is shown as valuation confidence, evidence confidence, and location confidence with weak/sparse/high-quality cluster signals.
- Explainability now includes rationale, filtering stages, retrieval timeline, and raw trace event inspection.

## Governance Guarantees

- AI does not alter valuation outputs.
- No fake or generated comparables are introduced.
- Visual order is deterministic.
- Comparable evidence comes from backend retrieval and weighting only.
- Authoritative valuation state is frozen with the submitted request.
- Exploration filters are local UI state and never rerun or silently change valuation authority.

## Verification

- Backend: `python -m pytest backend/app/tests`
- Frontend typecheck: `npm run lint`
- Frontend tests: `npm test`
- Frontend build: `npm run build`
- Browser smoke: `/valuation` loads locally with no console errors.
