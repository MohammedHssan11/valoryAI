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
    subject = f"negotiation-integration-{uuid.uuid4()}"
    headers = _headers(subject)
    workspace = _post(client, "/v1/copilot/workspaces", headers, {"name": "Negotiation Integration"})
    prop = _post(
        client,
        "/v1/copilot/properties",
        headers,
        {
            "workspace_id": workspace["id"],
            "label": "Mivida Negotiation Property",
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
            "name": "Expanded Mivida Negotiation Scenario",
            "modifications": {"size_sqm": 230},
        },
    )
    return headers, workspace, prop, scenario


def _negotiation(
    client: TestClient,
    headers: dict[str, str],
    workspace_id: int,
    property_id: int,
    asking_price_egp: int,
    *,
    scenario_id: int | None = None,
    what_if_modifications: dict | None = None,
):
    body = {
        "workspace_id": workspace_id,
        "property_id": property_id,
        "asking_price_egp": asking_price_egp,
    }
    if scenario_id is not None:
        body["scenario_id"] = scenario_id
    if what_if_modifications is not None:
        body["what_if_modifications"] = what_if_modifications
    return _post(client, "/v1/copilot/tools/negotiation", headers, body)


def _assert_grounded_package(result: dict):
    assert result["source"] == "TruthLayer"
    assert result["evidence_summary"]["source"] == "TruthLayer"
    assert result["comparable_summary"]["source"] == "TruthLayer"
    assert result["recommended_offer_band"]["source"] == "TruthLayer-derived"
    assert result["valuation_id"] == result["evidence_summary"]["valuation_id"]
    assert result["valuation_id"] == result["comparable_summary"]["valuation_id"]
    assert result["price_gap"] == result["asking_price"] - result["fair_price"]
    assert result["price_gap_percentage"] == round((result["price_gap"] / result["fair_price"]) * 100, 4)
    assert all(point["evidence"] for point in result["broker_talking_points"])
    assert result["negotiation_position_evidence"]
    assert result["risk_notes"]
    assert all(note["evidence"] for note in result["risk_notes"])
    allowed_prices = {result["fair_price"], *result["comparable_summary"]["observed_prices"]}
    band = result["recommended_offer_band"]
    assert band["low"] is None or band["low"] in allowed_prices
    assert band["high"] is None or band["high"] in allowed_prices


def test_negotiation_tool_handles_fairness_positions_with_traceable_real_evidence():
    with TestClient(app) as client:
        headers, workspace, prop, _ = _create_workspace_state(client)
        valuation = _post(
            client,
            "/v1/copilot/tools/valuation",
            headers,
            {"workspace_id": workspace["id"], "property_id": prop["id"]},
        )
        askings = {
            "Below Fair Value": max(1, valuation["price_range"]["low"] - 1),
            "Within Fair Value": valuation["fair_price"],
            "Above Fair Value": valuation["price_range"]["high"] + 1,
        }
        results = {
            status: _negotiation(
                client,
                headers,
                workspace["id"],
                prop["id"],
                asking_price,
            )
            for status, asking_price in askings.items()
        }
        events = client.get(f"/v1/copilot/workspaces/{workspace['id']}/tool-events", headers=headers).json()

    expected_positions = {
        "Below Fair Value": "Strong Buy Opportunity",
        "Within Fair Value": "Fair Market Position",
        "Above Fair Value": "Overpriced",
    }
    for status, result in results.items():
        _assert_grounded_package(result)
        assert result["fairness_status"] == status
        assert result["negotiation_position"] == expected_positions[status]
        assert result["asking_price"] == askings[status]
        assert result["comparable_summary"]["comparable_count"] > 0
        assert result["comparable_summary"]["comparable_count"] == len(result["comparable_summary"]["comparable_ids"])
        assert result["comparable_summary"]["comparable_count"] == len(result["comparable_summary"]["observed_prices"])
        valuation_event = next(
            event
            for event in events
            if event["tool_name"] == "valuation"
            and event["payload"]["response"]["valuation_id"] == result["valuation_id"]
        )
        audit_event = next(
            event
            for event in events
            if event["tool_name"] == "negotiation"
            and event["payload"]["response"]["valuation_id"] == result["valuation_id"]
        )
        assert valuation_event["payload"]["request"]["router_request"]["target_price_egp"] == askings[status]
        assert audit_event["payload"]["request"]["asking_price_egp"] == askings[status]
        assert audit_event["payload"]["response"]["fairness_status"] == status
        assert audit_event["payload"]["response"]["negotiation_position"] == expected_positions[status]

    assert results["Below Fair Value"]["recommended_offer_band"]["low"] is None
    assert results["Below Fair Value"]["recommended_offer_band"]["high"] is None
    assert results["Within Fair Value"]["recommended_offer_band"]["low"] == valuation["fair_price"]
    assert results["Within Fair Value"]["recommended_offer_band"]["high"] == valuation["fair_price"]
    above = results["Above Fair Value"]
    comparable_support = [
        price
        for price in above["comparable_summary"]["observed_prices"]
        if price <= above["fair_price"]
    ]
    expected_low = max(comparable_support) if comparable_support else above["fair_price"]
    assert above["recommended_offer_band"]["low"] == expected_low
    assert above["recommended_offer_band"]["high"] == above["fair_price"]
    assert sum(event["tool_name"] == "negotiation" for event in events) == 3


def test_negotiation_tool_applies_scenario_state_preserves_what_if_and_rejects_cross_tenant_access():
    with TestClient(app) as client:
        headers, workspace, prop, scenario = _create_workspace_state(client)
        scenario_valuation = _post(
            client,
            "/v1/copilot/tools/valuation",
            headers,
            {
                "workspace_id": workspace["id"],
                "property_id": prop["id"],
                "scenario_id": scenario["id"],
            },
        )
        result = _negotiation(
            client,
            headers,
            workspace["id"],
            prop["id"],
            scenario_valuation["price_range"]["high"] + 1,
            scenario_id=scenario["id"],
            what_if_modifications={"bathrooms": 4},
        )
        events = client.get(f"/v1/copilot/workspaces/{workspace['id']}/tool-events", headers=headers).json()
        other_headers = _headers(f"negotiation-other-{uuid.uuid4()}")
        cross_tenant = client.post(
            "/v1/copilot/tools/negotiation",
            headers=other_headers,
            json={
                "workspace_id": workspace["id"],
                "property_id": prop["id"],
                "scenario_id": scenario["id"],
                "asking_price_egp": result["asking_price"],
            },
        )

    _assert_grounded_package(result)
    valuation_event = next(
        event
        for event in events
        if event["tool_name"] == "valuation"
        and event["payload"]["response"]["valuation_id"] == result["valuation_id"]
    )
    audit_event = next(event for event in events if event["tool_name"] == "negotiation")
    what_if_event = next(event for event in events if event["tool_name"] == "what_if")
    assert valuation_event["payload"]["request"]["router_request"]["size_sqm"] == 230
    assert audit_event["scenario_state_id"] == scenario["id"]
    assert audit_event["payload"]["request"]["scenario_id"] == scenario["id"]
    assert audit_event["payload"]["request"]["what_if_modifications"] == {"bathrooms": 4}
    assert result["fairness_status"] == "Above Fair Value"
    assert result["negotiation_position"] == "Overpriced"
    assert result["what_if_analysis"]["source"] == "TruthLayer"
    assert result["what_if_analysis"]["scenario_valuation_id"] != result["what_if_analysis"]["base_valuation_id"]
    assert what_if_event["payload"]["request"]["modifications"] == {"bathrooms": 4}
    assert cross_tenant.status_code == 404
