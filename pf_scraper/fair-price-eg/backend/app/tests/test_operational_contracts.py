from pathlib import Path
import time

import pytest
from fastapi.testclient import TestClient

from app.api.routes import pricing as pricing_routes
from app.main import app


REPO_ROOT = Path(__file__).resolve().parents[3]


def test_postgis_indexes_support_spatial_and_market_snapshot_queries():
    indexes_sql = (REPO_ROOT / "docker" / "postgres" / "init" / "04_indexes.sql").read_text(encoding="utf-8")

    assert "ix_listings_geom_geog_gist" in indexes_sql
    assert "USING gist((geom::geography))" in indexes_sql
    assert "ix_listings_match_area_recency" in indexes_sql
    assert "category, period, property_type, bedrooms, area_id, scraped_at_utc DESC" in indexes_sql
    assert "ix_listings_market_snapshot" in indexes_sql


@pytest.mark.performance
def test_patched_valuation_endpoint_stays_within_local_latency_budget(monkeypatch):
    comps = [
        {
            "listing_id": f"latency-{index:03d}",
            "price_egp": 30000 + index,
            "size_sqm": 150,
            "property_type": "Apartment",
            "bedrooms": 3,
            "bathrooms": 2,
            "area_id": 10,
            "area_name": "Central Cairo",
            "dist_m": 400,
            "age_days": 10,
            "is_same_area": True,
        }
        for index in range(12)
    ]
    monkeypatch.setattr(pricing_routes, "nearest_area", lambda db, lat, lng: {"area_id": 10, "name": "Central Cairo"})
    monkeypatch.setattr(
        pricing_routes,
        "fetch_comps",
        lambda db, params, include_trace: (
            comps,
            1,
            [{"tier": 1, "reason_code": "SAME_AREA_MATCH", "comps_found": len(comps)}],
        ),
    )
    client = TestClient(app)

    start = time.perf_counter()
    response = client.post(
        "/v1/rent/fair-price",
        json={
            "lat": 30.0444,
            "lng": 31.2357,
            "property_type": "Apartment",
            "bedrooms": 3,
            "bathrooms": 2,
            "size_sqm": 150,
        },
    )
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert response.status_code == 200
    assert elapsed_ms < 250
