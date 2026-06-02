from __future__ import annotations

import logging
from typing import Callable

from sqlalchemy.orm import Session

from app.api.schemas.pricing import RentFairPriceRequest
from app.broker.context.assembler import BrokerContextAssembler, context_assembler
from app.broker.dialogue.engine import AnalyticalDialogueEngine, analytical_dialogue_engine
from app.broker.governance.response import ResponseGovernanceLayer, response_governance
from app.broker.intents.classifier import BrokerIntentClassifier, intent_classifier
from app.broker.reasoning.planner import ReasoningPlanBuilder, reasoning_plan_builder
from app.broker.reasoning.runtime import ReasoningStageRuntime, reasoning_stage_runtime
from app.broker.schemas.contracts import (
    BrokerAnalyzeRequest,
    BrokerChatRequest,
    BrokerContext,
    BrokerIntentClassification,
    BrokerIntentRequest,
    BrokerOrchestrationResponse,
    BrokerReasonRequest,
    BrokerReasoningPlan,
    BrokerStage,
    BrokerToolName,
    BrokerToolResult,
    GroundingReport,
    InvestorPreferences,
    ResponseGovernanceReport,
    ToolExecutionStatus,
    ValuationAnalysisToolResponse,
    BrokerStageEvent,
)
from app.broker.services.formatter import AIResponseFormatter, response_formatter
from app.broker.services.narration import DeterministicBrokerNarrationRuntime, deterministic_narration_runtime
from app.broker.sessions.state import BrokerSessionStore, session_store
from app.broker.telemetry.tracing import BrokerTrace
from app.broker.tools.registry import BrokerToolRegistry, tool_registry
from app.broker.tools.valuation import valuation_from_result
from app.broker.validators.grounding import GroundingValidator, grounding_validator
from app.core.observability import metrics

logger = logging.getLogger(__name__)


