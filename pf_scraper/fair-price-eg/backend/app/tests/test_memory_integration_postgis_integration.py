from __future__ import annotations

import os
import uuid

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration

if os.environ.get("RUN_POSTGIS_INTEGRATION") != "1":
    pytest.skip("Set RUN_POSTGIS_INTEGRATION=1 with a seeded PostGIS database to run.", allow_module_level=True)

from app.broker.sessions.state import BrokerSessionStore  # noqa: E402
from app.copilot.orchestrator.composer import DeterministicResponseComposer  # noqa: E402
from app.copilot.orchestrator.executor import DeterministicToolExecutor  # noqa: E402
from app.copilot.orchestrator.intents import intent_engine  # noqa: E402
from app.copilot.orchestrator.memory import DeterministicMemoryIntegration, MemoryStatus  # noqa: E402
from app.copilot.orchestrator.planner import PlannedToolCall, tool_planner  # noqa: E402
from app.core.auth import create_access_token  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
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


def test_memory_integration_rebuilds_real_postgis_context_and_isolates_tenants():
    with TestClient(app) as client:
        headers = _headers(f"memory-postgis-{uuid.uuid4()}")
        user = client.get("/v1/copilot/users/me", headers=headers).json()
        workspace = _post(client, "/v1/copilot/workspaces", headers, {"name": "Memory Integration"})
        property_a = _property(client, headers, workspace["id"], "Property A", 220)
        property_b = _property(client, headers, workspace["id"], "Property B", 230)
        scenario = _post(
            client,
            "/v1/copilot/scenarios",
            headers,
            {"property_state_id": property_a["id"], "name": "Memory scenario", "modifications": {"parking": True}},
        )

        other_headers = _headers(f"memory-postgis-other-{uuid.uuid4()}")
        other_user = client.get("/v1/copilot/users/me", headers=other_headers).json()

        execution = DeterministicToolExecutor().execute(
            tool_planner.plan(intent_engine.classify("Compare these two properties.")),
            user_id=user["id"],
            tool_inputs={
                PlannedToolCall.VALUATION_TOOL_PROPERTY_A: {
                    "workspace_id": workspace["id"],
                    "property_id": property_a["id"],
                    "scenario_id": scenario["id"],
                },
                PlannedToolCall.VALUATION_TOOL_PROPERTY_B: {
                    "workspace_id": workspace["id"],
                    "property_id": property_b["id"],
                },
            },
        )
        composed = DeterministicResponseComposer().compose(execution)

    broker_session_id = f"memory-postgis-{uuid.uuid4().hex[:18]}"
    with SessionLocal() as db:
        BrokerSessionStore().get_or_create(
            broker_session_id,
            db=db,
            user_id=user["id"],
            workspace_id=workspace["id"],
            scenario_id=scenario["id"],
        )
        remembered = DeterministicMemoryIntegration(db).remember(
            user_id=user["id"],
            workspace_id=workspace["id"],
            scenario_id=scenario["id"],
            broker_session_id=broker_session_id,
            execution_result=execution,
            composed_response=composed,
        )

    with SessionLocal() as db:
        recovered = DeterministicMemoryIntegration(db).load_context(
            user_id=user["id"],
            workspace_id=workspace["id"],
            scenario_id=scenario["id"],
            broker_session_id=broker_session_id,
        )
        denied = DeterministicMemoryIntegration(db).load_context(
            user_id=other_user["id"],
            workspace_id=workspace["id"],
            scenario_id=scenario["id"],
        )

    assert remembered.status == MemoryStatus.SUCCESS
    assert recovered.to_dict() == remembered.to_dict()
    assert remembered.active_comparison_context["status"] == "AVAILABLE"
    assert len(remembered.citation_package["valuation_ids"]) >= 2
    assert denied.status == MemoryStatus.ACCESS_DENIED
