from __future__ import annotations

import uuid

from app.copilot.orchestrator.llm import NarrationStatus
from app.copilot.orchestrator.runtime import (
    RUNTIME_ID,
    build_copilot_orchestrator_runtime_v1,
)
from app.db.session import SessionLocal
from app.models.copilot import User, Workspace


def _workspace() -> tuple[int, int]:
    with SessionLocal() as db:
        user = User(
            external_subject=f"orchestrator-runtime-{uuid.uuid4().hex}",
            display_name="Orchestrator Runtime User",
        )
        db.add(user)
        db.flush()
        workspace = Workspace(user_id=user.id, name="Orchestrator Runtime Workspace")
        db.add(workspace)
        db.commit()
        return user.id, workspace.id


def test_runtime_sequences_clarification_through_memory_and_deterministic_delivery():
    user_id, workspace_id = _workspace()
    with SessionLocal() as db:
        result = build_copilot_orchestrator_runtime_v1(db).run(
            user_id=user_id,
            workspace_id=workspace_id,
            user_message="Tell me more",
            tool_inputs={},
        )

    delivery = result.to_delivery_dict()
    assert result.execution_plan.requires_clarification is True
    assert result.execution_result.status.value == "CLARIFICATION_REQUIRED"
    assert result.composed_response.status.value == "CLARIFICATION_REQUIRED"
    assert result.narration_result.status == NarrationStatus.DETERMINISTIC_ONLY
    assert delivery["runtime_id"] == RUNTIME_ID
    assert delivery["delivery_mode"] == "DETERMINISTIC_FALLBACK"
    assert delivery["response"] is not None
    assert delivery["audit"]["memory_id"].startswith("memory_")


def test_runtime_access_denial_redacts_scope_dependent_delivery_metadata():
    user_id, _ = _workspace()
    with SessionLocal() as db:
        result = build_copilot_orchestrator_runtime_v1(db).run(
            user_id=user_id,
            workspace_id=999_999,
            user_message="Tell me more",
            tool_inputs={},
        )

    delivery = result.to_delivery_dict()
    assert result.narration_result.status == NarrationStatus.ACCESS_DENIED
    assert delivery == {
        "runtime_id": RUNTIME_ID,
        "response_id": result.narration_result.response_id,
        "intent": result.intent_result.intent.value,
        "status": "ACCESS_DENIED",
        "delivery_mode": "ACCESS_DENIED",
        "response": None,
        "citation_package": None,
        "audit": {"narration_status": "ACCESS_DENIED"},
    }
