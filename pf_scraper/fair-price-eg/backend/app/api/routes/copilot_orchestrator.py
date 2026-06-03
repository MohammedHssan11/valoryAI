from __future__ import annotations

import logging
import time

from fastapi import APIRouter, Depends, HTTPException, Request, status
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
logger = logging.getLogger(__name__)


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
    request_body: CopilotOrchestratorRequest,
    http_request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    started = time.perf_counter()
    request_id = http_request.headers.get("X-Request-ID") or getattr(
        http_request.state,
        "request_id",
        None,
    )
    logger.info(
        "copilot_orchestrator_request_received",
        extra={
            "request_id": request_id,
            "user_id": user.id,
            "workspace_id": request_body.workspace_id,
            "scenario_id": request_body.scenario_id,
            "broker_session_id": request_body.broker_session_id,
            "message_length": len(request_body.message),
            "tool_input_keys": sorted(request_body.tool_inputs.keys()),
        },
    )

    try:
        runtime = build_copilot_orchestrator_runtime_v1(db)
        result = runtime.run(
            user_id=user.id,
            workspace_id=request_body.workspace_id,
            scenario_id=request_body.scenario_id,
            broker_session_id=request_body.broker_session_id,
            user_message=request_body.message,
            tool_inputs=request_body.tool_inputs,
        )
        delivery = result.to_delivery_dict()
    except ValueError as exc:
        logger.warning(
            "copilot_orchestrator_request_invalid",
            extra={
                "request_id": request_id,
                "user_id": user.id,
                "workspace_id": request_body.workspace_id,
                "error": str(exc),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        logger.exception(
            "copilot_orchestrator_request_failed",
            extra={
                "request_id": request_id,
                "user_id": user.id,
                "workspace_id": request_body.workspace_id,
                "error_type": type(exc).__name__,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Copilot orchestrator is temporarily unavailable. Please retry.",
        ) from exc

    logger.info(
        "copilot_orchestrator_response_ready",
        extra={
            "request_id": request_id,
            "user_id": user.id,
            "workspace_id": request_body.workspace_id,
            "response_id": delivery.get("response_id"),
            "delivery_mode": delivery.get("delivery_mode"),
            "intent": delivery.get("intent"),
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
        },
    )
    return delivery
