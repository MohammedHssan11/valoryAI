from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

pytestmark = pytest.mark.integration

if os.environ.get("RUN_POSTGIS_INTEGRATION") != "1":
    pytest.skip("Set RUN_POSTGIS_INTEGRATION=1 with a seeded PostGIS database to run.", allow_module_level=True)

from app.db.session import engine  # noqa: E402
from app.main import app  # noqa: E402


def test_postgis_extension_and_full_valuation_pipeline_are_available():
    with engine.connect() as connection:
        postgis_version = connection.execute(text("SELECT PostGIS_Version()")).scalar_one()

    assert postgis_version

    with TestClient(app) as client:
        ready = client.get("/health/ready", headers={"X-Request-ID": "integration-ready"})
        assert ready.status_code == 200
        assert ready.json()["success"] is True

        response = client.post(
            "/v1/rent/fair-price",
            json={
                "lat": 30.0444,
                "lng": 31.2357,
                "property_type": "Apartment",
                "bedrooms": 3,
                "bathrooms": 2,
                "size_sqm": 150,
                "target_price_egp": 30000,
                "amenities": ["BA", "SE"],
            },
            headers={"X-Request-ID": "integration-valuation"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["meta"]["request_id"] == "integration-valuation"
    assert body["data"]["flag"] in {"INSUFFICIENT_DATA", "NO_TARGET", "TOO_HIGH", "TOO_LOW", "OK"}
    assert isinstance(body["data"]["explanation_trace"], list)
    assert body["data"]["confidence"]["label"] in {"High", "Medium", "Low"}
