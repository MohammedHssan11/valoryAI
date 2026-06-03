# ValorAI Master State Rebuild Audit

Audit date: 2026-05-31  
Scope: repository root and `pf_scraper/fair-price-eg` implementation  
Governance rule: **CODE > REPORTS > OLD MASTER STATE**

## Audit Result

The existing `PROJECT_MASTER_STATE.md` is not safe to use as an authoritative
state document. It contains recent Phase 5.5 additions alongside older claims
that remain materially false. The nested application documentation also
predates the Copilot persistence and JWT work.

The live repository supports a rebuilt master state. The authoritative
implemented baseline is **through Phase 5.5B.2 Tools 1 + 2**, with one newly
confirmed broker-runtime integration defect that must remain visible as an open
risk.

## Current Architecture

The implemented institutional architecture is:

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

This architecture exists through three runtime surfaces:

| Surface | Implemented path | Audit status |
| --- | --- | --- |
| Direct valuation API | `/v1/valuation/fair-price` and `/v1/rent/fair-price` -> Router -> CMT or ML -> explainability -> monitoring | Operational; currently unauthenticated |
| Copilot Tool API | JWT -> `/v1/copilot/tools/valuation` or `/explainability` -> workspace-scoped adapter -> Router/Truth Layer -> snapshots and tool events | Operational and Docker-validated |
| Broker reasoning API | JWT -> `/v1/broker/*` -> Broker Orchestrator -> broker evidence registry -> governed narration -> durable broker session | Partially operational; valuation-backed runs are degraded by an adapter signature drift |

The Broker Copilot and Phase 5.5B.2 Copilot Tool Layer are related but not the
same module. The broker runtime still uses the older
`backend/app/broker/tools/` registry. The Phase 5.5B.2 adapters live in
`backend/app/services/copilot_tools_service.py`.

## Current Active Phase

The latest implemented and validated named phase is **Phase 5.5B.2: Tool Layer,
Tools 1 + 2**.

No later named phase is implemented in the repository. Current work should be
treated as post-5.5B.2 stabilization and expansion:

1. Repair the broker valuation adapter call boundary.
2. Integrate web clients with JWT plus workspace/scenario context.
3. Implement Copilot Tool 3: Comparable Tool.

## Completed Phases

| Phase | Status | Repository evidence |
| --- | --- | --- |
| Data phases 1, 2, 2.5, 3, 3.5, 3.6 | Complete historical foundation | Scraper/data tooling, `dataset_v3` artifacts, CatBoost models, schemas |
| Phase 3A.1b and 3B | Complete historical foundation | Geospatial governance, property matrix, amenity intelligence, visual evidence UI |
| Phase 5.1 | Implemented | Optimized Router rules in `router_service.py` |
| Phase 5.2 | Implemented | Conditional orchestration Router in `router_service.py` |
| Phase 5.3A | Implemented | Shadow pipeline in `monitoring_service.py` |
| Phase 5.3B | Implemented | Prediction logging in `monitoring_service.py` |
| Phase 5.4 | Implemented | Router explainability model and ML SHAP feature drivers |
| Phase 5.5A | Complete | Copilot memory, assumptions, audit, and tool architecture discovery |
| Phase 5.5B.1 | Complete | Workspace, chat, message, property, and scenario persistence |
| Phase 5.5B.1R | Complete | Ownership, soft delete, scenario lineage, durable broker memory |
| Phase 5.5B.1R.1 | Complete | JWT, tenant constraints, broker ownership, restore semantics, bootstrap fix |
| Phase 5.5B.2 | Complete | Valuation and explainability Copilot adapters, valuation snapshots, tool events |

Formal standalone reports for Phases 5.1 through 5.4 were not found in the
repository. Their implemented status is derived from code, not inferred from
missing documentation.

## Deprecated Phases And Claims

| Deprecated claim | Replacement |
| --- | --- |
| Phase 4 Hybrid AVM is the active architecture | Historical roadmap only. The implemented architecture is Router + CMT/ML + Copilot adapters. |
| Explainability is planned | Explainability is implemented in the truth layer, ML SHAP path, frontend evidence UI, and Tool 2 adapter. |
| Authentication is missing | JWT bearer authentication is implemented for Copilot and Broker routes. |
| Broker sessions are in-memory only | Broker sessions persist in PostgreSQL with user/workspace/scenario ownership. |
| There is no migration framework | The canonical path is the checksum-enforced forward-only SQL runner for migrations `000` through `007`. |
| Alembic is the deployment migration authority | Alembic is a historical scaffold only. |
| Phase 5.5B.2 remains merely active | Tools 1 + 2 have a GO report and fresh Docker validation. Expansion work remains, but the named slice is delivered. |

