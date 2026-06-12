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
    subject = f"what-if-integration-{uuid.uuid4()}"
    headers = _headers(subject)
    workspace = _post(client, "/v1/copilot/workspaces", headers, {"name": "What-if Integration"})
    prop = _post(
        client,
        "/v1/copilot/properties",
        headers,
        {
            "workspace_id": workspace["id"],
            "label": "Mivida What-if Property",
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
            "name": "Existing Expanded Mivida Scenario",
            "modifications": {"size_sqm": 225},
        },
    )
    return headers, workspace, prop, scenario


def _valuation_event(events: list[dict], valuation_id: str) -> dict:
    return next(
        event
        for event in events
        if event["tool_name"] == "valuation" and event["payload"]["response"]["valuation_id"] == valuation_id
    )


def test_what_if_tool_re_evaluates_live_truth_layer_without_mutating_base_property():
    with TestClient(app) as client:
        headers, workspace, prop, _ = _create_workspace_state(client)
        result = _post(
            client,
            "/v1/copilot/tools/what-if",
            headers,
            {
                "workspace_id": workspace["id"],
                "property_id": prop["id"],
                "modifications": {"size_sqm": 230},
            },
        )
        bedroom_amenity_result = _post(
            client,
            "/v1/copilot/tools/what-if",
            headers,
            {
                "workspace_id": workspace["id"],
                "property_id": prop["id"],
                "modifications": {"bedrooms": 3, "parking": True},
            },
        )
        recovered_property = client.get(f"/v1/copilot/properties/{prop['id']}", headers=headers).json()
        events = client.get(f"/v1/copilot/workspaces/{workspace['id']}/tool-events", headers=headers).json()
        other_headers = _headers(f"what-if-other-{uuid.uuid4()}")
        cross_tenant = client.post(
            "/v1/copilot/tools/what-if",
            headers=other_headers,
            json={
                "workspace_id": workspace["id"],
                "property_id": prop["id"],
                "modifications": {"size_sqm": 230},
            },
        )

    sandbox_event = _valuation_event(events, result["scenario_valuation_id"])
    fairness_event = _valuation_event(events, result["fairness_valuation_id"])
    bedroom_amenity_event = _valuation_event(events, bedroom_amenity_result["scenario_valuation_id"])
    audit_event = next(event for event in events if event["tool_name"] == "what_if")
    assert result["source"] == "TruthLayer"
    assert result["scenario_valuation"] - result["base_valuation"] == result["delta_value"]
    assert result["comparables"]["source"] == "TruthLayer"
    assert result["comparables"]["valuation_id"] == result["scenario_valuation_id"]
    assert result["comparables"]["comparable_count"] > 0
    assert result["explainability"]["source"] == "TruthLayer"
    assert result["explainability"]["valuation_id"] == result["scenario_valuation_id"]
    assert result["fairness_valuation_id"] not in {
        result["base_valuation_id"],
        result["scenario_valuation_id"],
    }
    assert sandbox_event["payload"]["request"]["router_request"]["size_sqm"] == 230
    assert bedroom_amenity_event["payload"]["request"]["router_request"]["bedrooms"] == 3
    assert "CP" in bedroom_amenity_event["payload"]["request"]["router_request"]["amenities"]
    assert fairness_event["payload"]["request"]["router_request"]["target_price_egp"] == result["base_valuation"]
    assert recovered_property["area"] == "220.00"
    assert recovered_property["bedrooms"] == 4
    assert recovered_property["amenities"] == {"codes": ["BA", "SE"]}
    assert {item["feature"] for item in result["feature_changes"]["modified"]} == {"Size"}
    assert {item["feature"] for item in bedroom_amenity_result["feature_changes"]["added"]} == {"Parking"}
    assert {item["feature"] for item in bedroom_amenity_result["feature_changes"]["modified"]} == {"Bedrooms"}
    assert audit_event["payload"]["request"]["modifications"] == {"size_sqm": 230}
    assert audit_event["payload"]["response"]["delta_value"] == result["delta_value"]
    assert cross_tenant.status_code == 404


def test_what_if_tool_applies_overlay_on_existing_scenario_and_refreshes_evidence():
    with TestClient(app) as client:
        headers, workspace, prop, scenario = _create_workspace_state(client)
        result = _post(
            client,
            "/v1/copilot/tools/what-if",
            headers,
            {
                "workspace_id": workspace["id"],
                "property_id": prop["id"],
                "scenario_id": scenario["id"],
                "modifications": {"bathrooms": 4, "gym": True},
            },
        )
        recovered_scenario = client.get(f"/v1/copilot/scenarios/{scenario['id']}", headers=headers).json()
        events = client.get(f"/v1/copilot/workspaces/{workspace['id']}/tool-events", headers=headers).json()

    base_event = _valuation_event(events, result["base_valuation_id"])
    sandbox_event = _valuation_event(events, result["scenario_valuation_id"])
    fairness_event = _valuation_event(events, result["fairness_valuation_id"])
    assert base_event["payload"]["request"]["router_request"]["size_sqm"] == 225
    assert sandbox_event["payload"]["request"]["router_request"]["size_sqm"] == 225
    assert sandbox_event["payload"]["request"]["router_request"]["bathrooms"] == 4
    assert "SY" in sandbox_event["payload"]["request"]["router_request"]["amenities"]
    assert fairness_event["payload"]["request"]["router_request"]["bathrooms"] == 4
    assert "SY" in fairness_event["payload"]["request"]["router_request"]["amenities"]
    assert result["comparables"]["valuation_id"] == result["scenario_valuation_id"]
    assert result["fairness_valuation_id"] != result["scenario_valuation_id"]
    assert recovered_scenario["modifications"] == {"size_sqm": 225}
    assert {item["feature"] for item in result["feature_changes"]["added"]} == {"Gym"}
    assert {item["feature"] for item in result["feature_changes"]["modified"]} == {"Bathrooms"}
