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
    subject = f"investment-integration-{uuid.uuid4()}"
    headers = _headers(subject)
    workspace = _post(client, "/v1/copilot/workspaces", headers, {"name": "Investment Integration"})
    prop = _post(
        client,
        "/v1/copilot/properties",
        headers,
        {
            "workspace_id": workspace["id"],
            "label": "Mivida Investment Property",
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
    sparse_prop = _post(
        client,
        "/v1/copilot/properties",
        headers,
        {
            "workspace_id": workspace["id"],
            "label": "Sparse Central Cairo Investment Property",
            "location": "Central Cairo",
            "area": 150,
            "bedrooms": 3,
            "bathrooms": 2,
            "amenities": {"codes": ["BA"]},
            "valuation_inputs": {
                "lat": 30.0444,
                "lng": 31.2357,
            },
        },
    )
    scenario = _post(
        client,
        "/v1/copilot/scenarios",
        headers,
        {
            "property_state_id": prop["id"],
            "name": "Expanded Mivida Investment Scenario",
            "modifications": {"size_sqm": 230},
        },
    )
    return headers, workspace, prop, sparse_prop, scenario


def _investment(
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
    return _post(client, "/v1/copilot/tools/investment", headers, body)


def _assert_grounded_package(result: dict):
    assert result["source"] == "TruthLayer"
    assert result["evidence_summary"]["source"] == "TruthLayer"
    assert result["comparable_summary"]["source"] == "TruthLayer"
    assert result["negotiation_summary"]["source"] == "TruthLayer"
    assert result["valuation_id"] == result["evidence_summary"]["valuation_id"]
    assert result["valuation_id"] == result["comparable_summary"]["valuation_id"]
    assert result["price_gap"] == result["asking_price"] - result["fair_price"]
    assert result["price_gap_percentage"] == round((result["price_gap"] / result["fair_price"]) * 100, 4)
    assert result["investment_position_evidence"]
    assert all(item["evidence"] for item in result["strengths"])
    assert result["risks"]
    assert all(item["evidence"] for item in result["risks"])
    assert "roi" not in {key.lower() for key in result}
    assert "irr" not in {key.lower() for key in result}
    assert "cagr" not in {key.lower() for key in result}


def test_investment_tool_handles_all_positions_with_traceable_real_evidence():
    with TestClient(app) as client:
        headers, workspace, prop, sparse_prop, _ = _create_workspace_state(client)
        valuation = _post(
            client,
            "/v1/copilot/tools/valuation",
            headers,
            {"workspace_id": workspace["id"], "property_id": prop["id"]},
        )
        sparse_valuation = _post(
            client,
            "/v1/copilot/tools/valuation",
            headers,
            {"workspace_id": workspace["id"], "property_id": sparse_prop["id"]},
        )
        askings = {
            "Strong Opportunity": max(1, valuation["price_range"]["low"] - 1),
            "Fairly Priced": valuation["fair_price"],
            "Caution": valuation["fair_price"] + 1,
            "High Risk": valuation["price_range"]["high"] + 1,
        }
        results = {
            position: _investment(
                client,
                headers,
                workspace["id"],
                prop["id"],
                asking_price,
            )
            for position, asking_price in askings.items()
        }
        moderate_asking = max(1, sparse_valuation["price_range"]["low"] - 1)
        results["Moderate Opportunity"] = _investment(
            client,
            headers,
            workspace["id"],
            sparse_prop["id"],
            moderate_asking,
        )
        events = client.get(f"/v1/copilot/workspaces/{workspace['id']}/tool-events", headers=headers).json()

    assert {result["investment_position"] for result in results.values()} == set(results)
    for position, result in results.items():
        _assert_grounded_package(result)
        assert result["investment_position"] == position
        assert result["what_if_summary"]["status"] == "Insufficient Evidence"
        assert result["what_if_summary"]["source"] == "Insufficient Evidence"
        audit_event = next(
            event
            for event in events
            if event["tool_name"] == "investment"
            and event["payload"]["response"]["valuation_id"] == result["valuation_id"]
        )
        negotiation_event = next(
            event
            for event in events
            if event["tool_name"] == "negotiation"
            and event["payload"]["response"]["valuation_id"] == result["valuation_id"]
        )
        assert audit_event["payload"]["response"]["investment_position"] == position
        assert negotiation_event["payload"]["response"]["valuation_id"] == result["valuation_id"]

    assert results["Strong Opportunity"]["fairness_status"] == "Below Fair Value"
    assert results["Strong Opportunity"]["confidence_level"] == "High"
    assert results["Strong Opportunity"]["comparable_summary"]["comparable_count"] > 0
    assert results["Moderate Opportunity"]["fairness_status"] == "Below Fair Value"
    assert results["Moderate Opportunity"]["confidence_level"] == "Low"
    assert results["Moderate Opportunity"]["comparable_summary"]["comparable_count"] == 0
    assert results["Fairly Priced"]["fairness_status"] == "Within Fair Value"
    assert results["Caution"]["fairness_status"] == "Within Fair Value"
    assert results["High Risk"]["fairness_status"] == "Above Fair Value"
    assert sum(event["tool_name"] == "investment" for event in events) == 5


def test_investment_tool_applies_scenario_state_integrates_what_if_and_rejects_cross_tenant_access():
    with TestClient(app) as client:
        headers, workspace, prop, _, scenario = _create_workspace_state(client)
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
        result = _investment(
            client,
            headers,
            workspace["id"],
            prop["id"],
            scenario_valuation["price_range"]["high"] + 1,
            scenario_id=scenario["id"],
            what_if_modifications={"bathrooms": 4},
        )
        events = client.get(f"/v1/copilot/workspaces/{workspace['id']}/tool-events", headers=headers).json()
        other_headers = _headers(f"investment-other-{uuid.uuid4()}")
        cross_tenant = client.post(
            "/v1/copilot/tools/investment",
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
    audit_event = next(event for event in events if event["tool_name"] == "investment")
    negotiation_event = next(event for event in events if event["tool_name"] == "negotiation")
    what_if_event = next(event for event in events if event["tool_name"] == "what_if")
    assert valuation_event["payload"]["request"]["router_request"]["size_sqm"] == 230
    assert audit_event["scenario_state_id"] == scenario["id"]
    assert audit_event["payload"]["request"]["scenario_id"] == scenario["id"]
    assert audit_event["payload"]["request"]["what_if_modifications"] == {"bathrooms": 4}
    assert negotiation_event["scenario_state_id"] == scenario["id"]
    assert result["fairness_status"] == "Above Fair Value"
    assert result["investment_position"] == "High Risk"
    assert result["what_if_summary"]["status"] == "Available"
    assert result["what_if_summary"]["source"] == "TruthLayer"
    assert result["what_if_summary"]["analysis"]["scenario_valuation_id"] != result["what_if_summary"]["analysis"]["base_valuation_id"]
    assert what_if_event["payload"]["request"]["modifications"] == {"bathrooms": 4}
    assert cross_tenant.status_code == 404
