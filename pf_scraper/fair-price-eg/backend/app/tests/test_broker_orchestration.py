import uuid
from pathlib import Path

from fastapi.testclient import TestClient

from app.api.schemas.pricing import RentFairPriceResponse
from app.broker.governance.response import response_governance
from app.broker.schemas.contracts import BrokerAnalyticalResponse, BrokerAuthoritativeValues, BrokerContext, GroundingReport
from app.broker.tools import valuation as broker_valuation
from app.broker.validators.grounding import grounding_validator
from app.core.auth import create_access_token
from app.main import app
from app.services.copilot_tools_service import CopilotToolsService


def valid_payload():
    return {
        "lat": 30.0444,
        "lng": 31.2357,
        "property_type": "Apartment",
        "bedrooms": 3,
        "bathrooms": 2,
        "size_sqm": 150,
        "target_price_egp": 30000,
    }


def comparable_evidence(index: int):
    return {
        "property_id": f"broker-listing-{index}",
        "price": 28000 + index * 1000,
        "size_sqm": 145.0,
        "bedrooms": 3,
        "bathrooms": 2,
        "furnishing_status": None,
        "distance_km": 0.4 + index / 100,
        "similarity_score": 0.9,
        "listing_date": "Recent",
    }


def truth_router(request, db, **kwargs):
    return RentFairPriceResponse(
        fair_price_egp=int(request.size_sqm) * 200,
        range_low_egp=28000,
        range_high_egp=33000,
        flag="OK",
        tier_used=1,
        comps_count=12,
        confidence={"score": 0.82, "label": "High", "factors": {}, "dimensions": {}},
        engine_used="CMT",
        routing_reason="GoldilocksZone",
        explainability={
            "router_explanation": "CMT selected by the Router.",
            "confidence_explanation": {
                "confidence_level": "High",
                "confidence_reason": "High confidence because 12 similar properties were found.",
            },
            "fairness_explanation": {
                "estimated_value": int(request.size_sqm) * 200,
                "asking_price": request.target_price_egp,
                "difference_amount": 0,
                "difference_percentage": 0,
                "status": "Within Fair Value Range",
            },
            "narrative_explanation": {
                "summary": f"The property's fair value is {int(request.size_sqm) * 200:,.0f} EGP.",
                "why_this_price": "This is based on similar nearby properties.",
                "strongest_factors": "Nearby prices anchor the valuation.",
                "confidence_reason": "High confidence because 12 similar properties were found.",
            },
            "comparable_evidence": [comparable_evidence(index) for index in range(5)],
            "feature_drivers": [],
        },
        explanation=["12 comparable listings retained."],
        explanation_trace=[{"reason_code": "CONFIDENCE_FACTORS", "details": {"score": 0.82}}],
        area={"area_id": 10, "name": "Central Cairo"},
        resolved_location={"lat": 30.0444, "lng": 31.2357},
    )


def patch_deterministic_pricing(monkeypatch):
    monkeypatch.setattr(
        broker_valuation,
        "CopilotToolsService",
        lambda db: CopilotToolsService(db, router=truth_router),
    )


def parse_sse_events(body: str):
    parsed = []
    for block in body.strip().split("\n\n"):
        event_type = None
        data = None
        for line in block.splitlines():
            if line.startswith("event:"):
                event_type = line.removeprefix("event:").strip()
            if line.startswith("data:"):
                import json

                data = json.loads(line.removeprefix("data:").strip())
        if event_type and data is not None:
            parsed.append((event_type, data))
    return parsed


def broker_context(client: TestClient):
    headers = {"Authorization": f"Bearer {create_access_token(f'broker-{uuid.uuid4()}')}"}
    client.get("/v1/copilot/users/me", headers=headers).raise_for_status()
    workspace = client.post("/v1/copilot/workspaces", headers=headers, json={"name": "Broker Workspace"}).json()
    prop = client.post(
        "/v1/copilot/properties",
        headers=headers,
        json={
            "workspace_id": workspace["id"],
            "label": "Broker Property",
            "location": "New Cairo",
            "area": 150,
            "bedrooms": 3,
            "bathrooms": 2,
            "amenities": {},
            "valuation_inputs": {"lat": 30.0444, "lng": 31.2357, "target_price_egp": 30000},
        },
    ).json()
    scenario = client.post(
        "/v1/copilot/scenarios",
        headers=headers,
        json={"property_state_id": prop["id"], "name": "Broker Scenario", "modifications": {}},
    ).json()
    return headers, {"workspace_id": workspace["id"], "scenario_id": scenario["id"]}


