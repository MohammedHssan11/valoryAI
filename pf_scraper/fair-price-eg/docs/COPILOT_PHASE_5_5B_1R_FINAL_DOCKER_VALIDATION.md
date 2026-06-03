# ValorAI Phase 5.5B.1R Final Docker Validation

## Executive Result

**FINAL STATUS: FAIL**

**Production Promotion: NO-GO**

**Phase 5.5B.1R may not be closed.**

Real Docker and PostgreSQL validation was executed on May 31, 2026. The clean
installation path can apply migration `005` and the persistence runtime survives
backend restart, backend destruction/recreation, and PostgreSQL restart.

The canonical migration fails against the existing historical PostgreSQL
volume. This is a release blocker because an in-place production upgrade cannot
apply migration `005`.

No application code, architecture, or feature behavior was modified during this
validation phase.

## Validation Environment

- Docker Engine: `28.5.1`
- Database image: `postgis/postgis:16-3.4`
- Canonical Compose project: `fair-price-eg`
- Isolated clean validation project: `fair-price-eg-clean-validation`
- Clean backend port: `58000`
- Clean PostgreSQL port: `55432`

## 1. Migration Validation

### Historical-volume upgrade: FAIL

Command:

```powershell
.\scripts\validate_copilot_recovery.ps1
```

Canonical Compose result:

```text
fair-price-eg-db-bootstrap-1    Exited (1)
fair-price-eg-backend-1         Created
service "db-bootstrap" didn't complete successfully: exit 1
```

Migration runner error:

```text
migration_start
migration_lock_acquired
migration_applying
migration_failure
(psycopg.errors.UndefinedColumn) column "created_at" does not exist
migration_lock_released
```

Root cause evidence from the historical database:

```text
prediction_logs columns:
id, request_id, timestamp, price, engine, routing_decision, lat, lng,
property_type, size_sqm, compound, h3_res9

shadow_logs columns:
id, request_id, timestamp, actual_response, router_prediction, ml_prediction,
cmt_prediction, engine_used, routing_reason, comparable_count,
confidence_score, compound_name, h3_res9
```

Migration `005` uses `CREATE TABLE IF NOT EXISTS` for these existing tables and
then attempts to create indexes using `created_at`. The historical tables use
`timestamp`, so the atomic migration transaction fails and rolls back.

Rollback evidence:

```text
schema_migrations: 000, 001, 002, 003, 004 only
users:              absent
assumptions:        absent
decision_history:   absent
tool_events:        absent
scenario_lineage:   absent
broker_sessions:    absent
```

### Historical migration integrity: PASS

The normalized SHA-256 checksums stored in the historical database match the
local canonical files:

```text
000  75452a0cd308a861053298666623320db398cc302801e804e0f7c394968085a1
001  0b11d18c9733e2e54b1a84f39b7117d8a2dd1363e7e76be19bad35b4ce98780e
002  9994e895fbe2bb0c6adb2428cc02aea57fbd7c705e5eb82574d83fd75431c2b7
003  dba957655f1bf61c700820814d7a713717d60d25e394b1ce094f278773bc14d8
004  3c03333fdff48f44b009d8cadc148f6db313d52feaa06dd4ad3fc58d6f74f417
```

### Clean-volume migration: PASS after retry

An isolated fresh Docker volume applied all six migrations:

```text
000_baseline.sql
001_database_stabilization.sql
002_address_resolution_cache.sql
003_geospatial_governance.sql
004_property_matrix_amenity_governance.sql
005_copilot_persistence_hardening.sql
```

Verification command:

```powershell
docker compose -p fair-price-eg-clean-validation run --rm db-bootstrap `
  python -m app.scripts.run_migrations --verify
