from __future__ import annotations

from fastapi.testclient import TestClient

from app.api.routes import pricing as pricing_routes
from app.main import app


BASE_REQUEST = {
    "lat": 30.0444,
    "lng": 31.2357,
    "property_type": "Apartment",
    "bedrooms": 3,
    "bathrooms": 2,
    "size_sqm": 150,
    "target_price_egp": 35000,
    "amenities": [],
}


def make_comp(
    index: int,
    price_egp: int,
    *,
    size_sqm: float = 150,
    dist_m: float = 400,
    age_days: float = 15,
    area_id: int = 10,
    area_name: str = "Central Cairo",
    is_same_area: bool = True,
):
    return {
        "listing_id": f"comp-{index:03d}",
        "price_egp": price_egp,
        "size_sqm": size_sqm,
        "property_type": "Apartment",
        "bedrooms": 3,
        "bathrooms": 2,
        "area_id": area_id,
        "area_name": area_name,
        "dist_m": dist_m,
        "age_days": age_days,
        "is_same_area": is_same_area,
        "tier_label": "same compound/neighborhood",
        "reason_code": "SAME_AREA_MATCH",
    }


def install_comparable_snapshot(monkeypatch, comps, *, tier=1, trace=None, area=None):
    area = area or {"area_id": 10, "name": "Central Cairo", "level": 4}
    trace = trace or [
        {
            "tier": tier,
            "tier_label": "same compound/neighborhood",
            "reason_code": "SAME_AREA_MATCH",
            "scope": "same_area",
            "radius_m": 500,
            "comps_found": len(comps),
            "threshold": 40,
        }
    ]
    monkeypatch.setattr(pricing_routes, "nearest_area", lambda db, lat, lng: area)
    monkeypatch.setattr(pricing_routes, "fetch_comps", lambda db, params, include_trace: (comps, tier, trace))


def post_valuation(payload=BASE_REQUEST, *, request_id="valuation-regression"):
    client = TestClient(app)
    return client.post("/v1/rent/fair-price", json=payload, headers={"X-Request-ID": request_id})


def test_same_request_produces_identical_valuation_snapshot(monkeypatch):
    prices = [30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000]
    install_comparable_snapshot(monkeypatch, [make_comp(index, price) for index, price in enumerate(prices)])

    first = post_valuation(request_id="stable-snapshot")
    second = post_valuation(request_id="stable-snapshot")

    assert first.status_code == 200
    assert first.json() == second.json()
    data = first.json()["data"]
    assert data["fair_price_egp"] == 36000
    assert data["range_low_egp"] == 32000
    assert data["range_high_egp"] == 39000
    assert data["confidence"]["label"] == "Medium"
    assert round(data["confidence"]["score"], 3) == 0.734
    assert [comp["listing_id"] for comp in data["top_comps"][:3]] == ["comp-000", "comp-001", "comp-002"]


def test_luxury_apartment_regression_snapshot_detects_drift(monkeypatch):
    payload = {
        **BASE_REQUEST,
        "size_sqm": 220,
        "target_price_egp": 100000,
        "amenities": ["BA", "SE"],
        "furnishing_status": "furnished",
    }
    prices = [78000, 80000, 82000, 85000, 88000, 90000, 92000, 96000, 100000, 105000, 110000, 115000]
    comps = [
        {
            **make_comp(index, price, size_sqm=220, dist_m=250, age_days=7),
            "normalized_amenities": ["balcony", "security"],
            "unknown_amenity_codes": [],
            "furnishing_status": "furnished",
        }
        for index, price in enumerate(prices)
    ]
    install_comparable_snapshot(monkeypatch, comps)

    response = post_valuation(payload, request_id="luxury-regression")

    assert response.status_code == 200
    body = response.json()
    snapshot = {
        "fair_price_egp": body["data"]["fair_price_egp"],
        "range_low_egp": body["data"]["range_low_egp"],
        "range_high_egp": body["data"]["range_high_egp"],
        "flag": body["data"]["flag"],
        "tier_used": body["data"]["tier_used"],
        "comps_count": body["data"]["comps_count"],
        "confidence_label": body["data"]["confidence"]["label"],
        "confidence_score": round(body["data"]["confidence"]["score"], 3),
        "trace_codes": [item["reason_code"] for item in body["data"]["explanation_trace"]],
    }
    assert snapshot == {
        "fair_price_egp": 90000,
        "range_low_egp": 82000,
        "range_high_egp": 105000,
        "flag": "OK",
            "tier_used": 1,
            "comps_count": 12,
            "confidence_label": "Medium",
            "confidence_score": 0.742,
            "trace_codes": [
                "CATEGORY_VALUATION_CONTRACT",
                "ADDRESS_RESOLUTION",
                "SAME_AREA_MATCH",
                "HARD_GUARDRAILS_APPLIED",
                "MAD_OUTLIER_FILTER_APPLIED",
                "CONFIDENCE_FACTORS",
                "FEATURE_SIMILARITY_APPLIED",
                "AMENITY_INTELLIGENCE_APPLIED",
                "WEIGHTED_COMPARABLE_EVIDENCE",
            ],
        }


