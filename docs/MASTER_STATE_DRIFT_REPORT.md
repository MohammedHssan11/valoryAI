# ValorAI Master State Drift Report

Report date: 2026-05-31  
Compared documents:

- Root `PROJECT_MASTER_STATE.md`
- Root `PROJECT_MASTER_STATE_BACKUP.md`
- `pf_scraper/fair-price-eg/PROJECT_MASTER_STATE.md`
- `pf_scraper/fair-price-eg/README.md`
- Current code, migrations, reports, and executed validation

## Executive Finding

Documentation drift is severe enough that patching the old master state would
preserve false claims. The authoritative replacement is
`PROJECT_MASTER_STATE_V2.md`.

The dominant drift pattern is additive editing: later Phase 5.5 truths were
inserted while older roadmap, security, persistence, and readiness sections
remained unchanged.

## Contradictions Found

| Topic | Outdated claim | Authoritative replacement |
| --- | --- | --- |
| Current architecture | Hybrid AVM is active | Router + CMT/ML + Copilot Tool architecture is current |
| Explainability | Planned | Implemented across truth layer, ML SHAP, frontend, and Tool 2 |
| Authentication | Missing | JWT bearer identity implemented for Copilot and Broker APIs |
| Copilot persistence | Missing or partial | Workspace/chat/property/scenario/assumption memory implemented |
| Broker sessions | In-memory only | PostgreSQL-backed with user/workspace/scenario ownership |
| Valuation history | Missing | `valuation_snapshots` implemented |
| Audit trail | Planned | `decision_history`, `tool_events`, and lineage implemented |
| Migration framework | Empty or absent | Deterministic runner plus SQL migrations `000`-`007` |
| Phase 5.5B.2 | Active only | Tools 1 + 2 delivered and Docker-validated |
| Broker readiness | Fully implemented implication | Valuation-backed broker execution currently degrades |

## Outdated Sections

The old root master state contains obsolete current-state sections for:

- Phase 4 Hybrid AVM activation.
- Phase 5 explainability planning.
- Missing JWT/API authentication.
- In-memory broker sessions.
- Missing persistence and valuation history.
- Missing audit trail.
- Migration framework absence.
- Immediate next steps that were already completed by migrations `005`-`007`.
- Historical percentages that lack a reproducible system denominator.

The nested `pf_scraper/fair-price-eg/README.md` remains useful as a historical
frontend overview but is outdated for backend authentication and persistence.

## Incorrect Readiness Claims

| Claim type | Drift |
| --- | --- |
| Overstated | Any blanket production-ready claim is incorrect while the broker valuation adapter, frontend JWT integration, auth policy, secrets, RBAC, and test drift remain |
| Understated | Claims that Copilot persistence, JWT identity, tenant isolation, broker recovery, explainability, or Tools 1-2 are missing are incorrect |
| Ambiguous | Historical report readiness scores are scoped validation ratings, not total project completion |

Correct readiness classification:

```text
Staging-grade governed platform with unresolved production integration work.
Production promotion: NO-GO.
```

## Incorrect Architecture Claims

### Hybrid AVM As Current Architecture

The root document still marks Hybrid AVM active. Current code instead routes
between implemented CMT and ML engines using comparable density and exposure
rules.

### One Unified Tool Layer

The repository has two related tool concepts:

1. Broker evidence tools under `backend/app/broker/tools/`.
2. Phase 5.5B.2 authenticated Copilot Tool adapters in
   `backend/app/services/copilot_tools_service.py`.

They must not be conflated. Broker evidence tools do not mean Copilot Tools 3-5
are implemented.

### Fully Operational Broker Copilot

The broker orchestration structure exists, but its legacy valuation adapter
calls the pricing route through an obsolete positional boundary. On 2026-05-31:

```text
Direct Mivida valuation:
  HTTP 200
  engine_used: CMT
  routing_reason: GoldilocksZone
  comps_count: 49

Broker Mivida valuation-backed chat:
  HTTP 200
  degraded_mode: true
  valuation_analysis: failed
  downstream evidence tools: skipped
```

## Incorrect Phase Statuses

| Phase | Old status | Correct status |
| --- | --- | --- |
| Phase 4 Hybrid AVM | Active | Historical roadmap, not current active architecture |
| Phase 5 Explainability | Planned | Implemented |
| Phase 5.5B.1 | Sometimes omitted | Complete |
| Phase 5.5B.1R | Sometimes left blocked | Complete after 5.5B.1R.1 fixes |
| Phase 5.5B.1R.1 | Missing in older snapshots | Complete |
| Phase 5.5B.2 | Active | Delivered for Tools 1 + 2; expansion remains |

## Missing Implementations

Older documentation omits these implemented systems:

- JWT bearer decoding and user provisioning.
- Composite tenant-scoped foreign keys.
- Workspace cascade restore provenance.
- Durable broker sessions.
- Broker session user/workspace/scenario binding.
- Scenario lineage.
- Decision history.
- Tool events.
- Valuation snapshots.
- Copilot Valuation Tool.
- Copilot Explainability Tool.
- Migration compatibility preflight.
- Migration `006` production blockers resolution.
- Migration `007` Tool adapter schema.

## Historical Drift Sources

| Source | Drift contribution |
| --- | --- |
| Root `PROJECT_MASTER_STATE_BACKUP.md` | Pre-5.5 baseline retained as current language |
| Root `PROJECT_MASTER_STATE.md` | Incremental sync inserted new sections without removing contradictions |
| `MASTER_STATE_SYNC_REPORT.md` | Correctly identifies several drift areas but carried an estimated percentage |
| Nested app `PROJECT_MASTER_STATE.md` | Earlier Phase 3B presentation snapshot |
| Nested app `README.md` | Earlier local-state and future-JWT assumptions |
| Phase 5.5B.1R final Docker report | Historical FAIL report correctly superseded by 5.5B.1R.1 GO report |
| Phase 5.5B.2 report | Correct for Copilot Tools 1-2 but does not test the separate broker adapter path |

## Corrected Source Hierarchy

Use sources in this order:

1. Current code and migrations.
2. Fresh executed validation from 2026-05-31.
3. Phase reports, with later reports superseding earlier blockers.
4. Historical master states only for architecture evolution.

## Canonical Replacements

Use:

- `PROJECT_MASTER_STATE_V2.md` for authoritative current state.
- `MASTER_STATE_REBUILD_AUDIT.md` for audit rationale.
- `PROJECT_PROGRESS_ANALYSIS.md` for reproducible progress calculations.
- `MASTER_STATE_DRIFT_REPORT.md` for documentation governance.

Do not update historical master states in place. Preserve them as evidence of
architecture evolution.

