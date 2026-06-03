from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


_TOOL_INPUT_ALIASES = {
    "valuation": "VALUATION_TOOL",
    "explainability": "EXPLAINABILITY_TOOL",
    "comparable": "COMPARABLES_TOOL",
    "comparables": "COMPARABLES_TOOL",
    "fairness": "FAIRNESS_TOOL",
    "what_if": "WHAT_IF_TOOL",
    "negotiation": "NEGOTIATION_TOOL",
    "investment": "INVESTMENT_TOOL",
    "market_insight": "MARKET_INSIGHT_TOOL",
}


class CopilotOrchestratorRequest(BaseModel):
    workspace_id: int = Field(gt=0)
    scenario_id: int | None = Field(default=None, gt=0)
    broker_session_id: str | None = Field(default=None, min_length=1, max_length=120)
    message: str = Field(min_length=1, max_length=4000)
    tool_inputs: dict[str, dict[str, Any]] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def normalize_tool_input_aliases(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        tool_inputs = data.get("tool_inputs")
        if not isinstance(tool_inputs, dict):
            return data

        normalized: dict[str, Any] = {}
        for raw_key, payload in tool_inputs.items():
            key = str(raw_key)
            normalized[_TOOL_INPUT_ALIASES.get(key, key)] = payload
        return {**data, "tool_inputs": normalized}


class CopilotOrchestratorResponse(BaseModel):
    runtime_id: Literal["COPILOT_ORCHESTRATOR_LLM_V1"]
    response_id: str
    intent: str
    status: str
    delivery_mode: str
    response: dict[str, Any] | str | None
    citation_package: dict[str, Any] | None
    audit: dict[str, Any]
