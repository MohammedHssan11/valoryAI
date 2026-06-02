from __future__ import annotations

import asyncio
import json
import time
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.schemas.common import SuccessResponse, success_response
from app.broker.orchestrator.core import broker_orchestrator
from app.broker.schemas.contracts import (
    BrokerAnalyzeRequest,
    BrokerChatRequest,
    BrokerIntentClassification,
    BrokerIntentRequest,
    BrokerOrchestrationResponse,
    BrokerReasonRequest,
    BrokerSessionSnapshot,
    BrokerStage,
    BrokerStageEvent,
)
from app.broker.sessions.state import session_store
from app.core.auth import get_authenticated_user
from app.core.observability import metrics
from app.db.session import SessionLocal, get_db
from app.models.copilot import User

router = APIRouter(prefix="/v1/broker", tags=["broker"])


def _bind_broker_request(req, *, user_id: int, db: Session):
    session_id = req.session_id or session_store.new_session_id()
    try:
        session_store.get_or_create(
            session_id,
            db=db,
            user_id=user_id,
            workspace_id=req.workspace_id,
            scenario_id=req.scenario_id,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=404, detail="Broker session was not found.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return req.model_copy(update={"session_id": session_id})


@router.post(
    "/analyze",
    response_model=SuccessResponse[BrokerOrchestrationResponse],
    summary="Run grounded broker analysis",
    description=(
        "Runs the Phase 2A broker orchestration pipeline: intent analysis, deterministic tool execution, "
        "context assembly, structured response formatting, and grounding validation."
    ),
)
def broker_analyze(
    req: BrokerAnalyzeRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    req = _bind_broker_request(req, user_id=user.id, db=db)
    return success_response(broker_orchestrator.analyze(req, db))


@router.post(
    "/chat",
    response_model=SuccessResponse[BrokerOrchestrationResponse],
    summary="Run broker chat turn",
    description=(
        "Accepts a broker conversation turn. When valuation inputs are supplied, the deterministic backend is "
        "called before any analytical response is produced."
    ),
)
def broker_chat(
    req: BrokerChatRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    req = _bind_broker_request(req, user_id=user.id, db=db)
    return success_response(broker_orchestrator.chat(req, db))


@router.post(
    "/intent",
    response_model=SuccessResponse[BrokerIntentClassification],
    summary="Classify broker analytical intent",
    description="Runs low-latency rule-assisted broker intent classification without calling deterministic tools or LLMs.",
)
def broker_intent(req: BrokerIntentRequest, user: User = Depends(get_authenticated_user)):
    return success_response(broker_orchestrator.classify_intent(req))


@router.post(
    "/reason",
    response_model=SuccessResponse[BrokerOrchestrationResponse],
    summary="Run structured broker reasoning",
    description=(
        "Runs the Phase 2B structured reasoning pipeline: intent classification, reasoning plan generation, "
        "deterministic evidence execution, grounded narration, validation, and response governance."
    ),
)
def broker_reason(
    req: BrokerReasonRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    req = _bind_broker_request(req, user_id=user.id, db=db)
    return success_response(broker_orchestrator.reason(req, db))


@router.post(
    "/stream",
    summary="Stream broker reasoning events",
    description="Returns server-sent events for staged broker reasoning visualization and final governed response delivery.",
)
async def broker_stream(
    req: BrokerReasonRequest,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    req = _bind_broker_request(req, user_id=user.id, db=db)
    stream_started = time.perf_counter()

    async def event_stream():
        loop = asyncio.get_running_loop()
        queue: asyncio.Queue[tuple[str, BrokerStageEvent | BrokerOrchestrationResponse | None]] = asyncio.Queue()
        sent_events = 0
        closed = False

        def enqueue(kind: str, payload: BrokerStageEvent | BrokerOrchestrationResponse | None = None) -> None:
            if closed:
                return
            loop.call_soon_threadsafe(queue.put_nowait, (kind, payload))

        def enqueue_trace_event(event: BrokerStageEvent) -> None:
            enqueue("event", event)

        def run_orchestration() -> None:
            db = SessionLocal()
            try:
                response = broker_orchestrator.reason(req, db, event_handler=enqueue_trace_event)
                enqueue("final_response", response)
            except Exception as exc:
                metrics.increment("broker.stream_failed", {"error_type": type(exc).__name__})
                enqueue(
                    "event",
                    BrokerStageEvent(
                        event_id=f"evt_{uuid.uuid4().hex[:12]}",
                        stage=BrokerStage.FINALIZE_RESPONSE,
                        event_type="stream_error",
                        message="Broker stream failed before final response delivery",
                        elapsed_ms=(time.perf_counter() - stream_started) * 1000,
                        payload={"error_type": type(exc).__name__, "error": str(exc)},
                    ),
                )
            finally:
                db.close()
                enqueue("done")

        worker = asyncio.create_task(asyncio.to_thread(run_orchestration))
        try:
            while True:
                if await request.is_disconnected():
                    metrics.increment("broker.stream_disconnected", {})
                    break

                kind, payload = await queue.get()
                if kind == "done":
                    break

                if kind == "event":
                    assert isinstance(payload, BrokerStageEvent)
                    sent_events += 1
                    event_payload = payload.model_dump(mode="json")
                    event_payload["payload"] = {
                        **event_payload.get("payload", {}),
                        "stream_event_index": sent_events,
                        "stream_elapsed_ms": round((time.perf_counter() - stream_started) * 1000, 2),
                    }
                    metrics.increment("broker.stream_event", {"event_type": payload.event_type, "stage": payload.stage.value})
                    sse_event_type = "reasoning_event" if payload.event_type == "final_response" else payload.event_type
                    yield _sse(sse_event_type, event_payload)
                    continue

                if kind == "final_response":
                    assert isinstance(payload, BrokerOrchestrationResponse)
                    duration_ms = (time.perf_counter() - stream_started) * 1000
                    completed = BrokerStageEvent(
                        event_id=f"evt_{uuid.uuid4().hex[:12]}",
                        stage=BrokerStage.FINALIZE_RESPONSE,
                        event_type="stream_completed",
                        message="Broker stream completed",
                        elapsed_ms=duration_ms,
                        payload={
                            "stream_duration_ms": round(duration_ms, 2),
                            "stream_event_count": sent_events,
                            "session_id": payload.session_id,
                        },
                    )
                    metrics.observe("broker.stream_duration_ms", duration_ms, {"intent": payload.intent.value})
                    metrics.increment("broker.stream_completed", {"intent": payload.intent.value})
                    yield _sse("stream_completed", completed.model_dump(mode="json"))
                    yield _sse("final_response", payload.model_dump(mode="json"))
        finally:
            closed = True

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.get(
    "/session/{session_id}",
    response_model=SuccessResponse[BrokerSessionSnapshot],
    summary="Fetch lightweight broker session state",
    description="Returns the in-memory broker session state used for Phase 2A analytical continuity.",
)
def get_broker_session(
    session_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    snapshot = session_store.get(session_id, db=db, user_id=user.id)
    if snapshot is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "BROKER_SESSION_NOT_FOUND",
                "message": "Broker session was not found.",
            },
        )
    return success_response(snapshot)


def _sse(event_type: str, payload: dict) -> str:
    return f"event: {event_type}\ndata: {json.dumps(payload, default=str)}\n\n"
