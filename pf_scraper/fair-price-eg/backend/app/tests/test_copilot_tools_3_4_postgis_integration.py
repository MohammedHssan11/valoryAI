from __future__ import annotations

import os
import uuid

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration

if os.environ.get("RUN_POSTGIS_INTEGRATION") != "1":
    pytest.skip("Set RUN_POSTGIS_INTEGRATION=1 with a seeded PostGIS database to run.", allow_module_level=True)

from app.core.auth import create_access_token  # noqa: E402
from app.main import app  # noqa: E402


def _headers(subject: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {create_access_token(subject)}"}


def _post(client: TestClient, uri: str, headers: dict[str, str], body: dict):
    response = client.post(uri, headers=headers, json=body)
    response.raise_for_status()
    return response.json()


def _create_workspace_state(client: TestClient):
    subject = f"tools-3-4-integration-{uuid.uuid4()}"
    headers = _headers(subject)
    workspace = _post(client, "/v1/copilot/workspaces", headers, {"name": "Tools 3 + 4 Integration"})
    prop = _post(
        client,
        "/v1/copilot/properties",
        headers,
        {
            "workspace_id": workspace["id"],
            "label": "Mivida Integration Property",
            "location": "Mivida",
            "area": 220,
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
    scenario = _post(
        client,
        "/v1/copilot/scenarios",
        headers,
        {
            "property_state_id": prop["id"],
            "name": "Expanded Mivida Property",
            "modifications": {"size_sqm": 230},
        },
    )
    return headers, workspace, prop, scenario


def test_comparable_tool_retrieves_real_snapshot_and_scenario_evidence():
    with TestClient(app) as client:
        headers, workspace, prop, scenario = _create_workspace_state(client)
        base = _post(
            client,
            "/v1/copilot/tools/comparable",
            headers,
            {"workspace_id": workspace["id"], "property_id": prop["id"]},
        )
        replay = _post(
            client,
            "/v1/copilot/tools/comparable",
            headers,
            {
                "workspace_id": workspace["id"],
                "property_id": prop["id"],
                "valuation_id": base["valuation_id"],
            },
        )
        scenario_result = _post(
            client,
            "/v1/copilot/tools/comparable",
            headers,
            {
                "workspace_id": workspace["id"],
                "property_id": prop["id"],
                "scenario_id": scenario["id"],
            },
        )
        events = client.get(f"/v1/copilot/workspaces/{workspace['id']}/tool-events", headers=headers).json()

    assert base["source"] == "TruthLayer"
    assert base["comparable_count"] > 0
    assert replay["valuation_id"] == base["valuation_id"]
    assert replay["comparables"] == base["comparables"]
    assert scenario_result["comparable_count"] > 0
    assert all(comp["source"] == "TruthLayer" for comp in base["comparables"])
    assert all(comp["comparable_id"] for comp in base["comparables"])
    assert all(comp["similarity_reason"] for comp in base["comparables"])
    assert all("listing_date" not in comp for comp in base["comparables"])
    scenario_valuation = next(
        event
        for event in events
        if event["tool_name"] == "valuation"
        and event["payload"]["response"]["valuation_id"] == scenario_result["valuation_id"]
    )
    assert scenario_valuation["payload"]["request"]["router_request"]["size_sqm"] == 230


def test_fairness_tool_uses_truth_layer_statuses_and_enforces_tenant_scope():
    with TestClient(app) as client:
        headers, workspace, prop, scenario = _create_workspace_state(client)
        valuation = _post(
            client,
            "/v1/copilot/tools/valuation",
            headers,
            {"workspace_id": workspace["id"], "property_id": prop["id"]},
        )
        prices = {
            "Below Fair Value": max(1, valuation["price_range"]["low"] - 1),
            "Within Fair Value": valuation["fair_price"],
            "Above Fair Value": valuation["price_range"]["high"] + 1,
        }
        results = {
            expected: _post(
                client,
                "/v1/copilot/tools/fairness",
                headers,
                {
                    "workspace_id": workspace["id"],
                    "property_id": prop["id"],
                    "target_price_egp": target,
                },
            )
            for expected, target in prices.items()
        }
        scenario_result = _post(
            client,
            "/v1/copilot/tools/fairness",
            headers,
            {
                "workspace_id": workspace["id"],
                "property_id": prop["id"],
                "scenario_id": scenario["id"],
                "target_price_egp": valuation["fair_price"],
            },
        )
        events = client.get(f"/v1/copilot/workspaces/{workspace['id']}/tool-events", headers=headers).json()
        other_headers = _headers(f"tools-3-4-other-{uuid.uuid4()}")
        comparable_cross_tenant = client.post(
            "/v1/copilot/tools/comparable",
            headers=other_headers,
            json={"workspace_id": workspace["id"], "property_id": prop["id"]},
        )
        fairness_cross_tenant = client.post(
            "/v1/copilot/tools/fairness",
            headers=other_headers,
            json={
                "workspace_id": workspace["id"],
                "property_id": prop["id"],
                "target_price_egp": valuation["fair_price"],
            },
        )

    assert {result["fairness_status"] for result in results.values()} == set(prices)
    assert all(result["source"] == "TruthLayer" for result in results.values())
    assert all(result["target_price"] == prices[expected] for expected, result in results.items())
    assert scenario_result["source"] == "TruthLayer"
    scenario_valuation = next(
        event
        for event in events
        if event["tool_name"] == "valuation"
        and event["payload"]["response"]["valuation_id"] == scenario_result["valuation_id"]
    )
    assert scenario_valuation["payload"]["request"]["router_request"]["size_sqm"] == 230
    assert scenario_valuation["payload"]["request"]["router_request"]["target_price_egp"] == valuation["fair_price"]
    assert sum(event["tool_name"] == "fairness" for event in events) == 4
    assert comparable_cross_tenant.status_code == 404
    assert fairness_cross_tenant.status_code == 404
