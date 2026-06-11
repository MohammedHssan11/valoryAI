# Sprint 6 Authorization Certification

Date: 2026-06-11

## Certification Target

Certify that authenticated users cannot access another user's workspace, scenario, broker session, valuation snapshot, Copilot memory, or protected tool evidence in current source.

## Boundary Rules

| Resource | Ownership Rule | Source Evidence |
| --- | --- | --- |
| User profile | `/users/me` from JWT subject; `/users/{id}` returns 404 unless actor owns id | `api/routes/copilot.py`, `core/auth.py` |
| Workspace | `Workspace.id` plus `Workspace.user_id == actor` | `CopilotService.get_workspace` |
| Property | `PropertyState.id` plus `PropertyState.user_id == actor`; workspace consistency checked | `CopilotService`, `CopilotToolsService._property` |
| Scenario | `ScenarioState.id` plus actor, workspace, and property binding | `CopilotService`, `CopilotToolsService._scenario` |
| Valuation snapshot | `valuation_id` plus actor and workspace | `CopilotToolsService._snapshot` |
| Broker session | `session_id` plus actor; creation also requires workspace and scenario match | `BrokerSessionStore.get_or_create`, `get` |
| Copilot memory | actor, workspace, scenario, broker session, and property scope | `DeterministicMemoryIntegration._scope` |
| Narration | scope and citation binding before provider egress | `NarrationAdmissionGate._scope_binding_error` |

## Access Attempts

The following cross-tenant attempt classes were verified by tests collected and executed in Sprint 6:

- User B reading User A workspace: denied by `user_id` filters.
- User B creating a property under User A workspace: rejected.
- User B reading User A property/scenario: not found.
- User B using User A property/scenario in protected tools: `ToolResourceNotFound`.
- User B using User A valuation id in Tool Layer: not found because valuation snapshots are scoped by actor and workspace.
- User B using User A broker session id: not found or ownership mismatch.
- User B building Copilot memory over User A workspace/session: `ACCESS_DENIED`.
- User B inducing provider narration from inaccessible scope: fail-closed access-denied delivery.

## Verification

Commands executed:

```powershell
pytest --collect-only -q
pytest -q
$env:RUN_POSTGIS_INTEGRATION='1'
$env:DATABASE_URL='postgresql+psycopg://fairprice:fairprice@localhost:15480/fairprice'
pytest -q -m integration
```

Results:

- Backend collection: 208 tests collected in 6.50s.
- Backend default suite: 206 passed, 11 skipped in 65.23s.
- PostGIS integration suite: 17 passed, 206 deselected in 19.41s.

## Certification Result

Authorization certification: PASS.

No current-source evidence supports cross-tenant read/write access through protected Copilot, Broker, Tool, Orchestrator, memory, or valuation snapshot paths.

## Conditions

- Pricing endpoints remain public and are not tenant data endpoints.
- Live Firebase production-login smoke depends on real environment credentials and was not performed in Sprint 6.

