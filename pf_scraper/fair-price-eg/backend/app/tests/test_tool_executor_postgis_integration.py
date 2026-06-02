from __future__ import annotations

import os
import time
import uuid

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration

if os.environ.get("RUN_POSTGIS_INTEGRATION") != "1":
    pytest.skip("Set RUN_POSTGIS_INTEGRATION=1 with a seeded PostGIS database to run.", allow_module_level=True)

from app.copilot.orchestrator.executor import DeterministicToolExecutor, ExecutionStatus  # noqa: E402
from app.copilot.orchestrator.intents import intent_engine  # noqa: E402
from app.copilot.orchestrator.planner import PlannedToolCall, tool_planner  # noqa: E402
from app.core.auth import create_access_token  # noqa: E402
from app.main import app  # noqa: E402


def _headers(subject: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {create_access_token(subject)}"}


def _post(client: TestClient, uri: str, headers: dict[str, str], body: dict):
    response = client.post(uri, headers=headers, json=body)
    response.raise_for_status()
    return response.json()


def _property(
    client: TestClient,
    headers: dict[str, str],
    workspace_id: int,
    *,
    label: str,
    area: int,
):
    return _post(
        client,
        "/v1/copilot/properties",
        headers,
        {
            "workspace_id": workspace_id,
            "label": label,
            "location": "Mivida",
            "area": area,
            "bedrooms": 4,
            "bathrooms": 3,
            "amenities": {"codes": ["BA", "SE"]},
            "valuation_inputs": {
                "lat": 30.00575065612793,
                "lng": 31.533998489379883,
                "compound_name": "Mivida",
            },
        },
    )


def _state(client: TestClient):
    headers = _headers(f"tool-executor-{uuid.uuid4()}")
    user = client.get("/v1/copilot/users/me", headers=headers).json()
    workspace = _post(client, "/v1/copilot/workspaces", headers, {"name": "Tool Executor Integration"})
    property_a = _property(client, headers, workspace["id"], label="Property A", area=220)
    property_b = _property(client, headers, workspace["id"], label="Property B", area=230)

    other_headers = _headers(f"tool-executor-other-{uuid.uuid4()}")
    other_user = client.get("/v1/copilot/users/me", headers=other_headers).json()
    other_workspace = _post(client, "/v1/copilot/workspaces", other_headers, {"name": "Other Tenant"})
    other_property = _property(client, other_headers, other_workspace["id"], label="Other Property", area=240)
    return user, workspace, property_a, property_b, other_user, other_property


def test_executor_runs_real_tools_in_sequence_and_parallel_without_composing_payloads():
    with TestClient(app) as client:
        user, workspace, property_a, property_b, _, _ = _state(client)
        executor = DeterministicToolExecutor()

        valuation_plan = tool_planner.plan(intent_engine.classify("What is the fair price for this property?"))
        valuation = executor.execute(
            valuation_plan,
            user_id=user["id"],
            tool_inputs={
                PlannedToolCall.VALUATION_TOOL: {
                    "workspace_id": workspace["id"],
                    "property_id": property_a["id"],
                }
            },
        )
        comparison_plan = tool_planner.plan(intent_engine.classify("Compare these two properties."))
        comparison = executor.execute(
            comparison_plan,
            user_id=user["id"],
            tool_inputs={
                PlannedToolCall.VALUATION_TOOL_PROPERTY_A: {
                    "workspace_id": workspace["id"],
                    "property_id": property_a["id"],
                },
                PlannedToolCall.VALUATION_TOOL_PROPERTY_B: {
                    "workspace_id": workspace["id"],
                    "property_id": property_b["id"],
                },
            },
        )
        multi_plan = tool_planner.plan(
            intent_engine.classify("What is happening in Mivida and should I negotiate?")
        )
        multi = executor.execute(
            multi_plan,
            user_id=user["id"],
            tool_inputs={
                PlannedToolCall.MARKET_INSIGHT_TOOL: {"workspace_id": workspace["id"]},
                PlannedToolCall.NEGOTIATION_TOOL: {
                    "workspace_id": workspace["id"],
                    "property_id": property_a["id"],
                    "asking_price_egp": valuation.tool_results[0].payload["fair_price"],
                },
            },
        )

    assert valuation.status == ExecutionStatus.SUCCESS
    assert valuation.tool_results[0].payload["source"] == "TruthLayer"
    assert valuation.tool_results[0].payload["tool_name"] == "valuation"
    assert comparison.status == ExecutionStatus.SUCCESS
    assert [result.planned_tool for result in comparison.tool_results] == [
        PlannedToolCall.VALUATION_TOOL_PROPERTY_A,
        PlannedToolCall.VALUATION_TOOL_PROPERTY_B,
    ]
    assert [result.ordering_metadata.order_index for result in comparison.tool_results] == [0, 1]
    assert [result.ordering_metadata.parallel_group_index for result in comparison.tool_results] == [0, 0]
    assert all(result.payload["tool_name"] == "valuation" for result in comparison.tool_results)
    assert comparison.execution_time_ms < sum(result.execution_time_ms for result in comparison.tool_results)
    assert multi.status == ExecutionStatus.SUCCESS
    assert [result.payload["tool_name"] for result in multi.tool_results] == ["market_insight", "negotiation"]
    assert multi.audit_metadata.execution_strategy.value == "PARALLEL"


def test_executor_isolates_real_partial_failures_timeouts_and_tenants():
    with TestClient(app) as client:
        user, workspace, property_a, _, other_user, other_property = _state(client)
        comparison_plan = tool_planner.plan(intent_engine.classify("Compare these two properties."))
        partial = DeterministicToolExecutor().execute(
            comparison_plan,
            user_id=user["id"],
            tool_inputs={
                PlannedToolCall.VALUATION_TOOL_PROPERTY_A: {
                    "workspace_id": workspace["id"],
                    "property_id": property_a["id"],
                },
                PlannedToolCall.VALUATION_TOOL_PROPERTY_B: {
                    "workspace_id": workspace["id"],
                    "property_id": other_property["id"],
                },
            },
        )
        valuation_plan = tool_planner.plan(intent_engine.classify("What is the fair price for this property?"))
        cross_tenant = DeterministicToolExecutor().execute(
            valuation_plan,
            user_id=other_user["id"],
            tool_inputs={
                PlannedToolCall.VALUATION_TOOL: {
                    "workspace_id": workspace["id"],
                    "property_id": property_a["id"],
                }
            },
        )
        market_plan = tool_planner.plan(intent_engine.classify("What is happening in Mivida?"))
        timeout = DeterministicToolExecutor(timeout_seconds=0.000001).execute(
            market_plan,
            user_id=user["id"],
            tool_inputs={PlannedToolCall.MARKET_INSIGHT_TOOL: {"workspace_id": workspace["id"]}},
        )
        clarification_plan = tool_planner.plan(intent_engine.classify("Tell me more"))
        clarification = DeterministicToolExecutor().execute(
            clarification_plan,
            user_id=user["id"],
            tool_inputs={},
        )
        time.sleep(0.1)

    assert partial.status == ExecutionStatus.PARTIAL_SUCCESS
    assert partial.partial_success is True
    assert len(partial.tool_results) == 1
    assert partial.failed_tools[0].planned_tool == PlannedToolCall.VALUATION_TOOL_PROPERTY_B
    assert partial.failed_tools[0].error_type == "ToolResourceNotFound"
    assert cross_tenant.status == ExecutionStatus.FAILED
    assert cross_tenant.failed_tools[0].error_type == "ToolResourceNotFound"
    assert timeout.status == ExecutionStatus.FAILED
    assert timeout.partial_success is True
    assert timeout.failed_tools[0].error_type == "ToolTimeoutError"
    assert clarification.status == ExecutionStatus.CLARIFICATION_REQUIRED
    assert clarification.tool_results == ()
