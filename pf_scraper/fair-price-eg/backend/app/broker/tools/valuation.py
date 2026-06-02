from __future__ import annotations

import time

from sqlalchemy.orm import Session

from app.api.schemas.copilot_tools import ExplainabilityToolRequest, ValuationToolRequest
from app.broker.schemas.contracts import (
    BrokerToolName,
    BrokerToolResult,
    ToolExecutionStatus,
    ValuationAnalysisToolRequest,
    ValuationAnalysisToolResponse,
)
from app.broker.tools.base import BrokerTool
from app.services.copilot_tools_service import CopilotToolsService


class ValuationAnalysisTool(BrokerTool):
    name = BrokerToolName.VALUATION_ANALYSIS
    description = "Adapts broker workspace context to Copilot Valuation Tool and Explainability Tool contracts."

    def execute(
        self,
        *,
        db: Session,
        user_id: int,
        workspace_id: int,
        scenario_id: int,
        **kwargs,
    ) -> BrokerToolResult:
        start = time.perf_counter()
        try:
            adapter_request = ValuationAnalysisToolRequest(
                user_id=user_id,
                workspace_id=workspace_id,
                scenario_id=scenario_id,
            )
            tools = CopilotToolsService(db)
            scenario = tools.copilot.get_scenario_state(adapter_request.user_id, adapter_request.scenario_id)
            if scenario is None or scenario.workspace_id != adapter_request.workspace_id:
                raise ValueError("Scenario not found")

            valuation = tools.execute_valuation(
                adapter_request.user_id,
                ValuationToolRequest(
                    workspace_id=adapter_request.workspace_id,
                    property_id=scenario.property_state_id,
                    scenario_id=scenario.id,
                ),
            )
            explainability = tools.execute_explainability(
                adapter_request.user_id,
                ExplainabilityToolRequest(
                    workspace_id=adapter_request.workspace_id,
                    valuation_id=valuation.valuation_id,
                ),
            )
            response = ValuationAnalysisToolResponse(
                property_id=scenario.property_state_id,
                scenario_id=scenario.id,
                valuation=valuation,
                explainability=explainability,
            )
            duration_ms = (time.perf_counter() - start) * 1000
            return BrokerToolResult(
                tool_name=self.name,
                status=ToolExecutionStatus.SUCCESS,
                duration_ms=round(duration_ms, 2),
                evidence_ids=["valuation.authoritative", "explainability.truth_layer"],
                data=response.model_dump(mode="json"),
            )
        except Exception as exc:
            duration_ms = (time.perf_counter() - start) * 1000
            return BrokerToolResult(
                tool_name=self.name,
                status=ToolExecutionStatus.FAILED,
                duration_ms=round(duration_ms, 2),
                error_code="VALUATION_TOOL_FAILED",
                warnings=[str(exc)],
            )


def valuation_from_result(result: BrokerToolResult) -> ValuationAnalysisToolResponse | None:
    if result.status != ToolExecutionStatus.SUCCESS:
        return None
    return ValuationAnalysisToolResponse.model_validate(result.data)