## Contradictions Found

| Existing location | Contradiction | Reality |
| --- | --- | --- |
| Root `PROJECT_MASTER_STATE.md` | Declares JWT production-ready, then later lists API keys/OAuth/JWT as missing | JWT is implemented for Copilot/Broker APIs; web client attachment and organization RBAC remain |
| Root `PROJECT_MASTER_STATE.md` | Declares Copilot persistence production-ready, then later calls broker sessions in-memory | `broker_sessions` is PostgreSQL-backed and restart-validated |
| Root `PROJECT_MASTER_STATE.md` | Lists Phase 4 Hybrid AVM active while also describing Router + Copilot architecture | Router + Copilot architecture is current; Hybrid AVM is historical |
| Root `PROJECT_MASTER_STATE.md` | Lists Phase 5 explainability planned while later documenting implemented explainability | Explainability is implemented |
| Nested `pf_scraper/fair-price-eg/README.md` | Says JWT AuthN/AuthZ is future work | JWT bearer identity exists in `backend/app/core/auth.py` |
| Nested `pf_scraper/fair-price-eg/README.md` | Says no distributed session persistence and relies on local state | Backend broker sessions are durable in PostgreSQL; frontend continuity remains local |
| Nested `pf_scraper/fair-price-eg/PROJECT_MASTER_STATE.md` | Predates migrations `005` through `007` and Copilot Tool adapters | Historical snapshot only |

## Architecture Drift Findings

1. The root master state was incrementally synchronized instead of rebuilt.
   New Phase 5.5 text was inserted without removing obsolete roadmap and risk
   sections.
2. The nested application master state and README represent an earlier
   frontend-centric snapshot.
3. Broker orchestration and Copilot Tool APIs evolved as separate layers. Old
   documentation sometimes merges them into one tool registry.
4. The frontend remains behind the backend authentication contract. Axios and
   streaming fetch calls do not add bearer JWTs, and `BrokerScreen` does not
   send required workspace/scenario context.
5. The legacy broker valuation adapter calls `rent_fair_price` with the old
   positional signature. A live 2026-05-31 control audit confirmed that
   valuation-backed broker chat returns degraded mode while the same property
   succeeds through direct valuation.

## Obsolete Sections

The following sections of the old root master state should not be carried
forward as current claims:

- Hybrid AVM marked as the current active phase.
- Explainability marked as planned.
- Authentication marked as missing.
- Broker sessions marked as in-memory.
- Valuation history and audit persistence marked as missing.
- Alembic or empty migrations described as the migration state.
- Readiness percentages copied from earlier snapshots without a reproducible
  denominator.

## Missing Sections

The old documents omit or understate:

- JWT ownership and trusted-subject provisioning.
- Composite tenant foreign keys.
- Workspace cascade restore provenance.
- Broker session user/workspace/scenario ownership.
- Valuation snapshots.
- Copilot Tool API contracts.
- Tool event persistence.
- Migration `007`.
- Fresh Docker validation evidence.
- The broker valuation adapter defect.
- A reproducible progress calculation.

## Recommended Structure

The rebuilt authoritative document should:

1. Separate current implemented state from historical evolution.
2. Keep direct valuation, Copilot Tool, and Broker runtime surfaces distinct.
3. List phase completion only when code or executed reports support it.
4. Treat Docker Compose as staging-grade, not as a complete production
   deployment.
5. Keep frontend JWT integration, organization RBAC, external monitoring,
   Tool 3-5 delivery, and broker adapter repair visible as remaining work.
6. Use a counted system ledger for progress instead of estimated percentages.

## Validation Snapshot

Fresh checks executed during this rebuild on 2026-05-31:

| Check | Result |
| --- | --- |
| `python -m compileall -q app` | PASS |
| Focused Copilot tests | `13 passed` |
| Broad backend tests excluding stale collector | `103 passed, 1 skipped, 14 failed` |
| Full backend collection | BLOCKED by stale `test_spatial_confidence.py` import |
| Frontend tests | `25 passed` |
| Frontend TypeScript lint | PASS |
| Frontend production build | PASS |
| `docker compose config --quiet` | PASS |
| Migration verification | PASS, migrations `000` through `007` |
| Health/readiness/metrics/operational endpoints | PASS |
| Staging smoke | PASS |
| `validate_copilot_recovery.ps1` | PASS |
| `validate_copilot_tools.ps1` | PASS |
| Broker valuation-backed control audit | DEGRADED: legacy broker adapter defect confirmed |

