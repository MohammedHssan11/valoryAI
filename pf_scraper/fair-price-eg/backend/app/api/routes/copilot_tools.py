from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas.copilot_tools import (
    ComparableToolRequest,
    ComparableToolResponse,
    ExplainabilityToolRequest,
    ExplainabilityToolResponse,
    FairnessToolRequest,
    FairnessToolResponse,
    InvestmentToolRequest,
    InvestmentToolResponse,
    MarketInsightToolRequest,
    MarketInsightToolResponse,
    NegotiationToolRequest,
    NegotiationToolResponse,
    ValuationToolRequest,
    ValuationToolResponse,
    WhatIfToolRequest,
    WhatIfToolResponse,
)
from app.core.auth import get_authenticated_user
from app.db.session import get_db
from app.models.copilot import User
from app.services.copilot_tools_service import CopilotToolsService, ToolPayloadUnavailable, ToolResourceNotFound

router = APIRouter(prefix="/v1/copilot/tools", tags=["copilot-tools"])


def get_tools_service(db: Session = Depends(get_db)) -> CopilotToolsService:
    return CopilotToolsService(db)


def get_actor_user_id(user: User = Depends(get_authenticated_user)) -> int:
    return user.id


@router.post("/valuation", response_model=ValuationToolResponse)
def execute_valuation_tool(
    data: ValuationToolRequest,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotToolsService = Depends(get_tools_service),
):
    try:
        return service.execute_valuation(user_id, data)
    except ToolResourceNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/explainability", response_model=ExplainabilityToolResponse)
def execute_explainability_tool(
    data: ExplainabilityToolRequest,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotToolsService = Depends(get_tools_service),
):
    try:
        return service.execute_explainability(user_id, data)
    except ToolResourceNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ToolPayloadUnavailable as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/comparable", response_model=ComparableToolResponse)
def execute_comparable_tool(
    data: ComparableToolRequest,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotToolsService = Depends(get_tools_service),
):
    try:
        return service.execute_comparable(user_id, data)
    except ToolResourceNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ToolPayloadUnavailable as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/fairness", response_model=FairnessToolResponse)
def execute_fairness_tool(
    data: FairnessToolRequest,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotToolsService = Depends(get_tools_service),
):
    try:
        return service.execute_fairness(user_id, data)
    except ToolResourceNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ToolPayloadUnavailable as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/negotiation", response_model=NegotiationToolResponse)
def execute_negotiation_tool(
    data: NegotiationToolRequest,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotToolsService = Depends(get_tools_service),
):
    try:
        return service.execute_negotiation(user_id, data)
    except ToolResourceNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ToolPayloadUnavailable as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/investment", response_model=InvestmentToolResponse)
def execute_investment_tool(
    data: InvestmentToolRequest,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotToolsService = Depends(get_tools_service),
):
    try:
        return service.execute_investment(user_id, data)
    except ToolResourceNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ToolPayloadUnavailable as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/market-insight", response_model=MarketInsightToolResponse)
def execute_market_insight_tool(
    data: MarketInsightToolRequest,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotToolsService = Depends(get_tools_service),
):
    try:
        return service.execute_market_insight(user_id, data)
    except ToolResourceNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/what-if", response_model=WhatIfToolResponse)
def execute_what_if_tool(
    data: WhatIfToolRequest,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotToolsService = Depends(get_tools_service),
):
    try:
        return service.execute_what_if(user_id, data)
    except ToolResourceNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ToolPayloadUnavailable as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
