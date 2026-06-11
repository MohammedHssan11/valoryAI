# ValorAI Phase 5.5B.1R Persistence Recovery Report

## Scope

This release hardens persistence foundations only. It does not add Copilot
reasoning, LLM integration, frontend changes, or valuation behavior changes.

## Migration Review

The checksum-enforced SQL runner in `app.scripts.run_migrations` is the canonical
deployment migration mechanism. Docker `db-bootstrap` already executes it before
backend startup. Historical migrations `000` through `004` remain immutable.

Migration `005_copilot_persistence_hardening.sql` is forward-only. It creates or
backfills the tenant-scoped Copilot tables, audit foundation, durable broker
session storage, supporting indexes and constraints, and the previously missing
prediction and shadow log tables expected by existing monitoring writers.

The legacy Alembic scaffold remains for historical inspection and is not the
deployment authority.

## Ownership Design

`User -> Workspace -> Chat -> Message`

`User -> Workspace -> PropertyState -> ScenarioState`

Every Copilot entity stores `user_id`. All Copilot API operations require the
`X-User-ID` actor header and scope repository queries by actor. Cross-user reads
return no entity and cross-user writes are rejected. Composite database foreign
keys also reject direct-SQL tenant mismatches between workspaces, chats,
messages, properties, scenarios, and assumptions.

## Soft Delete Design

Workspace, chat, message, property, scenario, and assumption records use
`is_deleted`, `deleted_at`, `updated_at`, and `version`. Delete endpoints mark
records deleted. Restore endpoints are available for workspace, chat, property,
and scenario state. No default API path performs permanent deletion.

## Scenario Lineage Design

Each scenario stores `parent_scenario_id`. A durable `scenario_lineage` append
record is written when a scenario is forked. The API exposes lineage
reconstruction and scenario-tree retrieval.

## Assumptions Persistence

Assumptions store key, JSON value, status, source, confirmation timestamp,
override timestamp, override reason, tenant scope, property scope, optional
scenario scope, soft-delete state, and version metadata. Unknown assumptions are
stored explicitly and are never silently promoted to confirmed values.

## Audit Trail Design

`decision_history` records important Copilot state changes. `tool_events` is a
tenant-scoped durable reservation for future tool-layer execution logging.
`scenario_lineage` records scenario forks independently of mutable scenario
state.

## Broker Memory Recovery

The broker session dictionary has been removed. `BrokerSessionStore` now stores
JSON snapshots in `broker_sessions` through SQLAlchemy sessions. Existing broker
reasoning behavior is unchanged.

The broker compatibility route does not yet require actor headers, so persisted
broker rows allow nullable user/workspace scope for legacy clients. Before
production promotion, authenticated broker requests should bind every session
to a trusted user and workspace.

## Validation

Automated persistence tests verify:

- user and workspace isolation
- multiple properties in one workspace
- scenario lineage and tree reconstruction
- assumptions confirmation and override history
- audit records and tenant-scoped tool events
- soft delete and restore
- database constraint enforcement
- workspace, chat, property, scenario, and broker-memory recovery after reopening
  a disk-backed database
- broker route continuity through `/v1/broker/chat` and `/v1/broker/session`
- direct-database tenant mismatch rejection
- immutability of historical migrations
- canonical Docker migration runner selection

Docker restart validation is reproducible with:

```powershell
.\scripts\validate_copilot_recovery.ps1
```

## Environment Blocker

Docker Desktop was unavailable during implementation, so live Postgres
migration application and container restart evidence could not be collected on
this machine. Run the recovery script with Docker Desktop active before
production promotion.

## Test Results

Focused persistence foundation:

```text
python -m pytest -p no:cacheprovider app/tests/test_copilot.py app/tests/test_copilot_persistence_hardening.py -q
9 passed
```

Selected integration subset:

```text
python -m pytest -p no:cacheprovider app/tests/test_routes_and_health.py app/tests/test_config.py app/tests/test_sql_compilation.py app/tests/test_copilot.py app/tests/test_copilot_persistence_hardening.py -q
15 passed
```

Broad backend suite with the known collection-broken spatial test excluded:

```text
python -m pytest -p no:cacheprovider app/tests --ignore=app/tests/test_spatial_confidence.py -q
98 passed, 14 failed, 1 skipped
```

The 14 failures are existing valuation test drift: those tests monkeypatch
`pricing_routes.nearest_area`, which moved out of the route module. Running the
full suite without the ignore still stops during collection because
`app/tests/test_spatial_confidence.py` imports `_combine_confidence` from the old
route module. These failures are outside the persistence-only scope.

Static validation:

```text
docker compose config --quiet
PASS

PowerShell parser check for scripts/validate_copilot_recovery.ps1
PASS
```

## Readiness

Foundation code readiness: **92 / 100**

Production promotion readiness: **NO-GO** until live Docker/Postgres migration,
restart, and container recreation validation pass; the pre-existing valuation
test drift is repaired; and a trusted authentication boundary binds actor
identity and broker session ownership to request context.
