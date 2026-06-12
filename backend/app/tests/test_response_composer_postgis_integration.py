from __future__ import annotations

import os
import uuid

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration

if os.environ.get("RUN_POSTGIS_INTEGRATION") != "1":
    pytest.skip("Set RUN_POSTGIS_INTEGRATION=1 with a seeded PostGIS database to run.", allow_module_level=True)

from app.copilot.orchestrator.composer import CompositionStatus, DeterministicResponseComposer  # noqa: E402
from app.copilot.orchestrator.executor import DeterministicToolExecutor  # noqa: E402
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


def _property(client: TestClient, headers: dict[str, str], workspace_id: int, label: str, area: int):
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
    headers = _headers(f"response-composer-{uuid.uuid4()}")
    user = client.get("/v1/copilot/users/me", headers=headers).json()
    workspace = _post(client, "/v1/copilot/workspaces", headers, {"name": "Composer Integration"})
    empty_workspace = _post(client, "/v1/copilot/workspaces", headers, {"name": "Composer Empty"})
    property_a = _property(client, headers, workspace["id"], "Property A", 220)
    property_b = _property(client, headers, workspace["id"], "Property B", 230)

    other_headers = _headers(f"response-composer-other-{uuid.uuid4()}")
    client.get("/v1/copilot/users/me", headers=other_headers).json()
    other_workspace = _post(client, "/v1/copilot/workspaces", other_headers, {"name": "Other Tenant"})
    other_property = _property(client, other_headers, other_workspace["id"], "Other Property", 240)
    return user, workspace, empty_workspace, property_a, property_b, other_property


def test_composer_runs_real_comparison_multi_intent_and_sparse_flows():
    with TestClient(app) as client:
        user, workspace, empty_workspace, property_a, property_b, _ = _state(client)
        executor = DeterministicToolExecutor()
        composer = DeterministicResponseComposer()

        valuation = executor.execute(
            tool_planner.plan(intent_engine.classify("What is the fair price for this property?")),
            user_id=user["id"],
            tool_inputs={
                PlannedToolCall.VALUATION_TOOL: {
                    "workspace_id": workspace["id"],
                    "property_id": property_a["id"],
                }
            },
        )
        comparison_execution = executor.execute(
            tool_planner.plan(intent_engine.classify("Compare these two properties.")),
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
        comparables_execution = executor.execute(
            tool_planner.plan(intent_engine.classify("Show me nearby comparable properties.")),
            user_id=user["id"],
            tool_inputs={
                PlannedToolCall.COMPARABLES_TOOL: {
                    "workspace_id": workspace["id"],
                    "property_id": property_a["id"],
                }
            },
        )
        multi_execution = executor.execute(
            tool_planner.plan(intent_engine.classify("What is happening in Mivida and should I negotiate?")),
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
        investment_execution = executor.execute(
            tool_planner.plan(intent_engine.classify("Is this a good investment?")),
            user_id=user["id"],
            tool_inputs={
                PlannedToolCall.INVESTMENT_TOOL: {
                    "workspace_id": workspace["id"],
                    "property_id": property_a["id"],
                    "asking_price_egp": valuation.tool_results[0].payload["fair_price"],
                }
            },
        )
        sparse_execution = executor.execute(
            tool_planner.plan(intent_engine.classify("What is happening in Mivida?")),
            user_id=user["id"],
            tool_inputs={PlannedToolCall.MARKET_INSIGHT_TOOL: {"workspace_id": empty_workspace["id"]}},
        )

    comparison = composer.compose(comparison_execution)
    comparables = composer.compose(comparables_execution)
    multi = composer.compose(multi_execution)
    investment = composer.compose(investment_execution)
    sparse = composer.compose(sparse_execution)

    assert comparison.status == CompositionStatus.SUCCESS
    assert comparison.evidence_summary["property_comparison"]["price_delta"] == (
        comparison.evidence_summary["property_comparison"]["property_b"]["fair_price"]
        - comparison.evidence_summary["property_comparison"]["property_a"]["fair_price"]
    )
    assert len(comparables.compressed_context["evidence"]["tool_summaries"][0]["summary"]["comparables"]["top_comparables"]) <= 3
    assert multi.primary_intent.value == "MARKET_INSIGHT"
    assert [intent.value for intent in multi.secondary_intents] == ["NEGOTIATION"]
    assert investment.status == CompositionStatus.SUCCESS
    assert sparse.status == CompositionStatus.SPARSE_EVIDENCE
    assert DeterministicResponseComposer().compose(comparison_execution).to_dict() == comparison.to_dict()


def test_composer_normalizes_real_partial_and_full_comparison_failures():
    with TestClient(app) as client:
        user, workspace, _, property_a, _, other_property = _state(client)
        plan = tool_planner.plan(intent_engine.classify("Compare these two properties."))
        executor = DeterministicToolExecutor()
        partial_execution = executor.execute(
            plan,
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
        failed_execution = executor.execute(
            plan,
            user_id=user["id"],
            tool_inputs={
                PlannedToolCall.VALUATION_TOOL_PROPERTY_A: {
                    "workspace_id": workspace["id"],
                    "property_id": other_property["id"],
                },
                PlannedToolCall.VALUATION_TOOL_PROPERTY_B: {
                    "workspace_id": workspace["id"],
                    "property_id": other_property["id"],
                },
            },
        )

    partial = DeterministicResponseComposer().compose(partial_execution)
    failed = DeterministicResponseComposer().compose(failed_execution)

    assert partial.status == CompositionStatus.PARTIAL_SUCCESS
    assert failed.status == CompositionStatus.FAILED
    assert partial.evidence_summary["property_comparison"]["status"] == "UNAVAILABLE"
    assert failed.evidence_summary["property_comparison"]["status"] == "UNAVAILABLE"
