from __future__ import annotations

from datetime import datetime, timezone

from app.comps import selector
from app.comps.selector import fetch_comps


class FakeResult:
    def __init__(self, rows=None, first_row=None):
        self.rows = rows or []
        self.first_row = first_row

    def mappings(self):
        return self

    def all(self):
        return self.rows

    def first(self):
        return self.first_row


class FakeDB:
    def __init__(self, counts):
        self.counts = counts
        self.calls = []

    def execute(self, statement, params=None):
        if params is None or "scope" not in params:
            return FakeResult(first_row={"as_of_utc": datetime(2026, 1, 1, tzinfo=timezone.utc)})

        self.calls.append(dict(params))
        count = self.counts.get((params["scope"], params["radius_m"]), self.counts.get(params["scope"], 0))
        return FakeResult(
            rows=[
                {
                    "listing_id": f"{params['scope']}-{params['radius_m']}-{index:03d}",
                    "price_egp": 10000 + index,
                    "size_sqm": 100,
                    "property_type": params["property_type"],
                    "bedrooms": params["bedrooms"],
                    "bathrooms": params["bathrooms"],
                    "dist_m": index,
                    "age_days": index,
                }
                for index in range(count)
            ]
        )


def base_params():
    return {
        "lat": 30.0,
        "lng": 31.0,
        "area_id": 1,
        "property_type": "Apartment",
        "bedrooms": 2,
        "bathrooms": 2,
        "size_sqm": 120,
    }


def test_fetch_comps_reaches_governorate_fallback_in_declared_sequence():
    db = FakeDB({("same_governorate", 15000): 18})

    rows, tier, trace = fetch_comps(db, base_params(), include_trace=True)

    assert tier == 5
    assert len(rows) == 18
    assert [(call["scope"], call["radius_m"]) for call in db.calls] == [
        ("same_area", 500),
        ("same_area", 1000),
        ("same_district", 2000),
        ("nearby_districts", 5000),
        ("same_city", 10000),
        ("same_governorate", 15000),
    ]
    assert [entry["reason_code"] for entry in trace][-1] == "GOVERNORATE_FALLBACK"
    assert trace[-1]["status"] == "selected"


def test_fetch_comps_passes_recency_size_and_guardrail_params_to_sql():
    db = FakeDB({("same_area", 500): 45})

    fetch_comps(db, base_params(), include_trace=True)

    first_call = db.calls[0]
    assert first_call["stale_days"] == 90
    assert first_call["size_low"] == 0.85
    assert first_call["size_high"] == 1.15
    assert first_call["min_price_egp"] == 1000
    assert first_call["max_price_egp"] == 500000
    assert first_call["listing_category"] == "rent"
    assert first_call["listing_period"] == "monthly"
    assert first_call["property_category"] == "residential_rent"
    assert first_call["limit"] <= 800
    assert first_call["tier_number"] == 1


def test_tier_sql_preserves_recency_filter_and_deterministic_ordering():
    sql = selector.TIER_SQL[1]

    assert "l.scraped_at_utc >= (:as_of_utc - (:stale_days * INTERVAL '1 day'))" in sql
    assert "l.category = :listing_category" in sql
    assert "l.period = :listing_period" in sql
    assert "ORDER BY" in sql
    assert "dist_m ASC" in sql
    assert "l.scraped_at_utc DESC" in sql
    assert "l.price_egp ASC" in sql
    assert "l.listing_id ASC" in sql


def test_fetch_comps_uses_category_specific_retrieval_contract():
    params = {
        **base_params(),
        "property_category": "villa_sale",
        "property_type": "Villa",
        "target_features": {"amenities": ["PG", "PP"], "normalized_amenities": ["private_garden", "private_pool"], "canonical_amenity_symbols": ["PG", "PP"]},
    }
    db = FakeDB({("same_area", 725): 25})

    rows, tier, trace = fetch_comps(db, params, include_trace=True)

    assert tier == 1
    assert len(rows) == 25
    first_call = db.calls[0]
    assert first_call["listing_category"] == "buy"
    assert first_call["listing_period"] == "sale"
    assert first_call["property_category"] == "villa_sale"
    assert first_call["radius_m"] == 725
    assert first_call["size_low"] == 0.70
    assert first_call["size_high"] == 1.35
    assert first_call["stale_days"] == 180
    assert trace[0]["threshold"] == 22


def test_fetch_comps_supports_nullable_numeric_metadata_for_commercial_office():
    params = {
        **base_params(),
        "property_category": "office_rent",
        "property_type": "Office",
        "bedrooms": None,
        "bathrooms": None,
    }
    db = FakeDB({"same_area": 100})

    rows, tier, trace = fetch_comps(db, params, include_trace=True)

    assert tier == 1
    assert len(rows) == 100
    first_call = db.calls[0]
    assert first_call["bedrooms"] is None
    assert first_call["bathrooms"] is None
    assert first_call["property_category"] == "office_rent"


def test_fetch_comps_supports_nullable_numeric_metadata_for_land_sale():
    params = {
        **base_params(),
        "property_category": "land_sale",
        "property_type": "Land",
        "bedrooms": None,
        "bathrooms": None,
    }
    db = FakeDB({"same_area": 100})

    rows, tier, trace = fetch_comps(db, params, include_trace=True)

    assert tier == 1
    assert len(rows) == 100
    first_call = db.calls[0]
    assert first_call["bedrooms"] is None
    assert first_call["bathrooms"] is None
    assert first_call["property_category"] == "land_sale"


def test_fetch_comps_supports_mixed_nullable_metadata_for_retail():
    params = {
        **base_params(),
        "property_category": "retail_rent",
        "property_type": "Retail",
        "bedrooms": None,
        "bathrooms": 1,
    }
    db = FakeDB({"same_area": 100})

    rows, tier, trace = fetch_comps(db, params, include_trace=True)

    assert tier == 1
    assert len(rows) == 100
    first_call = db.calls[0]
    assert first_call["bedrooms"] is None
    assert first_call["bathrooms"] == 1
    assert first_call["property_category"] == "retail_rent"