def test_broker_analyze_returns_grounded_institutional_response(monkeypatch):
    patch_deterministic_pricing(monkeypatch)
    client = TestClient(app)
    headers, ownership = broker_context(client)

    response = client.post(
        "/v1/broker/analyze",
        headers=headers,
        json={
            **ownership,
            "message": "Give me an investor risk analysis.",
            "valuation_request": valid_payload(),
            "investor_preferences": {"risk_tolerance": "moderate"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    data = body["data"]
    authoritative = data["response"]["authoritative_values"]
    assert data["grounding"]["status"] == "passed"
    assert data["intent"] == "investor_brief"
    assert data["intent_classification"]["confidence"] > 0.5
    assert data["reasoning_plan"]["selected_tools"] == ["valuation_analysis", "explainability"]
    assert data["governance"]["status"] == "passed"
    assert data["narration"]["provider"] == "deterministic_formatter"
    assert authoritative["fair_price_egp"] == 30000
    assert authoritative["confidence_label"] == "High"
    assert data["context"]["deterministic_authority"]["llm_may_override"] is False
    assert [result["tool_name"] for result in data["tool_results"]] == ["valuation_analysis", "explainability"]
    tool_events = client.get(f"/v1/copilot/workspaces/{ownership['workspace_id']}/tool-events", headers=headers).json()
    assert [event["tool_name"] for event in tool_events[-2:]] == ["valuation", "explainability"]
    assert any(event["stage"] == "classify_intent" for event in data["events"])
    assert any(event["event_type"] == "governance_check" for event in data["events"])


def test_broker_intent_endpoint_is_lightweight_and_rule_assisted():
    client = TestClient(app)
    headers = {"Authorization": f"Bearer {create_access_token(f'intent-{uuid.uuid4()}')}"}

    response = client.post(
        "/v1/broker/intent",
        headers=headers,
        json={
            "message": "Why is this apartment valued lower than nearby properties?",
            "has_valuation_request": True,
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["intent"] == "valuation_explanation"
    assert data["confidence"] >= 0.7
    assert data["has_valuation_request"] is True


def test_broker_session_can_be_retrieved_after_analysis(monkeypatch):
    patch_deterministic_pricing(monkeypatch)
    client = TestClient(app)
    headers, ownership = broker_context(client)

    analyze_response = client.post(
        "/v1/broker/analyze",
        headers=headers,
        json={"session_id": "session-test-001", **ownership, "valuation_request": valid_payload()},
    )
    assert analyze_response.status_code == 200

    session_response = client.get("/v1/broker/session/session-test-001", headers=headers)

    assert session_response.status_code == 200
    session = session_response.json()["data"]
    assert session["session_id"] == "session-test-001"
    assert session["active_district"] is None
    assert len(session["previous_valuations"]) == 1
    assert session["analytical_context"]["last_reasoning_plan_id"].startswith("plan_")


def test_broker_reason_runs_structured_phase_2b_pipeline(monkeypatch):
    patch_deterministic_pricing(monkeypatch)
    client = TestClient(app)
    headers, ownership = broker_context(client)

    response = client.post(
        "/v1/broker/reason",
        headers=headers,
        json={
            **ownership,
            "message": "Discuss confidence and any unusual comparable signals.",
            "valuation_request": valid_payload(),
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["intent"] == "confidence_discussion"
    assert data["grounding"]["status"] == "passed"
    assert data["governance"]["status"] == "passed"
    assert data["reasoning_plan"]["selected_tools"] == ["valuation_analysis", "explainability"]
    assert [event["stage"] for event in data["events"] if event["event_type"] == "stage_completed"][-1] == "finalize_response"


def test_broker_stream_emits_runtime_sse_lifecycle(monkeypatch):
    patch_deterministic_pricing(monkeypatch)
    client = TestClient(app)
    headers, ownership = broker_context(client)

    with client.stream(
        "POST",
        "/v1/broker/stream",
        headers=headers,
        json={
            **ownership,
            "message": "Discuss confidence and district signals.",
            "valuation_request": valid_payload(),
        },
    ) as response:
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/event-stream")
        events = parse_sse_events(response.read().decode())

    event_types = [event_type for event_type, _ in events]
    assert "stage_started" in event_types
    assert "stage_progress" in event_types
    assert "confidence_update" in event_types
    assert "narration_chunk" in event_types
    assert "governance_update" in event_types
    assert "stream_completed" in event_types
    assert "final_response" in event_types
    assert event_types.index("stage_started") < event_types.index("final_response")

    final_response = next(data for event_type, data in events if event_type == "final_response")
    assert final_response["grounding"]["status"] == "passed"
    assert final_response["governance"]["status"] == "passed"


def test_grounding_validator_rejects_authoritative_drift(monkeypatch):
    patch_deterministic_pricing(monkeypatch)
    client = TestClient(app)
    headers, ownership = broker_context(client)
    response = client.post(
        "/v1/broker/analyze",
        headers=headers,
        json={**ownership, "valuation_request": valid_payload()},
    )
    data = response.json()["data"]

    parsed_context = BrokerContext.model_validate(data["context"])
    parsed_response = BrokerAnalyticalResponse.model_validate(data["response"])
    parsed_response.authoritative_values = BrokerAuthoritativeValues(
        **{
            **parsed_response.authoritative_values.model_dump(),
            "fair_price_egp": 999999,
        }
    )

    report = grounding_validator.validate(context=parsed_context, response=parsed_response)

    assert report.status == "failed"
    assert any("fair_price_egp" in violation for violation in report.violations)


def test_response_governance_rejects_unsupported_egp_claim(monkeypatch):
    patch_deterministic_pricing(monkeypatch)
    client = TestClient(app)
    headers, ownership = broker_context(client)
    response = client.post(
        "/v1/broker/analyze",
        headers=headers,
        json={**ownership, "valuation_request": valid_payload()},
    )
    data = response.json()["data"]

    parsed_context = BrokerContext.model_validate(data["context"])
    parsed_response = BrokerAnalyticalResponse.model_validate(data["response"])
    parsed_response.executive_summary = "This asset is guaranteed at 999,999 EGP with risk-free upside."

    report = response_governance.evaluate(
        context=parsed_context,
        response=parsed_response,
        grounding=GroundingReport.model_validate(data["grounding"]),
    )

    assert report.status == "failed"
    assert any("Unsupported EGP" in violation for violation in report.violations)
    assert any("Forbidden broker narration" in violation for violation in report.violations)


def test_broker_adapter_applies_workspace_scenario_through_tool_layer(monkeypatch):
    patch_deterministic_pricing(monkeypatch)
    client = TestClient(app)
    headers = {"Authorization": f"Bearer {create_access_token(f'scenario-{uuid.uuid4()}')}"}
    client.get("/v1/copilot/users/me", headers=headers).raise_for_status()
    workspace = client.post("/v1/copilot/workspaces", headers=headers, json={"name": "Scenario Workspace"}).json()
    prop = client.post(
        "/v1/copilot/properties",
        headers=headers,
        json={
            "workspace_id": workspace["id"],
            "label": "Scenario Property",
            "location": "Central Cairo",
            "area": 150,
            "bedrooms": 3,
            "bathrooms": 2,
            "amenities": {},
            "valuation_inputs": {"lat": 30.0444, "lng": 31.2357},
        },
    ).json()
    scenario = client.post(
        "/v1/copilot/scenarios",
        headers=headers,
        json={"property_state_id": prop["id"], "name": "Expanded", "modifications": {"size_sqm": 175}},
    ).json()

    response = client.post(
        "/v1/broker/chat",
        headers=headers,
        json={
            "workspace_id": workspace["id"],
            "scenario_id": scenario["id"],
            "message": "Explain the scenario valuation.",
            "valuation_request": valid_payload(),
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["degraded_mode"] is False
    assert data["response"]["authoritative_values"]["fair_price_egp"] == 35000
    assert data["context"]["deterministic_authority"]["source_of_truth"] == "copilot_tool_layer"
    assert data["context"]["deterministic_authority"]["valuation_tool"] == "valuation"
    assert data["context"]["deterministic_authority"]["explainability_tool"] == "explainability"
    events = client.get(f"/v1/copilot/workspaces/{workspace['id']}/tool-events", headers=headers).json()
    assert [event["tool_name"] for event in events[-2:]] == ["valuation", "explainability"]
    assert events[-2]["payload"]["request"]["router_request"]["size_sqm"] == 175


def test_broker_adapter_has_no_direct_pricing_route_dependency():
    source = Path(broker_valuation.__file__).read_text(encoding="utf-8")

    assert "app.api.routes" not in source
    assert "pricing_routes" not in source
    assert "rent_fair_price" not in source
