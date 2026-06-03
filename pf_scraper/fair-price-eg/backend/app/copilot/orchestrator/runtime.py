from __future__ import annotations

import logging
import time
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.copilot.orchestrator.composer import (
    ComposedResponse,
    DeterministicResponseComposer,
    response_composer,
)
from app.copilot.orchestrator.executor import (
    DeterministicToolExecutor,
    ExecutionResult,
    tool_executor,
)
from app.copilot.orchestrator.intents import IntentResult, RuleBasedIntentEngine, intent_engine
from app.copilot.orchestrator.llm import (
    CopilotOrchestratorLLMV1,
    NarrationResult,
    NarrationScope,
    NarrationStatus,
    build_copilot_orchestrator_llm_v1,
)
from app.copilot.orchestrator.memory import (
    DeterministicMemoryIntegration,
    MemoryContext,
)
from app.copilot.orchestrator.planner import (
    DeterministicToolPlanner,
    ExecutionPlan,
    PlannedToolCall,
    tool_planner,
)


RUNTIME_ID = "COPILOT_ORCHESTRATOR_LLM_V1"
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CopilotOrchestratorRuntimeResult:
    intent_result: IntentResult
    execution_plan: ExecutionPlan
    execution_result: ExecutionResult
    composed_response: ComposedResponse
    memory_context: MemoryContext
    narration_result: NarrationResult

    def to_delivery_dict(self) -> dict[str, Any]:
        narration = self.narration_result
        if narration.status == NarrationStatus.ACCEPT_NARRATION:
            delivery_mode = "GROUNDED_NARRATION"
            response: dict[str, Any] | str | None = narration.narrated_text
        elif narration.status == NarrationStatus.ACCESS_DENIED:
            return {
                "runtime_id": RUNTIME_ID,
                "response_id": narration.response_id,
                "intent": self.intent_result.intent.value,
                "status": narration.status.value,
                "delivery_mode": "ACCESS_DENIED",
                "response": None,
                "citation_package": None,
                "audit": {"narration_status": narration.status.value},
            }
        else:
            delivery_mode = "DETERMINISTIC_FALLBACK"
            response = narration.deterministic_fallback_payload
        return {
            "runtime_id": RUNTIME_ID,
            "response_id": narration.response_id,
            "intent": self.intent_result.intent.value,
            "status": narration.status.value,
            "delivery_mode": delivery_mode,
            "response": response,
            "citation_package": narration.citation_package,
            "audit": {
                "plan_id": self.execution_plan.plan_id,
                "execution_id": self.execution_result.execution_id,
                "composition_status": self.composed_response.status.value,
                "memory_id": self.memory_context.memory_id,
                "memory_status": self.memory_context.status.value,
                "narration_status": narration.status.value,
            },
        }


class CopilotOrchestratorRuntimeV1:
    """Thin activation layer for the approved governed Copilot sequence."""

    def __init__(
        self,
        *,
        intents: RuleBasedIntentEngine,
        planner: DeterministicToolPlanner,
        executor: DeterministicToolExecutor,
        composer: DeterministicResponseComposer,
        memory: DeterministicMemoryIntegration,
        narrator: CopilotOrchestratorLLMV1,
    ) -> None:
        self.intents = intents
        self.planner = planner
        self.executor = executor
        self.composer = composer
        self.memory = memory
        self.narrator = narrator

    def run(
        self,
        *,
        user_id: int,
        workspace_id: int,
        user_message: str,
        tool_inputs: Mapping[PlannedToolCall | str, BaseModel | Mapping[str, Any]],
        scenario_id: int | None = None,
        broker_session_id: str | None = None,
    ) -> CopilotOrchestratorRuntimeResult:
        started = time.perf_counter()
        logger.info(
            "copilot_runtime_started",
            extra={
                "runtime_id": RUNTIME_ID,
                "user_id": user_id,
                "workspace_id": workspace_id,
                "scenario_id": scenario_id,
                "broker_session_id": broker_session_id,
                "message_length": len(user_message),
                "tool_input_keys": sorted(str(key) for key in tool_inputs.keys()),
            },
        )
        intent_result = self.intents.classify(user_message)
        logger.info(
            "copilot_runtime_intent_classified",
            extra={
                "runtime_id": RUNTIME_ID,
                "user_id": user_id,
                "workspace_id": workspace_id,
                "intent": intent_result.intent.value,
                "confidence": intent_result.confidence.value,
            },
        )
        execution_plan = self.planner.plan(intent_result)
        logger.info(
            "copilot_runtime_plan_created",
            extra={
                "runtime_id": RUNTIME_ID,
                "user_id": user_id,
                "workspace_id": workspace_id,
                "plan_id": execution_plan.plan_id,
                "tools": [tool.value for tool in execution_plan.tools],
                "strategy": execution_plan.execution_strategy.value,
            },
        )
        execution_result = self.executor.execute(
            execution_plan,
            user_id=user_id,
            tool_inputs=tool_inputs,
        )
        logger.info(
            "copilot_runtime_tools_executed",
            extra={
                "runtime_id": RUNTIME_ID,
                "user_id": user_id,
                "workspace_id": workspace_id,
                "execution_id": execution_result.execution_id,
                "status": execution_result.status.value,
                "successful_tools": [
                    result.planned_tool.value for result in execution_result.tool_results
                ],
                "failed_tools": [
                    failure.planned_tool.value for failure in execution_result.failed_tools
                ],
            },
        )
        composed_response = self.composer.compose(execution_result)
        logger.info(
            "copilot_runtime_response_composed",
            extra={
                "runtime_id": RUNTIME_ID,
                "user_id": user_id,
                "workspace_id": workspace_id,
                "response_id": composed_response.response_id,
                "composition_status": composed_response.status.value,
            },
        )
        memory_context = self.memory.remember(
            user_id=user_id,
            workspace_id=workspace_id,
            scenario_id=scenario_id,
            broker_session_id=broker_session_id,
            execution_result=execution_result,
            composed_response=composed_response,
        )
        logger.info(
            "copilot_runtime_memory_recorded",
            extra={
                "runtime_id": RUNTIME_ID,
                "user_id": user_id,
                "workspace_id": workspace_id,
                "memory_id": memory_context.memory_id,
                "memory_status": memory_context.status.value,
            },
        )
        narration_result = self.narrator.narrate(
            scope=NarrationScope(
                user_id=user_id,
                workspace_id=workspace_id,
                scenario_id=scenario_id,
                broker_session_id=broker_session_id,
            ),
            user_message=user_message,
            composed_response=composed_response,
            memory_context=memory_context,
        )
        logger.info(
            "copilot_runtime_narration_completed",
            extra={
                "runtime_id": RUNTIME_ID,
                "user_id": user_id,
                "workspace_id": workspace_id,
                "response_id": narration_result.response_id,
                "narration_status": narration_result.status.value,
                "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
            },
        )
        return CopilotOrchestratorRuntimeResult(
            intent_result=intent_result,
            execution_plan=execution_plan,
            execution_result=execution_result,
            composed_response=composed_response,
            memory_context=memory_context,
            narration_result=narration_result,
        )


def build_copilot_orchestrator_runtime_v1(db: Session) -> CopilotOrchestratorRuntimeV1:
    return CopilotOrchestratorRuntimeV1(
        intents=intent_engine,
        planner=tool_planner,
        executor=tool_executor,
        composer=response_composer,
        memory=DeterministicMemoryIntegration(db),
        narrator=build_copilot_orchestrator_llm_v1(),
    )
