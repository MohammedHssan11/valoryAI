from fastapi.testclient import TestClient

from app.api.routes import pricing as pricing_routes
from app.api.schemas.pricing import RentFairPriceResponse
from app.main import app


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


def comp(index: int):
    return {
        "listing_id": f"listing-{index}",
        "price_egp": 25000 + index,
        "size_sqm": 145,
        "property_type": "Apartment",
        "bedrooms": 3,
        "bathrooms": 2,
        "area_id": 10,
        "area_name": "Central Cairo",
        "dist_m": 400,
        "age_days": 20,
        "weight": 1.0,
        "weight_components": {
            "size_similarity": 1.0,
            "bathrooms": 1.0,
            "bedrooms": 1.0,
            "property_type": 1.0,
        },
    }


def response_fixture(rows):
    return RentFairPriceResponse(
        fair_price_egp=30000,
        range_low_egp=28000,
        range_high_egp=33000,
        flag="OK",
        tier_used=1,
        comps_count=len(rows),
        confidence={
            "score": 0.82,
            "label": "High",
            "factors": {"count": 1.0, "tier": 1.0, "kept_ratio": 1.0, "dispersion": 0.8},
            "dimensions": {
                "valuation_evidence": {"score": 0.82, "label": "High"},
                "location_resolution": {"score": 0.95, "label": "High"},
            },
        },
        explanation=["12 comparable listings retained."],
        explanation_trace=[{"reason_code": "CONFIDENCE_SCORE", "details": {"score": 0.82}}],
        retrieval_trace=[
            {
                "tier": 1,
                "tier_label": "same compound/neighborhood",
                "reason_code": "SAME_AREA_MATCH",
                "scope": "same_area",
                "radius_m": 500,
                "comps_found": len(rows),
                "threshold": 10,
                "shortfall": 0,
                "attempt_index": 1,
                "status": "selected",
                "selected": True,
            }
        ],
        spatial_diagnostics={"retrieval_radius_m": 500},
        evidence_summary={"authoritative_valuation_frozen": True},
        area={"area_id": 10, "name": "Central Cairo"},
        property_category="residential_rent",
        valuation_contract={"governance": {"amenities_override_pricing": False}},
        amenity_intelligence={"governance": {"canonical_symbol_storage": True}},
        top_comps=rows[:2],
    )


def test_pricing_success_uses_standard_response_envelope(monkeypatch):
    rows = [comp(index) for index in range(12)]

    def route_router(req, db, ctx, background_tasks, request_id):
        assert req.property_type == "Apartment"
        assert ctx["stage"] == "contract_resolution"
        assert request_id.startswith("req_")
        return response_fixture(rows)

    monkeypatch.setattr(pricing_routes, "price_listing_router", route_router)

    client = TestClient(app)
    response = client.post("/v1/rent/fair-price", json=valid_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["fair_price_egp"] == 30000
    assert body["data"]["confidence"]["label"] == "High"
    assert body["data"]["top_comps"][0]["listing_id"] == "listing-0"
    assert body["data"]["retrieval_trace"][0]["selected"] is True
    assert body["data"]["property_category"] == "residential_rent"
    assert body["data"]["valuation_contract"]["governance"]["amenities_override_pricing"] is False
    assert body["data"]["amenity_intelligence"]["governance"]["canonical_symbol_storage"] is True
    assert body["data"]["spatial_diagnostics"]["retrieval_radius_m"] == 500
    assert body["data"]["evidence_summary"]["authoritative_valuation_frozen"] is True
    assert body["meta"]["request_id"]
