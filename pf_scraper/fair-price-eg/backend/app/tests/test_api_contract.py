from fastapi.testclient import TestClient

from app.api.routes import pricing as pricing_routes
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


def test_pricing_success_uses_standard_response_envelope(monkeypatch):
    rows = [comp(index) for index in range(12)]
    monkeypatch.setattr(pricing_routes, "nearest_area", lambda db, lat, lng: {"area_id": 10, "name": "Central Cairo"})
    monkeypatch.setattr(
        pricing_routes,
        "fetch_comps",
        lambda db, params, include_trace: (
            rows,
            1,
            [
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
        ),
    )
    monkeypatch.setattr(pricing_routes, "hard_guardrails", lambda comps, **kwargs: (comps, {"kept": len(comps), "removed": 0}))
    monkeypatch.setattr(pricing_routes, "mad_filter", lambda comps: (comps, {"kept": len(comps), "removed": 0}))
    monkeypatch.setattr(pricing_routes, "compute_weights", lambda comps, size_sqm, **kwargs: comps)
    monkeypatch.setattr(pricing_routes, "weighted_median", lambda prices, weights: 30000)
    monkeypatch.setattr(pricing_routes, "weighted_quantile", lambda prices, weights, quantile: 28000 if quantile < 0.5 else 33000)
    monkeypatch.setattr(
        pricing_routes,
        "compute_confidence",
        lambda *args, **kwargs: {
            "score": 0.82,
            "label": "High",
            "factors": {
                "count": 0.35,
                "tier": 0.25,
                "kept_ratio": 0.2,
                "dispersion": 0.12,
            },
        },
    )
    monkeypatch.setattr(pricing_routes, "build_explanation", lambda **kwargs: ["12 comparable listings retained."])
    monkeypatch.setattr(
        pricing_routes,
        "build_explanation_trace",
        lambda *args, **kwargs: [{"reason_code": "CONFIDENCE_SCORE", "details": {"score": 0.82}}],
    )
    monkeypatch.setattr(pricing_routes, "pick_top_comps", lambda weighted, n: weighted[:2])

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