class BrokerOrchestrator:
    def __init__(
        self,
        *,
        registry: BrokerToolRegistry,
        assembler: BrokerContextAssembler,
        formatter: AIResponseFormatter,
        validator: GroundingValidator,
        sessions: BrokerSessionStore,
        classifier: BrokerIntentClassifier,
        planner: ReasoningPlanBuilder,
        runtime: ReasoningStageRuntime,
        narrator: DeterministicBrokerNarrationRuntime,
        governance: ResponseGovernanceLayer,
        dialogue: AnalyticalDialogueEngine,
    ) -> None:
        self.registry = registry
        self.assembler = assembler
        self.formatter = formatter
        self.validator = validator
        self.sessions = sessions
        self.classifier = classifier
        self.planner = planner
        self.runtime = runtime
        self.narrator = narrator
        self.governance = governance
        self.dialogue = dialogue

    def classify_intent(self, request: BrokerIntentRequest) -> BrokerIntentClassification:
        return self.classifier.classify(
            message=request.message,
            has_valuation_request=request.has_valuation_request,
        )

    def analyze(self, request: BrokerAnalyzeRequest, db: Session) -> BrokerOrchestrationResponse:
        return self._run(
            db=db,
            session_id=request.session_id,
            message=request.message,
            valuation_request=request.valuation_request,
            investor_preferences=request.investor_preferences,
        )

    def chat(self, request: BrokerChatRequest, db: Session) -> BrokerOrchestrationResponse:
        return self._run(
            db=db,
            session_id=request.session_id,
            message=request.message,
            valuation_request=request.valuation_request,
            investor_preferences=request.investor_preferences,
        )

    def reason(
        self,
        request: BrokerReasonRequest,
        db: Session,
        event_handler: Callable[[BrokerStageEvent], None] | None = None,
    ) -> BrokerOrchestrationResponse:
        return self._run(
            db=db,
            session_id=request.session_id,
            message=request.message,
            valuation_request=request.valuation_request,
            investor_preferences=request.investor_preferences,
            event_handler=event_handler,
        )

    def _run(
        self,
        *,
        db: Session,
        session_id: str | None,
        message: str,
        valuation_request: RentFairPriceRequest | None,
        investor_preferences: InvestorPreferences | None,
        event_handler: Callable[[BrokerStageEvent], None] | None = None,
    ) -> BrokerOrchestrationResponse:
        session = self.sessions.get_or_create(session_id, db=db)
        trace = BrokerTrace(session.session_id, event_handler=event_handler)

        classification = self.runtime.execute(
            trace=trace,
            stage=BrokerStage.CLASSIFY_INTENT,
            message="Classifying analytical broker intent",
            operation=lambda: self.classifier.classify(
                message=message,
                has_valuation_request=valuation_request is not None,
            ),
        )
        intent = classification.intent
        trace.add_event(
            stage=BrokerStage.CLASSIFY_INTENT,
            event_type="confidence_update",
            message=f"Intent resolved as {intent.value}",
            payload={
                "intent": intent.value,
                "confidence": classification.confidence,
                "fallback": classification.fallback,
            },
        )

        plan = self.runtime.execute(
            trace=trace,
            stage=BrokerStage.BUILD_REASONING_PLAN,
            message="Building deterministic reasoning plan",
            operation=lambda: self._build_reasoning_plan(classification, valuation_request is not None),
        )
        trace.add_event(
            stage=BrokerStage.BUILD_REASONING_PLAN,
            event_type="stage_progress",
            message="Reasoning plan selected deterministic stages and tools",
            payload={
                "plan_id": plan.plan_id,
                "selected_tools": [tool.value for tool in plan.selected_tools],
                "stage_count": len(plan.stages),
                "degraded_mode_reasons": plan.degraded_mode_reasons,
            },
        )

        tool_results, valuation = self.runtime.execute(
            trace=trace,
            stage=BrokerStage.EXECUTE_TOOLS,
            message="Executing deterministic evidence tools",
            operation=lambda: self._execute_tool_plan(
                db=db,
                trace=trace,
                plan=plan,
                valuation_request=valuation_request,
                user_id=session.user_id,
                workspace_id=session.workspace_id,
                scenario_id=session.scenario_id,
            ),
        )

        dialogue_context = self.dialogue.continuity_context(session=session, classification=classification)
        context = self.runtime.execute(
            trace=trace,
            stage=BrokerStage.ASSEMBLE_CONTEXT,
            message="Assembling grounded broker context",
            operation=lambda: self.assembler.assemble(
                intent=intent,
                session=session,
                message=message,
                tool_results=tool_results,
                dialogue_context=dialogue_context,
            ),
        )
        trace.add_event(
            stage=BrokerStage.ASSEMBLE_CONTEXT,
            event_type="stage_progress",
            message="Grounded context assembled",
            payload={
                "evidence_count": len(context.evidence),
                "comparable_count": len(context.comparable_evidence),
                "has_valuation_summary": context.valuation_summary is not None,
                "estimated_context_tokens": context.token_budget.estimated_context_tokens,
            },
        )

        narration = self.runtime.execute(
            trace=trace,
            stage=BrokerStage.GENERATE_NARRATION,
            message="Generating governed analytical narration",
            operation=lambda: self.narrator.generate(
                context=context,
                plan=plan,
                on_chunk=lambda text, payload: self._record_narration_chunk(trace, text, payload),
            ),
        )
        response = narration.response

        grounding = self.runtime.execute(
            trace=trace,
            stage=BrokerStage.VALIDATE_GROUNDING,
            message="Validating deterministic grounding",
            operation=lambda: self._validate_grounding(trace=trace, context=context, response=response),
        )

        response, grounding, governance = self.runtime.execute(
            trace=trace,
            stage=BrokerStage.FINALIZE_RESPONSE,
            message="Applying response governance and finalizing broker output",
            operation=lambda: self._finalize_response(
                trace=trace,
                context=context,
                response=response,
                grounding=grounding,
            ),
        )

        self.sessions.record_turn(
            session_id=session.session_id,
            message=message,
            intent=intent,
            investor_preferences=investor_preferences,
            valuation_summary=context.valuation_summary,
            analytical_context={
                "last_intent": intent.value,
                "last_intent_confidence": classification.confidence,
                "last_grounding_status": grounding.status,
                "last_governance_status": governance.status,
                "last_reasoning_plan_id": plan.plan_id,
                "last_narration_provider": narration.telemetry.provider,
            },
            db=db,
        )
        degraded_mode = (
            context.valuation_summary is None
            or grounding.status == "failed"
            or governance.status == "failed"
            or bool(plan.degraded_mode_reasons)
        )
        metrics.increment("broker.request", {"intent": intent.value, "grounding": grounding.status})
        metrics.increment("broker.reasoning_request", {"intent": intent.value, "governance": governance.status})
        metrics.record_event(
            "broker_orchestration",
            {
                "session_id": session.session_id,
                "intent": intent.value,
                "intent_confidence": classification.confidence,
                "tool_count": len(tool_results),
                "grounding": grounding.status,
                "governance": governance.status,
                "degraded_mode": degraded_mode,
                "narration_provider": narration.telemetry.provider,
            },
        )

        return BrokerOrchestrationResponse(
            session_id=session.session_id,
            intent=intent,
            response=response,
            grounding=grounding,
            context=context,
            tool_results=tool_results,
            events=trace.events,
            degraded_mode=degraded_mode,
            intent_classification=classification,
            reasoning_plan=plan,
            narration=narration.telemetry,
            governance=governance,
        )

    def _build_reasoning_plan(
        self,
        classification: BrokerIntentClassification,
        has_valuation_request: bool,
    ) -> BrokerReasoningPlan:
        selected_tools = self.registry.select_tools(
            intent=classification.intent,
            has_valuation_request=has_valuation_request,
        )
        return self.planner.build(classification=classification, selected_tools=selected_tools)

    def _execute_tool_plan(
        self,
        *,
        db: Session,
        trace: BrokerTrace,
        plan: BrokerReasoningPlan,
        valuation_request: RentFairPriceRequest | None,
        user_id: int,
        workspace_id: int,
        scenario_id: int,
    ) -> tuple[list[BrokerToolResult], ValuationAnalysisToolResponse | None]:
        tool_results: list[BrokerToolResult] = []
        valuation: ValuationAnalysisToolResponse | None = None

        for tool_name in plan.selected_tools:
            trace.add_event(
                stage=BrokerStage.EXECUTE_TOOLS,
                event_type="stage_progress",
                message=f"Preparing deterministic tool {tool_name.value}",
                payload={"tool": tool_name.value},
            )
            result = self.registry.execute(
                tool_name=tool_name,
                db=db,
                trace=trace,
                valuation_request=valuation_request,
                valuation=valuation,
                user_id=user_id,
                workspace_id=workspace_id,
                scenario_id=scenario_id,
                stage=BrokerStage.EXECUTE_TOOLS,
            )
            tool_results.append(result)
            if tool_name == BrokerToolName.VALUATION_ANALYSIS:
                valuation = valuation_from_result(result)
                if valuation is not None:
                    trace.add_event(
                        stage=BrokerStage.EXECUTE_TOOLS,
                        event_type="confidence_update",
                        message="TruthLayer valuation and explainability resolved through Copilot tools",
                        payload={
                            "valuation_id": valuation.valuation.valuation_id,
                            "confidence_label": valuation.valuation.confidence_level,
                            "engine_used": valuation.valuation.engine_used,
                            "routing_reason": valuation.valuation.routing_reason,
                            "source": valuation.valuation.source,
                            "explainability_source": valuation.explainability.source,
                        },
                    )
            if result.status == ToolExecutionStatus.FAILED:
                logger.warning(
                    "broker_tool_failed",
                    extra={
                        "session_id": trace.session_id,
                        "tool": tool_name.value,
                        "error_code": result.error_code,
                        "warnings": result.warnings,
                    },
                )
        return tool_results, valuation

    def _record_narration_chunk(self, trace: BrokerTrace, text: str, payload: dict) -> None:
        trace.add_event(
            stage=BrokerStage.GENERATE_NARRATION,
            event_type="narration_chunk",
            message=text,
            payload={"delta": text, **payload},
        )

    def _validate_grounding(
        self,
        *,
        trace: BrokerTrace,
        context: BrokerContext,
        response,
    ) -> GroundingReport:
        grounding = self.validator.validate(context=context, response=response)
        trace.add_event(
            stage=BrokerStage.VALIDATE_GROUNDING,
            event_type="validation",
            message=f"Grounding validation {grounding.status}",
            payload={"violations": grounding.violations},
        )
        trace.add_event(
            stage=BrokerStage.VALIDATE_GROUNDING,
            event_type="governance_update",
            message=f"Deterministic grounding {grounding.status}",
            payload={"status": grounding.status, "violations": grounding.violations},
        )
        return grounding

    def _finalize_response(
        self,
        *,
        trace: BrokerTrace,
        context: BrokerContext,
        response,
        grounding: GroundingReport,
    ) -> tuple[object, GroundingReport, ResponseGovernanceReport]:
        governance = self.governance.evaluate(context=context, response=response, grounding=grounding)
        trace.add_event(
            stage=BrokerStage.FINALIZE_RESPONSE,
            event_type="governance_check",
            message=f"Response governance {governance.status}",
            payload={"violations": governance.violations},
        )
        trace.add_event(
            stage=BrokerStage.FINALIZE_RESPONSE,
            event_type="governance_update",
            message=f"Response governance {governance.status}",
            payload={
                "status": governance.status,
                "violations": governance.violations,
                "sanitized": governance.sanitized,
            },
        )
        if grounding.status == "passed" and governance.status == "passed":
            self._record_final_narration_chunks(trace, response)
            trace.add_event(
                stage=BrokerStage.FINALIZE_RESPONSE,
                event_type="final_response",
                message="Broker response finalized",
            )
            return response, grounding, governance

        fallback_response = self.formatter.safety_fallback(context, grounding)
        fallback_grounding = self.validator.validate(context=context, response=fallback_response)
        fallback_governance = self.governance.evaluate(
            context=context,
            response=fallback_response,
            grounding=fallback_grounding,
        ).model_copy(update={"sanitized": True})
        self._record_final_narration_chunks(trace, fallback_response)
        trace.add_event(
            stage=BrokerStage.FINALIZE_RESPONSE,
            event_type="final_response",
            message="Broker response finalized in safety fallback mode",
            payload={
                "grounding": fallback_grounding.status,
                "governance": fallback_governance.status,
                "sanitized": True,
            },
        )
        return fallback_response, fallback_grounding, fallback_governance

    def _record_final_narration_chunks(self, trace: BrokerTrace, response) -> None:
        chunks = [
            response.executive_summary,
            response.valuation_interpretation,
            response.comparable_reasoning,
            response.district_insights,
            response.confidence_explanation,
            response.analytical_conclusion,
        ]
        for index, chunk in enumerate(chunks):
            if not chunk:
                continue
            text = f"{chunk} "
            trace.add_event(
                stage=BrokerStage.FINALIZE_RESPONSE,
                event_type="narration_chunk",
                message=text,
                payload={"delta": text, "chunk_index": index, "validated": True},
            )


broker_orchestrator = BrokerOrchestrator(
    registry=tool_registry,
    assembler=context_assembler,
    formatter=response_formatter,
    validator=grounding_validator,
    sessions=session_store,
    classifier=intent_classifier,
    planner=reasoning_plan_builder,
    runtime=reasoning_stage_runtime,
    narrator=deterministic_narration_runtime,
    governance=response_governance,
    dialogue=analytical_dialogue_engine,
)
