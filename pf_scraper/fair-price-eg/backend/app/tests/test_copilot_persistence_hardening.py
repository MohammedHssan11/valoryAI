from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from app.api.schemas.copilot import (
    AssumptionCreate,
    AssumptionUpdate,
    ChatCreate,
    MessageCreate,
    PropertyStateCreate,
    ScenarioStateCreate,
    ToolEventCreate,
    UserCreate,
    WorkspaceCreate,
)
from app.broker.schemas.contracts import BrokerIntent
from app.broker.sessions.state import BrokerSessionStore
from app.core.auth import create_access_token
from app.db.base import Base
from app.main import app as fastapi_app
from app.models.copilot import PropertyState
from app.scripts.run_migrations import MIGRATIONS_DIR, compute_checksum
from app.services.copilot_service import CopilotService
import app.models.copilot  # noqa: F401


@pytest.fixture()
def session_factory(tmp_path: Path):
    db_path = tmp_path / "copilot-recovery.sqlite3"
    engine = create_engine(f"sqlite:///{db_path}")

    @event.listens_for(engine, "connect")
    def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
        dbapi_connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(bind=engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    yield factory, db_path
    engine.dispose()


def create_user(service: CopilotService, subject: str):
    return service.create_user(UserCreate(external_subject=subject, display_name=subject.title()))


def create_property(service: CopilotService, user_id: int, workspace_id: int, label: str):
    return service.create_property_state(
        user_id,
        PropertyStateCreate(
            workspace_id=workspace_id,
            label=label,
            location="New Cairo",
            area=150,
            bedrooms=3,
            bathrooms=2,
            amenities={},
        ),
    )


def test_user_and_workspace_isolation_with_multiple_properties(session_factory):
    factory, _ = session_factory
    with factory() as db:
        service = CopilotService(db)
        alice = create_user(service, "alice")
        bob = create_user(service, "bob")
        workspace = service.create_workspace(alice.id, WorkspaceCreate(name="Alice Portfolio"))
        props = [create_property(service, alice.id, workspace.id, f"Property {label}") for label in "ABC"]

        assert [item.label for item in service.get_property_states_for_workspace(alice.id, workspace.id)] == [
            "Property A",
            "Property B",
            "Property C",
        ]
        assert service.get_workspace(bob.id, workspace.id) is None
        assert service.get_property_state(bob.id, props[0].id) is None
        with pytest.raises(ValueError, match="Workspace not found"):
            create_property(service, bob.id, workspace.id, "Cross Tenant")


def test_scenario_lineage_tree_assumptions_and_audit_trail(session_factory):
    factory, _ = session_factory
    with factory() as db:
        service = CopilotService(db)
        user = create_user(service, "lineage-user")
        workspace = service.create_workspace(user.id, WorkspaceCreate(name="Scenario Lab"))
        prop = create_property(service, user.id, workspace.id, "Property A")

        scenario_a = service.create_scenario_state(
            user.id,
            ScenarioStateCreate(property_state_id=prop.id, name="Scenario A", modifications={"parking": "unknown"}),
        )
        scenario_b = service.create_scenario_state(
            user.id,
            ScenarioStateCreate(
                property_state_id=prop.id,
                parent_scenario_id=scenario_a.id,
                name="Scenario B",
                modifications={"parking": True},
            ),
        )
        scenario_c = service.create_scenario_state(
            user.id,
            ScenarioStateCreate(
                property_state_id=prop.id,
                parent_scenario_id=scenario_b.id,
                name="Scenario C",
                modifications={"furnishing": "confirmed"},
            ),
        )
        assumption = service.create_assumption(
            user.id,
            AssumptionCreate(
                property_state_id=prop.id,
                scenario_state_id=scenario_c.id,
                key="finishing",
                value=None,
                status="unknown",
                source="broker-input",
            ),
        )
        confirmed = service.update_assumption(
            user.id,
            assumption.id,
            AssumptionUpdate(value="super_lux", status="confirmed", source="user-confirmation"),
        )
        overridden = service.update_assumption(
            user.id,
            assumption.id,
            AssumptionUpdate(value="core_shell", status="overridden", override_reason="Inspection report"),
        )

        lineage = service.get_scenario_lineage(user.id, scenario_c.id)
        tree = service.get_scenario_tree(user.id, prop.id)
        decisions = service.get_decision_history(user.id, workspace.id)

        assert [item.name for item in lineage] == ["Scenario A", "Scenario B", "Scenario C"]
        assert tree[0]["children"][0]["children"][0]["id"] == scenario_c.id
        assert confirmed.confirmed_at is not None
        assert overridden.overridden_at is not None
        assert overridden.override_reason == "Inspection report"
        assert {"property.created", "scenario.forked", "assumption.created", "assumption.updated"} <= {
            item.action for item in decisions
        }


def test_soft_delete_restore_and_tool_event_tenant_safety(session_factory):
    factory, _ = session_factory
    with factory() as db:
        service = CopilotService(db)
        alice = create_user(service, "soft-delete-alice")
        bob = create_user(service, "soft-delete-bob")
        workspace = service.create_workspace(alice.id, WorkspaceCreate(name="Recovery"))
        prop = create_property(service, alice.id, workspace.id, "Property A")

        assert service.delete_property_state(alice.id, prop.id)
        assert service.get_property_state(alice.id, prop.id) is None
        restored = service.restore_property_state(alice.id, prop.id)
        assert restored is not None and restored.is_deleted is False and restored.version > 1

        event = service.record_tool_event(
            alice.id,
            ToolEventCreate(
                workspace_id=workspace.id,
                property_state_id=prop.id,
                tool_name="future-valuator",
                event_type="reserved",
                payload={"mode": "foundation-only"},
            ),
        )
        assert service.get_tool_events(alice.id, workspace.id)[0].id == event.id
        assert service.get_tool_events(bob.id, workspace.id) == []


def test_workspace_restore_recovers_only_children_deleted_by_workspace_cascade(session_factory):
    factory, _ = session_factory
    with factory() as db:
        service = CopilotService(db)
        user = create_user(service, "workspace-cascade")
        workspace = service.create_workspace(user.id, WorkspaceCreate(name="Cascade Restore"))
        prop = create_property(service, user.id, workspace.id, "Property A")
        scenario = service.create_scenario_state(
            user.id,
            ScenarioStateCreate(property_state_id=prop.id, name="Scenario A", modifications={}),
        )
        service.create_assumption(
            user.id,
            AssumptionCreate(
                property_state_id=prop.id,
                scenario_state_id=scenario.id,
                key="parking",
                value=None,
                source="broker-input",
            ),
        )
        cascade_chat = service.create_chat(user.id, ChatCreate(workspace_id=workspace.id, title="Cascade Chat"))
        service.create_message(user.id, MessageCreate(chat_id=cascade_chat.id, role="user", content="Restore me."))
        intentionally_deleted_chat = service.create_chat(
            user.id, ChatCreate(workspace_id=workspace.id, title="Keep Deleted")
        )
        service.create_message(
            user.id, MessageCreate(chat_id=intentionally_deleted_chat.id, role="user", content="Stay deleted.")
        )
        assert service.delete_chat(user.id, intentionally_deleted_chat.id)

        assert service.delete_workspace(user.id, workspace.id)
        restored = service.restore_workspace(user.id, workspace.id)

        assert restored is not None
        assert service.get_chat(user.id, cascade_chat.id) is not None
        assert service.get_messages_for_chat(user.id, cascade_chat.id)[0].content == "Restore me."
        assert service.get_property_state(user.id, prop.id) is not None
        assert service.get_scenario_state(user.id, scenario.id) is not None
        assert service.get_assumptions_for_property(user.id, prop.id)[0].key == "parking"
        assert service.get_chat(user.id, intentionally_deleted_chat.id) is None


def test_chat_and_broker_memory_survive_database_reopen(session_factory):
    factory, db_path = session_factory
    with factory() as db:
        service = CopilotService(db)
        user = create_user(service, "recovery-user")
        workspace = service.create_workspace(user.id, WorkspaceCreate(name="Durable"))
        prop = create_property(service, user.id, workspace.id, "Property A")
        scenario = service.create_scenario_state(
            user.id, ScenarioStateCreate(property_state_id=prop.id, name="Base fork", modifications={})
        )
        child_scenario = service.create_scenario_state(
            user.id,
            ScenarioStateCreate(
                property_state_id=prop.id,
                parent_scenario_id=scenario.id,
                name="Child fork",
                modifications={"parking": "unknown"},
            ),
        )
        service.create_assumption(
            user.id,
            AssumptionCreate(
                property_state_id=prop.id,
                scenario_state_id=child_scenario.id,
                key="parking",
                value=None,
                status="unknown",
                source="broker-input",
            ),
        )
        chat = service.create_chat(user.id, ChatCreate(workspace_id=workspace.id, title="Persistent chat"))
        service.create_message(user.id, MessageCreate(chat_id=chat.id, role="user", content="Remember this."))

        store = BrokerSessionStore()
        store.get_or_create(
            "restart-proof-session",
            db=db,
            user_id=user.id,
            workspace_id=workspace.id,
            scenario_id=child_scenario.id,
        )
        store.record_turn(
            session_id="restart-proof-session",
            message="Remember the district.",
            intent=BrokerIntent.GENERAL_GUIDANCE,
            investor_preferences=None,
            valuation_summary=None,
            analytical_context={"checkpoint": "before-restart"},
            db=db,
        )
        user_id = user.id
        workspace_id = workspace.id
        prop_id = prop.id
        scenario_id = scenario.id
        child_scenario_id = child_scenario.id
        chat_id = chat.id

    reopened_engine = create_engine(f"sqlite:///{db_path}")
    reopened_factory = sessionmaker(bind=reopened_engine)
    with reopened_factory() as db:
        service = CopilotService(db)
        recovered_workspace = service.get_workspace(user_id, workspace_id)
        recovered_prop = service.get_property_state(user_id, prop_id)
        recovered_scenario = service.get_scenario_state(user_id, scenario_id)
        recovered_lineage = service.get_scenario_lineage(user_id, child_scenario_id)
        recovered_assumptions = service.get_assumptions_for_property(user_id, prop_id)
        recovered_messages = service.get_messages_for_chat(user_id, chat_id)
        recovered_broker = BrokerSessionStore().get("restart-proof-session", db=db)

        assert recovered_workspace is not None and recovered_workspace.name == "Durable"
        assert recovered_prop is not None and recovered_prop.label == "Property A"
        assert recovered_scenario is not None and recovered_scenario.name == "Base fork"
        assert [item.name for item in recovered_lineage] == ["Base fork", "Child fork"]
        assert recovered_assumptions[0].status == "unknown"
        assert recovered_messages[0].content == "Remember this."
        assert recovered_broker is not None
        assert recovered_broker.user_id == user_id
        assert recovered_broker.workspace_id == workspace_id
        assert recovered_broker.scenario_id == child_scenario_id
        assert recovered_broker.analytical_context["checkpoint"] == "before-restart"
        assert recovered_broker.previous_requests[0].message == "Remember the district."
    reopened_engine.dispose()


def test_database_constraints_reject_invalid_property(session_factory):
    factory, _ = session_factory
    with factory() as db:
        service = CopilotService(db)
        user = create_user(service, "constraint-user")
        workspace = service.create_workspace(user.id, WorkspaceCreate(name="Constraints"))
        db.add(
            PropertyState(
                user_id=user.id,
                workspace_id=workspace.id,
                label="Invalid",
                location="Nowhere",
                area=0,
                bedrooms=0,
                bathrooms=0,
                amenities={},
            )
        )
        with pytest.raises(IntegrityError):
            db.commit()


def test_database_constraints_reject_cross_tenant_workspace_pair(session_factory):
    factory, _ = session_factory
    with factory() as db:
        service = CopilotService(db)
        alice = create_user(service, "db-tenant-alice")
        bob = create_user(service, "db-tenant-bob")
        workspace = service.create_workspace(alice.id, WorkspaceCreate(name="Alice Workspace"))
        db.add(
            PropertyState(
                user_id=bob.id,
                workspace_id=workspace.id,
                label="Invalid Tenant Pair",
                location="Nowhere",
                area=100,
                bedrooms=1,
                bathrooms=1,
                amenities={},
            )
        )
        with pytest.raises(IntegrityError):
            db.commit()


def test_broker_chat_route_persists_conversation_snapshot_without_tools():
    client = TestClient(fastapi_app)
    session_id = "foundation-route-recovery"
    headers = {"Authorization": f"Bearer {create_access_token(f'route-{session_id}')}"}
    user = client.get("/v1/copilot/users/me", headers=headers).json()
    workspace = client.post("/v1/copilot/workspaces", headers=headers, json={"name": "Route Recovery"}).json()
    prop = client.post(
        "/v1/copilot/properties",
        headers=headers,
        json={
            "workspace_id": workspace["id"],
            "label": "Property A",
            "location": "New Cairo",
            "area": 150,
            "bedrooms": 3,
            "bathrooms": 2,
            "amenities": {},
        },
    ).json()
    scenario = client.post(
        "/v1/copilot/scenarios",
        headers=headers,
        json={"property_state_id": prop["id"], "name": "Base Scenario", "modifications": {}},
    ).json()

    response = client.post(
        "/v1/broker/chat",
        headers=headers,
        json={
            "session_id": session_id,
            "workspace_id": workspace["id"],
            "scenario_id": scenario["id"],
            "message": "Explain what inputs are required before discussing price.",
        },
    )
    assert response.status_code == 200
    assert response.json()["data"]["degraded_mode"] is True

    recovered = client.get(f"/v1/broker/session/{session_id}", headers=headers)
    assert recovered.status_code == 200
    snapshot = recovered.json()["data"]
    assert snapshot["session_id"] == session_id
    assert snapshot["user_id"] == user["id"]
    assert snapshot["workspace_id"] == workspace["id"]
    assert snapshot["scenario_id"] == scenario["id"]
    assert snapshot["previous_requests"][0]["message"].startswith("Explain what inputs")


def test_canonical_forward_only_migration_path_preserves_history():
    expected_historical_checksums = {
        "000_baseline.sql": "75452a0cd308a861053298666623320db398cc302801e804e0f7c394968085a1",
        "001_database_stabilization.sql": "0b11d18c9733e2e54b1a84f39b7117d8a2dd1363e7e76be19bad35b4ce98780e",
        "002_address_resolution_cache.sql": "9994e895fbe2bb0c6adb2428cc02aea57fbd7c705e5eb82574d83fd75431c2b7",
        "003_geospatial_governance.sql": "dba957655f1bf61c700820814d7a713717d60d25e394b1ce094f278773bc14d8",
        "004_property_matrix_amenity_governance.sql": "3c03333fdff48f44b009d8cadc148f6db313d52feaa06dd4ad3fc58d6f74f417",
    }
    for name, checksum in expected_historical_checksums.items():
        assert compute_checksum(MIGRATIONS_DIR / name) == checksum

    migration_names = [path.name for path in sorted(MIGRATIONS_DIR.glob("*.sql"))]
    assert migration_names[-1] == "008_market_insight_analytics_indexes.sql"
    migration = (MIGRATIONS_DIR / "005_copilot_persistence_hardening.sql").read_text(encoding="utf-8")
    for table in [
        "users",
        "workspaces",
        "assumptions",
        "scenario_lineage",
        "tool_events",
        "decision_history",
        "broker_sessions",
        "prediction_logs",
        "shadow_logs",
    ]:
        assert f"CREATE TABLE IF NOT EXISTS {table}" in migration

    tool_migration = (MIGRATIONS_DIR / "007_copilot_tools_valuation_explainability.sql").read_text(encoding="utf-8")
    assert "CREATE TABLE IF NOT EXISTS valuation_snapshots" in tool_migration
    assert "ADD COLUMN IF NOT EXISTS valuation_inputs" in tool_migration

    market_insight_migration = (MIGRATIONS_DIR / "008_market_insight_analytics_indexes.sql").read_text(encoding="utf-8")
    assert "ix_prediction_logs_market_filters" in market_insight_migration
    assert "ix_shadow_logs_market_filters" in market_insight_migration

    compose = (MIGRATIONS_DIR.parents[3] / "docker-compose.yml").read_text(encoding="utf-8")
    assert "python -m app.scripts.run_migrations" in compose
