from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas.copilot_orchestrator import (
    CopilotOrchestratorRequest,
    CopilotOrchestratorResponse,
)
from app.copilot.orchestrator.runtime import build_copilot_orchestrator_runtime_v1
from app.core.auth import get_authenticated_user
from app.db.session import get_db
from app.models.copilot import User

router = APIRouter(prefix="/v1/copilot/orchestrator", tags=["copilot-orchestrator"])


@router.post(
    "/respond",
    response_model=CopilotOrchestratorResponse,
    summary="Run the governed Copilot orchestrator",
    description=(
        "Runs the approved Intent Engine, Tool Planner, Tool Executor, Response Composer, "
        "Memory Integration, and default-off governed narration handoff."
    ),
)
def orchestrator_respond(
    request: CopilotOrchestratorRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    runtime = build_copilot_orchestrator_runtime_v1(db)
    result = runtime.run(
        user_id=user.id,
        workspace_id=request.workspace_id,
        scenario_id=request.scenario_id,
        broker_session_id=request.broker_session_id,
        user_message=request.message,
        tool_inputs=request.tool_inputs,
    )
    return result.to_delivery_dict()