```

Result:

```text
migration_verify_success
```

### Clean first-boot reliability: FAIL

The first isolated clean bootstrap attempt failed with:

```text
psycopg.OperationalError: connection refused
```

The PostGIS image briefly passed health checks during initialization, shut down
its temporary server, then started the final PostgreSQL process. A retry after
PostgreSQL settled succeeded. The one-shot bootstrap remains unreliable on a
fresh volume.

## 2. Schema, Constraints, and Indexes

### Clean schema structure: PASS

The clean PostgreSQL schema contains:

```text
users
workspaces
chats
messages
property_states
scenario_states
assumptions
scenario_lineage
tool_events
decision_history
broker_sessions
prediction_logs
shadow_logs
```

### Required constraints: PASS

Verified constraints:

```text
ck_messages_role
ck_property_states_area_positive
ck_property_states_bathrooms_non_negative
ck_property_states_bedrooms_non_negative
ck_scenario_states_delta_non_negative
fk_chats_workspace_user
fk_messages_chat_workspace_user
fk_property_states_workspace_user
fk_scenario_states_property_workspace_user
fk_assumptions_property_workspace_user
```

### Required indexes: PASS

Verified persistence indexes:

```text
ix_workspaces_user_active
ix_chats_user_workspace_active
ix_messages_chat_created_active
ix_property_states_user_workspace_active
ix_scenario_states_user_property_active
ix_scenario_states_parent
ix_assumptions_user_property_active
ix_assumptions_scenario_active
ix_scenario_lineage_user_property
ix_scenario_lineage_child
ix_tool_events_user_workspace_created
ix_decision_history_user_workspace_created
ix_broker_sessions_workspace_updated
ix_prediction_logs_request_created
ix_shadow_logs_request_created
```

## 3. Container Recovery Validation

### Backend restart: PASS on clean PostgreSQL

Created and persisted:

```text
workspace_id:  1
chat_id:       1
message_id:    1
property_id:   1
scenario_a:    1
scenario_b:    2
assumption_id: 1
tool_event_id: 1
broker_session: docker-broker-348943cac4
```

After `docker compose -p fair-price-eg-clean-validation restart backend`:

```text
workspace:    1
chat:         1
messages:     1
property:     1
scenario:     2
assumptions:  1
decisions:    present
tool_events:  1
broker_turns: 1
```

## 4. Container Recreation Validation

### Backend destruction and recreation: PASS on clean PostgreSQL

Commands:

```powershell
docker compose -p fair-price-eg-clean-validation rm -sf backend
docker compose -p fair-price-eg-clean-validation up -d backend
```

Retrieved after recreation:

```text
workspace:    1
chat:         1
messages:     1
property:     1
scenario:     2
assumptions:  1
decisions:    present
tool_events:  1
broker_turns: 1
```

## 5. PostgreSQL Persistence Validation

### PostgreSQL container restart: PASS on clean PostgreSQL

After restarting both `db` and `backend`, the API returned:

```json
{
  "workspace": 1,
  "chat": 1,
  "property": 1,
  "scenario": 2,
  "broker_turns": 1
}
```

Persisted row counts:

```text
decision_history: 19
tool_events:       1
scenario_lineage:  2
assumptions:       1
broker_sessions:   1
```

Workspace, chat, message, property, scenario, assumption, audit, lineage,
tool-event, and broker-session rows all remain in PostgreSQL.

## 6. Broker Memory Validation

### Broker turn recovery: PASS

Persisted broker row:

```text
session_id:         docker-broker-348943cac4
previous_requests:  1
last_intent:        general_guidance
grounding_status:   passed
governance_status:  passed
```

The broker session restored after backend restart, backend
destruction/recreation, and PostgreSQL restart.

### Workspace and scenario context binding: FAIL

The current broker compatibility route does not bind Copilot workspace or
scenario context into the broker session:

```text
broker_sessions.user_id:      NULL
broker_sessions.workspace_id: NULL
analytical_context: no workspace_id or scenario_id
```

Workspace and scenario records independently restore through the Copilot API,
but broker-session workspace/scenario context restoration cannot be claimed.

## 7. Tenant Isolation Validation

### API isolation: PASS

User B attempted to retrieve User A's workspace:

```text
USER_B_GET_USER_A_WORKSPACE_STATUS=404
```

### Database isolation: PASS

Direct cross-tenant SQL insertion was rejected:

```text
ERROR: insert or update on table "chats" violates foreign key constraint
"fk_chats_workspace_user"
DETAIL: Key (workspace_id, user_id)=(1, 3) is not present in table "workspaces".
```

Production still needs a trusted authentication boundary because `X-User-ID`
is currently supplied directly by the caller.

## 8. Soft Delete Validation

### Individual entity soft delete and restore: PASS

For workspace, chat, property, and scenario:

- Delete returned success.
- Normal retrieval returned `404`.
- PostgreSQL retained the row with `is_deleted = TRUE`.
- Restore returned the entity.

Audit evidence:

```text
workspace.deleted / workspace.restored
chat.deleted      / chat.restored
property.deleted  / property.restored
scenario.deleted  / scenario.restored
```

### Workspace cascade restoration: PARTIAL

Deleting a workspace soft-deletes its child chats, messages, properties,
scenarios, and assumptions. Restoring the workspace restores the workspace row
only. Children remain deleted until restored individually; messages and
assumptions do not currently expose restore endpoints.

## 9. Audit Trail Validation

### Audit persistence: PASS

Persisted records:

```text
decision_history: 19
tool_events:       1
scenario_lineage:  2
```

Lineage evidence:

```text
Scenario A: parent NULL -> child 1
Scenario B: parent 1    -> child 2
```

Tool-event evidence:

```text
tool_name:  docker-validation
event_type: probe
payload:    {"phase": "5.5B.1R"}
```

## 10. Docker Evidence

Canonical project after failed historical upgrade:

```text
fair-price-eg-db-1             Up (healthy)
fair-price-eg-db-bootstrap-1   Exited (1)
fair-price-eg-backend-1        Created
```

Isolated clean validation project:

```text
fair-price-eg-clean-validation-db-1             Up (healthy)
fair-price-eg-clean-validation-db-bootstrap-1   Exited (0)
fair-price-eg-clean-validation-backend-1        Up (healthy)
```

## 11. Final Readiness Review

| Layer | Score | Result |
| --- | ---: | --- |
| Ownership Layer | 8 / 10 | Tenant ownership and composite FKs pass; trusted actor binding remains |
| Persistence Layer | 5 / 10 | Clean schema passes; historical-volume upgrade fails |
| Recovery Layer | 7 / 10 | Runtime recovery passes on clean DB; first-boot race remains |
| Audit Layer | 10 / 10 | Decision, tool-event, and lineage persistence pass |
| Scenario Layer | 10 / 10 | Scenario state and lineage recovery pass |
| Workspace Layer | 8 / 10 | Workspace recovery passes; cascade restoration is partial |
| Assumptions Layer | 8 / 10 | Durable row persists; cascade restore path is incomplete |
| Tenant Isolation | 8 / 10 | API and DB enforcement pass; trusted authentication remains |

**Updated Docker Validation Readiness: 64 / 80 = 80 / 100**

The previous code-foundation score of `92 / 100` remains useful as an
implementation score. It is not a production-promotion score.

## Remaining Blockers

1. Migration `005` must support historical `prediction_logs` and `shadow_logs`
   tables that use `timestamp` instead of `created_at`.
2. Fresh-volume Compose bootstrap must tolerate the PostGIS initialization
   readiness race.
3. Broker sessions must bind trusted user/workspace ownership and persist
   workspace/scenario context before that recovery claim can pass.
4. Production authentication must bind the actor identity rather than trusting
   a caller-supplied `X-User-ID`.
5. Workspace cascade restore semantics must be explicitly accepted or completed
   for child messages and assumptions.

## Final Decision

**NO-GO**

Phase 5.5B.1R is not officially closed. Phase 5.5B.2 Tool Layer Implementation
must not begin until the canonical historical-volume migration succeeds and the
remaining promotion blockers are resolved or explicitly accepted.
