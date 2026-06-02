from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.api.schemas.copilot import (
    AssumptionCreate,
    ChatCreate,
    MessageCreate,
    PropertyStateCreate,
    ScenarioStateCreate,
    ToolEventCreate,
    UserCreate,
    WorkspaceCreate,
)
from app.broker.sessions.state import BrokerSessionStore
from app.copilot.orchestrator.composer import ComposedResponse, CompositionStatus
from app.copilot.orchestrator.executor import (
    ExecutionAuditMetadata,
    ExecutionResult,
    ExecutionStatus,
)
from app.copilot.orchestrator.intents import Intent
from app.copilot.orchestrator.memory import (
    ACTIVE_ASSUMPTIONS_LIMIT,
    RECENT_CONVERSATION_METADATA_LIMIT,
    RECENT_DECISIONS_LIMIT,
    RECENT_TOOL_EVENTS_LIMIT,
    RECENT_VALUATIONS_LIMIT,
    DeterministicMemoryIntegration,
    MemoryStatus,
)
from app.copilot.orchestrator.planner import ExecutionStrategy
from app.db.base import Base
from app.models.copilot import ValuationSnapshot
from app.services.copilot_service import CopilotService
import app.models.copilot  # noqa: F401


@pytest.fixture()
def session_factory(tmp_path: Path):
    db_path = tmp_path / "memory-integration.sqlite3"
    engine = create_engine(f"sqlite:///{db_path}")

    @event.listens_for(engine, "connect")
    def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
        dbapi_connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(bind=engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    yield factory, db_path
    engine.dispose()


def _state(service: CopilotService, subject: str):
    user = service.create_user(UserCreate(external_subject=subject, display_name=subject))
    workspace = service.create_workspace(user.id, WorkspaceCreate(name=f"{subject} workspace"))
    prop = service.create_property_state(
        user.id,
        PropertyStateCreate(
            workspace_id=workspace.id,
            label="Property A",
            location="Mivida",
            area=220,
            bedrooms=4,
            bathrooms=3,
            amenities={"codes": ["BA", "SE"]},
            valuation_inputs={"compound_name": "Mivida"},
        ),
    )
    scenario = service.create_scenario_state(
        user.id,
        ScenarioStateCreate(
            property_state_id=prop.id,
            name="Scenario A",
            modifications={"parking": True},
        ),
    )
    return user, workspace, prop, scenario


def _runtime(*, response_id: str = "response_memory_fixture"):
    execution = ExecutionResult(
        execution_id="exec_memory_fixture",
        plan_id="plan_memory_fixture",
        primary_intent=Intent.PROPERTY_COMPARISON,
        secondary_intents=(),
        status=ExecutionStatus.SUCCESS,
        tool_results=(),
        failed_tools=(),
        execution_time_ms=1.0,
        partial_success=False,
        audit_metadata=ExecutionAuditMetadata(
            executed_tools=(),
            successful_tools=(),
            failed_tools=(),
            execution_strategy=ExecutionStrategy.PARALLEL,
            timeout_seconds=30.0,
        ),
    )
    comparison = {
        "status": "AVAILABLE",
        "property_a": {"valuation_id": "val_a", "fair_price": 1_000_000},
        "property_b": {"valuation_id": "val_b", "fair_price": 1_250_000},
        "price_delta": 250_000,
        "price_percentage_delta": 25.0,
    }
    composed = ComposedResponse(
        response_id=response_id,
        execution_id=execution.execution_id,
        plan_id=execution.plan_id,
        primary_intent=execution.primary_intent,
        secondary_intents=execution.secondary_intents,
        status=CompositionStatus.SUCCESS,
        evidence_summary={"property_comparison": comparison},
        citation_package={
            "valuation_ids": ["val_a", "val_b"],
            "tool_event_ids": [],
            "comparable_ids": ["comp_a", "comp_b"],
            "unavailable_optional_citation_types": [],
        },
        compressed_context={},
        frontend_payload={},
        composer_metadata={},
    )
    return execution, composed


def _snapshot(db, *, user_id: int, workspace_id: int, property_id: int, scenario_id: int, index: int):
    db.add(
        ValuationSnapshot(
            valuation_id=f"val_{index:03d}",
            user_id=user_id,
            workspace_id=workspace_id,
            property_state_id=property_id,
            scenario_state_id=scenario_id,
            router_request={"workspace_id": workspace_id},
            normalized_response={
                "valuation_id": f"val_{index:03d}",
                "fair_price": 1_000_000 + index,
                "confidence_level": "High",
                "source": "TruthLayer",
            },
            explainability_payload={
                "comparable_evidence": [
                    {"property_id": f"comp_snapshot_{index}", "price": 900_000 + index}
                ]
            },
        )
    )


def test_memory_context_rebuilds_identically_after_database_reopen(session_factory):
    factory, db_path = session_factory
    with factory() as db:
        service = CopilotService(db)
        user, workspace, prop, scenario = _state(service, "memory-recovery")
        service.create_assumption(
            user.id,
            AssumptionCreate(
                property_state_id=prop.id,
                scenario_state_id=scenario.id,
                key="parking",
                value=True,
                status="confirmed",
                source="user-confirmation",
            ),
        )
        chat = service.create_chat(user.id, ChatCreate(workspace_id=workspace.id, title="Acquisition"))
        service.create_message(user.id, MessageCreate(chat_id=chat.id, role="user", content="Remember this asset."))
        event_row = service.record_tool_event(
            user.id,
            ToolEventCreate(
                workspace_id=workspace.id,
                property_state_id=prop.id,
                scenario_state_id=scenario.id,
                tool_name="comparable",
                event_type="executed",
                payload={
                    "response": {
                        "valuation_id": "val_001",
                        "comparable_ids": ["comp_event_a", "comp_event_b"],
                    }
                },
            ),
        )
        _snapshot(
            db,
            user_id=user.id,
            workspace_id=workspace.id,
            property_id=prop.id,
            scenario_id=scenario.id,
            index=1,
        )
        db.commit()
        BrokerSessionStore().get_or_create(
            "memory-restart-session",
            db=db,
            user_id=user.id,
            workspace_id=workspace.id,
            scenario_id=scenario.id,
        )
        execution, composed = _runtime()
        remembered = DeterministicMemoryIntegration(db).remember(
            user_id=user.id,
            workspace_id=workspace.id,
            scenario_id=scenario.id,
            broker_session_id="memory-restart-session",
            execution_result=execution,
            composed_response=composed,
        )
        loaded = DeterministicMemoryIntegration(db).load_context(
            user_id=user.id,
            workspace_id=workspace.id,
            scenario_id=scenario.id,
            broker_session_id="memory-restart-session",
        )
        user_id = user.id
        workspace_id = workspace.id
        scenario_id = scenario.id

    reopened_engine = create_engine(f"sqlite:///{db_path}")
    reopened_factory = sessionmaker(bind=reopened_engine)
    with reopened_factory() as db:
        recovered = DeterministicMemoryIntegration(db).load_context(
            user_id=user_id,
            workspace_id=workspace_id,
            scenario_id=scenario_id,
            broker_session_id="memory-restart-session",
        )
    reopened_engine.dispose()

    assert remembered.status == MemoryStatus.SUCCESS
    assert remembered.to_dict() == loaded.to_dict() == recovered.to_dict()
    assert remembered.memory_id.startswith("memory_")
    assert remembered.active_comparison_context["price_delta"] == 250_000
    assert remembered.broker_session_context["session_id"] == "memory-restart-session"
    assert remembered.citation_package["workspace_id"] == workspace_id
    assert remembered.citation_package["scenario_id"] == scenario_id
    assert event_row.id in remembered.citation_package["tool_event_ids"]
    assert {"val_a", "val_b", "val_001"} <= set(remembered.citation_package["valuation_ids"])
    assert {"comp_a", "comp_b", "comp_event_a", "comp_event_b", "comp_snapshot_1"} <= set(
        remembered.citation_package["comparable_ids"]
    )
    assert "content" not in remembered.recent_conversation_metadata[0]


def test_memory_fails_closed_for_tenants_deleted_scenarios_and_runtime_mismatch(session_factory):
    factory, _ = session_factory
    with factory() as db:
        service = CopilotService(db)
        alice, workspace, _, scenario = _state(service, "memory-alice")
        bob = service.create_user(UserCreate(external_subject="memory-bob", display_name="Bob"))
        integration = DeterministicMemoryIntegration(db)

        denied = integration.load_context(
            user_id=bob.id,
            workspace_id=workspace.id,
            scenario_id=scenario.id,
        )
        execution, composed = _runtime()
        mismatched = integration.remember(
            user_id=alice.id,
            workspace_id=workspace.id,
            scenario_id=scenario.id,
            execution_result=execution,
            composed_response=replace(composed, execution_id="exec_wrong"),
        )
        partial = integration.remember(
            user_id=alice.id,
            workspace_id=workspace.id,
            scenario_id=scenario.id,
            execution_result=execution,
            composed_response=replace(
                composed,
                response_id="response_partial_memory_fixture",
                status=CompositionStatus.PARTIAL_SUCCESS,
            ),
        )
        service.delete_scenario_state(alice.id, scenario.id)
        deleted = integration.load_context(
            user_id=alice.id,
            workspace_id=workspace.id,
            scenario_id=scenario.id,
        )

    assert denied.status == MemoryStatus.ACCESS_DENIED
    assert denied.workspace_context == {}
    assert deleted.status == MemoryStatus.ACCESS_DENIED
    assert deleted.workspace_context == {}
    assert mismatched.status == MemoryStatus.FAILED
    assert mismatched.memory_metadata["reason_code"] == "RUNTIME_CONTEXT_MISMATCH"
    assert partial.status == MemoryStatus.PARTIAL_SUCCESS


def test_memory_empty_workspace_and_large_history_compression(session_factory):
    factory, _ = session_factory
    with factory() as db:
        service = CopilotService(db)
        user = service.create_user(UserCreate(external_subject="memory-empty", display_name="Empty"))
        empty_workspace = service.create_workspace(user.id, WorkspaceCreate(name="Empty"))
        empty = DeterministicMemoryIntegration(db).load_context(
            user_id=user.id,
            workspace_id=empty_workspace.id,
        )

        history_user, workspace, prop, scenario = _state(service, "memory-history")
        chat = service.create_chat(history_user.id, ChatCreate(workspace_id=workspace.id, title="History"))
        for index in range(RECENT_CONVERSATION_METADATA_LIMIT + 5):
            service.create_message(
                history_user.id,
                MessageCreate(chat_id=chat.id, role="user", content=f"Message {index}"),
            )
        for index in range(RECENT_TOOL_EVENTS_LIMIT + 5):
            service.record_tool_event(
                history_user.id,
                ToolEventCreate(
                    workspace_id=workspace.id,
                    property_state_id=prop.id,
                    scenario_state_id=scenario.id,
                    tool_name="valuation",
                    event_type="executed",
                    payload={"response": {"valuation_id": f"event_val_{index}"}},
                ),
            )
        for index in range(RECENT_VALUATIONS_LIMIT + 3):
            _snapshot(
                db,
                user_id=history_user.id,
                workspace_id=workspace.id,
                property_id=prop.id,
                scenario_id=scenario.id,
                index=index,
            )
        db.commit()
        for index in range(ACTIVE_ASSUMPTIONS_LIMIT + 5):
            service.create_assumption(
                history_user.id,
                AssumptionCreate(
                    property_state_id=prop.id,
                    scenario_state_id=scenario.id,
                    key=f"assumption_{index}",
                    value=index,
                    source="compression-test",
                ),
            )
        context = DeterministicMemoryIntegration(db).load_context(
            user_id=history_user.id,
            workspace_id=workspace.id,
            scenario_id=scenario.id,
        )

    assert empty.status == MemoryStatus.EMPTY_CONTEXT
    assert len(context.recent_tool_history) == RECENT_TOOL_EVENTS_LIMIT
    assert len(context.recent_decisions) == RECENT_DECISIONS_LIMIT
    assert len(context.recent_valuations) == RECENT_VALUATIONS_LIMIT
    assert len(context.active_assumptions) == ACTIVE_ASSUMPTIONS_LIMIT
    assert len(context.recent_conversation_metadata) == RECENT_CONVERSATION_METADATA_LIMIT
    assert all(context.memory_metadata["compression"].values())


def test_memory_source_has_no_prohibited_provider_or_vector_dependencies():
    package_root = Path(__file__).resolve().parents[1] / "copilot" / "orchestrator" / "memory"
    source = "\n".join(
        source_path.read_text(encoding="utf-8").casefold()
        for source_path in package_root.glob("*.py")
    )
    forbidden = (
        "anthropic",
        "chroma",
        "embedding",
        "faiss",
        "gemini",
        "openai",
        "pinecone",
        "weaviate",
    )

    assert [term for term in forbidden if term in source] == []