def test_extreme_prices_are_removed_before_fair_price_is_computed(monkeypatch):
    normal_prices = [25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000]
    comps = [make_comp(index, price) for index, price in enumerate(normal_prices)]
    comps.extend(
        [
            make_comp(98, 900000),
            make_comp(99, 500),
        ]
    )
    install_comparable_snapshot(monkeypatch, comps)

    response = post_valuation(request_id="guardrail-regression")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["fair_price_egp"] == 30000
    assert data["range_low_egp"] == 27000
    assert data["range_high_egp"] == 32000
    assert data["comps_count"] == 10
    assert any("Hard guardrails removed 2 records" in item for item in data["explanation"])


def test_no_comps_returns_insufficient_data_without_hallucinated_price(monkeypatch):
    install_comparable_snapshot(
        monkeypatch,
        [],
        tier=5,
        trace=[
            {
                "tier": 5,
                "tier_label": "same governorate fallback",
                "reason_code": "GOVERNORATE_FALLBACK",
                "scope": "same_governorate",
                "radius_m": 15000,
                "comps_found": 0,
                "threshold": 40,
            }
        ],
    )

    response = post_valuation(request_id="no-comps-regression")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["flag"] == "INSUFFICIENT_DATA"
    assert data["fair_price_egp"] == 0
    assert data["range_low_egp"] == 0
    assert data["range_high_egp"] == 0
    assert data["confidence"]["score"] == 0.0
    assert data["confidence"]["label"] == "Low"
    assert data["explanation_trace"][0]["reason_code"] == "CATEGORY_VALUATION_CONTRACT"
    assert data["explanation_trace"][1]["reason_code"] == "INSUFFICIENT_COMPARABLES"


def test_stale_governorate_fallback_degrades_confidence(monkeypatch):
    prices = [22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000]
    comps = [
        {
            **make_comp(index, price, dist_m=14000, age_days=360, area_id=99, area_name="Fallback Governorate", is_same_area=False),
            "tier_label": "same governorate fallback",
            "reason_code": "GOVERNORATE_FALLBACK",
        }
        for index, price in enumerate(prices)
    ]
    install_comparable_snapshot(
        monkeypatch,
        comps,
        tier=5,
        trace=[
            {
                "tier": 5,
                "tier_label": "same governorate fallback",
                "reason_code": "GOVERNORATE_FALLBACK",
                "scope": "same_governorate",
                "radius_m": 15000,
                "comps_found": len(comps),
                "threshold": 40,
            }
        ],
    )

    response = post_valuation(request_id="stale-fallback-regression")

    assert response.status_code == 200
    confidence = response.json()["data"]["confidence"]
    assert confidence["label"] == "Low"
    assert confidence["score"] < 0.50
    assert confidence["factors"]["tier"] < 0.15
    assert confidence["factors"]["distance"] < 0.10
    assert confidence["factors"]["recency"] < 0.20


def test_missing_structured_features_do_not_create_feature_similarity_trace(monkeypatch):
    prices = [30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000]
    install_comparable_snapshot(monkeypatch, [make_comp(index, price) for index, price in enumerate(prices)])

    response = post_valuation(request_id="missing-features-regression")

    assert response.status_code == 200
    data = response.json()["data"]
    assert "FEATURE_SIMILARITY_APPLIED" not in [item["reason_code"] for item in data["explanation_trace"]]
    assert data["top_comps"][0]["feature_similarity"] is None
    assert data["top_comps"][0]["weight_components"]["feature_similarity"] == 1.0
