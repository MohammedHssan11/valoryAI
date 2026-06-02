from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class CopilotOrchestratorRequest(BaseModel):
    workspace_id: int = Field(gt=0)
    scenario_id: int | None = Field(default=None, gt=0)
    broker_session_id: str | None = Field(default=None, min_length=1, max_length=120)
    message: str = Field(min_length=1, max_length=4000)
    tool_inputs: dict[str, dict[str, Any]] = Field(default_factory=dict)


class CopilotOrchestratorResponse(BaseModel):
    runtime_id: Literal["COPILOT_ORCHESTRATOR_LLM_V1"]
    response_id: str
    intent: str
    status: str
    delivery_mode: str
    response: dict[str, Any] | str | None
    citation_package: dict[str, Any] | None
    audit: dict[str, Any]
