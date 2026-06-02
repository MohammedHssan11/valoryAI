from __future__ import annotations

import os
import uuid

import h3
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


def _property(
    client: TestClient,
    headers: dict[str, str],
    workspace_id: int,
    *,
    label: str,
    location: str,
    property_type: str,
    lat: float,
    lng: float,
    compound_name: str | None = None,
):
    valuation_inputs = {"lat": lat, "lng": lng}
    if compound_name is not None:
        valuation_inputs["compound_name"] = compound_name
    return _post(
        client,
        "/v1/copilot/properties",
        headers,
        {
            "workspace_id": workspace_id,
            "label": label,
            "location": location,
            "area": 220 if property_type == "Villa" else 150,
            "bedrooms": 4 if property_type == "Villa" else 3,
            "bathrooms": 3 if property_type == "Villa" else 2,
            "property_type": property_type,
            "amenities": {"codes": ["BA", "SE"]},
            "valuation_inputs": valuation_inputs,
        },
    )


def _market(client: TestClient, headers: dict[str, str], body: dict):
    return _post(client, "/v1/copilot/tools/market-insight", headers, body)


def test_market_insight_describes_real_persisted_truth_layer_history_and_enforces_tenant_scope():
    with TestClient(app) as client:
        headers = _headers(f"market-insight-{uuid.uuid4()}")
        workspace = _post(client, "/v1/copilot/workspaces", headers, {"name": "Market Insight Integration"})
        mivida_apartment = _property(
            client,
            headers,
            workspace["id"],
            label="Mivida Apartment",
            location="Mivida",
            property_type="Apartment",
            lat=30.00575065612793,
            lng=31.533998489379883,
            compound_name="Mivida",
        )
        mivida_villa = _property(
            client,
            headers,
            workspace["id"],
            label="Mivida Villa",
            location="Mivida",
            property_type="Villa",
            lat=30.00575065612793,
            lng=31.533998489379883,
            compound_name="Mivida",
        )
        cairo_apartment = _property(
            client,
            headers,
            workspace["id"],
            label="Central Cairo Apartment",
            location="Central Cairo",
            property_type="Apartment",
            lat=30.0444,
            lng=31.2357,
        )
        for prop in (mivida_apartment, mivida_villa, cairo_apartment):
            _post(
                client,
                "/v1/copilot/tools/valuation",
                headers,
                {"workspace_id": workspace["id"], "property_id": prop["id"]},
            )

        h3_res9 = h3.latlng_to_cell(30.00575065612793, 31.533998489379883, 9)
        overall = _market(client, headers, {"workspace_id": workspace["id"]})
        compound = _market(client, headers, {"workspace_id": workspace["id"], "compound_name": "Mivida"})
        area = _market(client, headers, {"workspace_id": workspace["id"], "h3_res9": h3_res9})
        property_type = _market(client, headers, {"workspace_id": workspace["id"], "property_type": "Villa"})
        history = _market(client, headers, {"workspace_id": workspace["id"], "time_window": "30d"})
        events = client.get(f"/v1/copilot/workspaces/{workspace['id']}/tool-events", headers=headers).json()

        other_headers = _headers(f"market-insight-other-{uuid.uuid4()}")
        cross_tenant = client.post(
            "/v1/copilot/tools/market-insight",
            headers=other_headers,
            json={"workspace_id": workspace["id"]},
        )

    assert overall["source"] == "TruthLayer"
    assert overall["tool_name"] == "market_insight"
    assert overall["valuation_volume"] == 3
    assert overall["fair_value_distribution"]["valuation_count"] == 3
    assert overall["confidence_distribution"]["valuation_count"] == 3
    assert overall["comparable_density"]["valuation_count"] == 3
    assert overall["active_compounds"][0]["name"] == "Mivida"
    assert overall["active_compounds"][0]["valuation_count"] == 2
    assert {item["name"] for item in overall["active_areas"]} == {"Mivida", "Central Cairo"}
    assert overall["evidence_summary"]["source_record_counts"]["prediction_logs"] == 3
    assert overall["evidence_summary"]["source_record_counts"]["shadow_logs"] == 3
    assert {"valuation_snapshots", "prediction_logs", "shadow_logs"} <= set(overall["data_sources_used"])
    assert all(statement["evidence"] for statement in overall["evidence_summary"]["statements"])
    assert "forecast" not in overall["market_summary"].lower()
    assert "future" not in overall["market_summary"].lower()

    assert compound["valuation_volume"] == 2
    assert compound["active_compounds"][0]["name"] == "Mivida"
    assert area["valuation_volume"] == 2
    assert property_type["valuation_volume"] == 1
    assert property_type["evidence_summary"]["filters_used"]["property_type"] == "Villa"
    assert history["valuation_volume"] == 3
    assert history["evidence_summary"]["filters_used"]["time_window"] == "30d"

    audits = [event for event in events if event["tool_name"] == "market_insight"]
    assert len(audits) == 5
    assert audits[1]["payload"]["request"]["filters_used"]["compound_name"] == "Mivida"
    assert audits[2]["payload"]["request"]["filters_used"]["h3_res9"] == h3_res9
    assert audits[3]["payload"]["request"]["filters_used"]["property_type"] == "Villa"
    assert audits[4]["payload"]["request"]["filters_used"]["time_window"] == "30d"
    assert cross_tenant.status_code == 404
