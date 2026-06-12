from __future__ import annotations

from sqlalchemy.orm import Session

from app.api.schemas.pricing import RentFairPriceRequest
from app.broker.schemas.contracts import (
    BrokerIntent,
    BrokerStage,
    BrokerToolName,
    BrokerToolResult,
    ValuationAnalysisToolResponse,
)
from app.broker.telemetry.tracing import BrokerTrace
from app.broker.tools.base import BrokerTool
from app.broker.tools.evidence import ExplainabilityTool
from app.broker.tools.valuation import ValuationAnalysisTool


class BrokerToolRegistry:
    def __init__(self, tools: list[BrokerTool] | None = None) -> None:
        default_tools: list[BrokerTool] = [
            ValuationAnalysisTool(),
            ExplainabilityTool(),
        ]
        self._tools = {tool.name: tool for tool in (tools or default_tools)}

    def get(self, name: BrokerToolName) -> BrokerTool:
        return self._tools[name]

    def select_tools(self, *, intent: BrokerIntent, has_valuation_request: bool) -> list[BrokerToolName]:
        if not has_valuation_request:
            return []
        return [BrokerToolName.VALUATION_ANALYSIS, BrokerToolName.EXPLAINABILITY]

    def execute(
        self,
        *,
        tool_name: BrokerToolName,
        db: Session,
        trace: BrokerTrace,
        valuation_request: RentFairPriceRequest | None = None,
        valuation: ValuationAnalysisToolResponse | None = None,
        user_id: int | None = None,
        workspace_id: int | None = None,
        scenario_id: int | None = None,
        stage: BrokerStage = BrokerStage.EVIDENCE_GATHERING,
    ) -> BrokerToolResult:
        trace.add_event(
            stage=stage,
            event_type="tool_started",
            message=f"{tool_name.value} started",
            payload={"tool": tool_name.value},
        )
        result = self.get(tool_name).execute(
            db=db,
            valuation_request=valuation_request,
            valuation=valuation,
            user_id=user_id,
            workspace_id=workspace_id,
            scenario_id=scenario_id,
        )
        trace.record_tool(result.tool_name, result.duration_ms, result.status.value)
        trace.add_event(
            stage=stage,
            event_type="tool_completed",
            message=f"{tool_name.value} completed",
            elapsed_ms=result.duration_ms,
            payload={"tool": tool_name.value, "status": result.status.value},
        )
        return result


tool_registry = BrokerToolRegistry()
