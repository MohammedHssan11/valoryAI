from __future__ import annotations

from collections.abc import Mapping
from concurrent.futures import Future, ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from dataclasses import dataclass
import time
from typing import Any
import uuid

from pydantic import BaseModel

from app.api.schemas.copilot_tools import (
    ComparableToolRequest,
    ExplainabilityToolRequest,
    FairnessToolRequest,
    InvestmentToolRequest,
    MarketInsightToolRequest,
    NegotiationToolRequest,
    ValuationToolRequest,
    WhatIfToolRequest,
)
from app.copilot.orchestrator.executor.contracts import (
    ExecutionAuditMetadata,
    ExecutionResult,
    ExecutionStatus,
    ToolExecutionFailure,
    ToolExecutionResult,
    ToolOrderingMetadata,
)
from app.copilot.orchestrator.planner import ExecutionPlan, ExecutionStrategy, PlannedToolCall
from app.db.session import SessionLocal
from app.services.copilot_tools_service import CopilotToolsService


DEFAULT_TOOL_TIMEOUT_SECONDS = 30.0


class MissingToolInputError(ValueError):
    pass


class UnsupportedToolCallError(ValueError):
    pass


class ToolTimeoutError(TimeoutError):
    pass


@dataclass(frozen=True)
class _ToolBinding:
    tool_name: str
    request_model: type[BaseModel]
    service_method: str


@dataclass(frozen=True)
class _Invocation:
    planned_tool: PlannedToolCall
    payload: BaseModel | Mapping[str, Any]
    ordering_metadata: ToolOrderingMetadata


@dataclass(frozen=True)
class _CompletedInvocation:
    payload: dict[str, Any]
    execution_time_ms: float


_TOOL_BINDINGS = {
    PlannedToolCall.VALUATION_TOOL: _ToolBinding("valuation", ValuationToolRequest, "execute_valuation"),
    PlannedToolCall.EXPLAINABILITY_TOOL: _ToolBinding(
        "explainability",
        ExplainabilityToolRequest,
        "execute_explainability",
    ),
    PlannedToolCall.COMPARABLES_TOOL: _ToolBinding("comparable", ComparableToolRequest, "execute_comparable"),
    PlannedToolCall.FAIRNESS_TOOL: _ToolBinding("fairness", FairnessToolRequest, "execute_fairness"),
    PlannedToolCall.WHAT_IF_TOOL: _ToolBinding("what_if", WhatIfToolRequest, "execute_what_if"),
    PlannedToolCall.NEGOTIATION_TOOL: _ToolBinding(
        "negotiation",
        NegotiationToolRequest,
        "execute_negotiation",
    ),
    PlannedToolCall.INVESTMENT_TOOL: _ToolBinding("investment", InvestmentToolRequest, "execute_investment"),
    PlannedToolCall.MARKET_INSIGHT_TOOL: _ToolBinding(
        "market_insight",
        MarketInsightToolRequest,
        "execute_market_insight",
    ),
    PlannedToolCall.VALUATION_TOOL_PROPERTY_A: _ToolBinding(
        "valuation",
        ValuationToolRequest,
        "execute_valuation",
    ),
    PlannedToolCall.VALUATION_TOOL_PROPERTY_B: _ToolBinding(
        "valuation",
        ValuationToolRequest,
        "execute_valuation",
    ),
}


def _elapsed_ms(started: float) -> float:
    return round((time.perf_counter() - started) * 1000, 3)


class CopilotToolInvoker:
    """Invoke approved Tool Layer methods with an isolated session per call."""

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    @staticmethod
    def tool_name(planned_tool: PlannedToolCall) -> str:
        binding = _TOOL_BINDINGS.get(planned_tool)
        return binding.tool_name if binding is not None else str(planned_tool)

    def invoke(
        self,
        user_id: int,
        planned_tool: PlannedToolCall,
        payload: BaseModel | Mapping[str, Any],
    ) -> dict[str, Any]:
        binding = _TOOL_BINDINGS.get(planned_tool)
        if binding is None:
            raise UnsupportedToolCallError(f"Unsupported planned Tool call: {planned_tool}")
        request = (
            payload
            if isinstance(payload, binding.request_model)
            else binding.request_model.model_validate(payload)
        )
        db = self.session_factory()
        try:
            service = CopilotToolsService(db)
            response = getattr(service, binding.service_method)(user_id, request)
            return response.model_dump(mode="json")
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()


class DeterministicToolExecutor:
    def __init__(
        self,
        *,
        timeout_seconds: float = DEFAULT_TOOL_TIMEOUT_SECONDS,
        invoker: CopilotToolInvoker | None = None,
    ):
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero")
        self.timeout_seconds = float(timeout_seconds)
        self.invoker = invoker or CopilotToolInvoker()

    def execute(
        self,
        plan: ExecutionPlan,
        *,
        user_id: int,
        tool_inputs: Mapping[PlannedToolCall | str, BaseModel | Mapping[str, Any]],
    ) -> ExecutionResult:
        if not isinstance(plan, ExecutionPlan):
            raise TypeError("plan must be an ExecutionPlan")
        if user_id <= 0:
            raise ValueError("user_id must be greater than zero")

        execution_id = f"exec_{uuid.uuid4().hex}"
        started = time.perf_counter()
        if (
            plan.execution_strategy == ExecutionStrategy.CLARIFICATION_REQUIRED
            or plan.requires_clarification
        ):
            return self._result(
                execution_id=execution_id,
                plan=plan,
                started=started,
                results=(),
                failures=(),
            )
        if not plan.tools:
            raise ValueError("Executable plans must include at least one Tool")

        invocations, input_failures = self._invocations(plan, tool_inputs)
        if plan.execution_strategy == ExecutionStrategy.SEQUENTIAL:
            results, failures = self._execute_sequential(user_id, invocations)
        elif plan.execution_strategy == ExecutionStrategy.PARALLEL:
            results, failures = self._execute_parallel(user_id, invocations)
        else:
            raise ValueError(f"Unsupported execution strategy: {plan.execution_strategy}")

        return self._result(
            execution_id=execution_id,
            plan=plan,
            started=started,
            results=tuple((*results,)),
            failures=tuple((*input_failures, *failures)),
        )

    def _invocations(
        self,
        plan: ExecutionPlan,
        tool_inputs: Mapping[PlannedToolCall | str, BaseModel | Mapping[str, Any]],
    ) -> tuple[tuple[_Invocation, ...], tuple[ToolExecutionFailure, ...]]:
        invocations = []
        failures = []
        for order_index, planned_tool in enumerate(plan.tools):
            ordering_metadata = ToolOrderingMetadata(
                order_index=order_index,
                parallel_group_index=self._parallel_group_index(plan, planned_tool),
            )
            try:
                payload = self._tool_input(tool_inputs, planned_tool)
            except MissingToolInputError as exc:
                failures.append(
                    ToolExecutionFailure(
                        planned_tool=planned_tool,
                        tool_name=self.invoker.tool_name(planned_tool),
                        error_type=type(exc).__name__,
                        error_message=str(exc),
                        execution_time_ms=0.0,
                        ordering_metadata=ordering_metadata,
                    )
                )
                continue
            invocations.append(
                _Invocation(
                    planned_tool=planned_tool,
                    payload=payload,
                    ordering_metadata=ordering_metadata,
                )
            )
        return tuple(invocations), tuple(failures)

    @staticmethod
    def _tool_input(
        tool_inputs: Mapping[PlannedToolCall | str, BaseModel | Mapping[str, Any]],
        planned_tool: PlannedToolCall,
    ) -> BaseModel | Mapping[str, Any]:
        if planned_tool in tool_inputs:
            return tool_inputs[planned_tool]
        if planned_tool.value in tool_inputs:
            return tool_inputs[planned_tool.value]
        raise MissingToolInputError(f"Missing input payload for {planned_tool.value}")

    @staticmethod
    def _parallel_group_index(plan: ExecutionPlan, planned_tool: PlannedToolCall) -> int | None:
        for group_index, group in enumerate(plan.parallel_groups):
            if planned_tool in group:
                return group_index
        return None

    def _execute_sequential(
        self,
        user_id: int,
        invocations: tuple[_Invocation, ...],
    ) -> tuple[tuple[ToolExecutionResult, ...], tuple[ToolExecutionFailure, ...]]:
        results = []
        failures = []
        for invocation in invocations:
            executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="valorai-tool-executor")
            submitted = time.perf_counter()
            future = executor.submit(self._invoke, user_id, invocation)
            try:
                result, failure = self._resolve_future(
                    future,
                    invocation,
                    self.timeout_seconds,
                    submitted,
                )
            finally:
                executor.shutdown(wait=False, cancel_futures=True)
            if result is not None:
                results.append(result)
            if failure is not None:
                failures.append(failure)
        return tuple(results), tuple(failures)

    def _execute_parallel(
        self,
        user_id: int,
        invocations: tuple[_Invocation, ...],
    ) -> tuple[tuple[ToolExecutionResult, ...], tuple[ToolExecutionFailure, ...]]:
        if not invocations:
            return (), ()
        executor = ThreadPoolExecutor(
            max_workers=len(invocations),
            thread_name_prefix="valorai-tool-executor",
        )
        submitted = time.perf_counter()
        futures = [
            (invocation, executor.submit(self._invoke, user_id, invocation))
            for invocation in invocations
        ]
        results = []
        failures = []
        try:
            for invocation, future in futures:
                remaining = max(0.0, self.timeout_seconds - (time.perf_counter() - submitted))
                result, failure = self._resolve_future(
                    future,
                    invocation,
                    remaining,
                    submitted,
                )
                if result is not None:
                    results.append(result)
                if failure is not None:
                    failures.append(failure)
        finally:
            executor.shutdown(wait=False, cancel_futures=True)
        return tuple(results), tuple(failures)

    def _invoke(self, user_id: int, invocation: _Invocation) -> _CompletedInvocation:
        started = time.perf_counter()
        payload = self.invoker.invoke(user_id, invocation.planned_tool, invocation.payload)
        return _CompletedInvocation(payload=payload, execution_time_ms=_elapsed_ms(started))

    def _resolve_future(
        self,
        future: Future[_CompletedInvocation],
        invocation: _Invocation,
        timeout_seconds: float,
        submitted: float,
    ) -> tuple[ToolExecutionResult | None, ToolExecutionFailure | None]:
        try:
            completed = future.result(timeout=timeout_seconds)
        except FutureTimeoutError:
            exc = ToolTimeoutError(
                f"{invocation.planned_tool.value} exceeded the {self.timeout_seconds:g} second timeout"
            )
            return None, self._failure(invocation, exc, _elapsed_ms(submitted))
        except Exception as exc:
            return None, self._failure(invocation, exc, _elapsed_ms(submitted))
        return (
            ToolExecutionResult(
                planned_tool=invocation.planned_tool,
                tool_name=self.invoker.tool_name(invocation.planned_tool),
                payload=completed.payload,
                execution_time_ms=completed.execution_time_ms,
                ordering_metadata=invocation.ordering_metadata,
            ),
            None,
        )

    def _failure(
        self,
        invocation: _Invocation,
        exc: Exception,
        execution_time_ms: float,
    ) -> ToolExecutionFailure:
        return ToolExecutionFailure(
            planned_tool=invocation.planned_tool,
            tool_name=self.invoker.tool_name(invocation.planned_tool),
            error_type=type(exc).__name__,
            error_message=str(exc),
            execution_time_ms=execution_time_ms,
            ordering_metadata=invocation.ordering_metadata,
        )

    def _result(
        self,
        *,
        execution_id: str,
        plan: ExecutionPlan,
        started: float,
        results: tuple[ToolExecutionResult, ...],
        failures: tuple[ToolExecutionFailure, ...],
    ) -> ExecutionResult:
        if plan.execution_strategy == ExecutionStrategy.CLARIFICATION_REQUIRED or plan.requires_clarification:
            status = ExecutionStatus.CLARIFICATION_REQUIRED
        elif failures and results:
            status = ExecutionStatus.PARTIAL_SUCCESS
        elif failures:
            status = ExecutionStatus.FAILED
        else:
            status = ExecutionStatus.SUCCESS
        return ExecutionResult(
            execution_id=execution_id,
            plan_id=plan.plan_id,
            primary_intent=plan.primary_intent,
            secondary_intents=plan.secondary_intents,
            status=status,
            tool_results=results,
            failed_tools=failures,
            execution_time_ms=_elapsed_ms(started),
            partial_success=bool(failures),
            audit_metadata=ExecutionAuditMetadata(
                executed_tools=plan.tools,
                successful_tools=tuple(result.planned_tool for result in results),
                failed_tools=tuple(failure.planned_tool for failure in failures),
                execution_strategy=plan.execution_strategy,
                timeout_seconds=self.timeout_seconds,
            ),
        )


tool_executor = DeterministicToolExecutor()
