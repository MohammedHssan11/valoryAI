from fastapi.testclient import TestClient

from app.core import logging as logging_core
from app.api.routes import health as health_routes
from app.core.enums import ConfidenceLevel, PriceFlag, PropertyCategory, PropertyType
from app.main import app


def test_health_ready_success_uses_standard_envelope(monkeypatch):
    monkeypatch.setattr(health_routes, "check_database", lambda: None)
    client = TestClient(app)

    response = client.get("/health/ready", headers={"X-Request-ID": "ready-ok"})

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": {"database": "ok"},
        "meta": {"request_id": "ready-ok"},
    }
    assert response.headers["X-Request-ID"] == "ready-ok"


def test_health_ready_failure_uses_standard_error_envelope(monkeypatch):
    def fail_database():
        raise RuntimeError("database unavailable")

    monkeypatch.setattr(health_routes, "check_database", fail_database)
    client = TestClient(app)

    response = client.get("/health/ready", headers={"X-Request-ID": "ready-failed"})

    assert response.status_code == 503
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "DATABASE_UNAVAILABLE"
    assert body["error"]["details"] == []
    assert body["meta"]["request_id"] == "ready-failed"
    assert response.headers["X-Request-ID"] == "ready-failed"


def test_validation_errors_echo_request_id_in_header_and_meta():
    client = TestClient(app)

    response = client.post(
        "/v1/rent/fair-price",
        json={
            "lat": 100,
            "lng": 31.2357,
            "property_type": "Apartment",
            "size_sqm": 150,
        },
        headers={"X-Request-ID": "invalid-contract"},
    )

    assert response.status_code == 422
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "INVALID_COORDINATES"
    assert body["meta"]["request_id"] == "invalid-contract"
    assert response.headers["X-Request-ID"] == "invalid-contract"


def test_correlation_id_is_propagated_in_response_headers():
    client = TestClient(app)

    response = client.get(
        "/health",
        headers={"X-Request-ID": "trace-request", "X-Correlation-ID": "trace-correlation"},
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "trace-request"
    assert response.headers["X-Correlation-ID"] == "trace-correlation"


def test_rate_limited_requests_use_standard_error_envelope(monkeypatch):
    monkeypatch.setattr(logging_core, "rate_limiter", logging_core.InMemoryRateLimiter(max_requests=1))
    client = TestClient(app)
    payload = {
        "lat": 100,
        "lng": 31.2357,
        "property_type": "Apartment",
        "size_sqm": 150,
    }
    headers = {"X-Forwarded-For": "203.0.113.10", "X-Request-ID": "rate-limit-1"}

    first = client.post("/v1/rent/fair-price", json=payload, headers=headers)
    second = client.post(
        "/v1/rent/fair-price",
        json=payload,
        headers={**headers, "X-Request-ID": "rate-limit-2"},
    )

    assert first.status_code == 422
    assert second.status_code == 429
    body = second.json()
    assert body["success"] is False
    assert body["error"]["code"] == "RATE_LIMIT_EXCEEDED"
    assert body["meta"]["request_id"] == "rate-limit-2"
    assert second.headers["X-Request-ID"] == "rate-limit-2"
    assert "Retry-After" in second.headers


def test_openapi_documents_pricing_examples_and_metrics_endpoint():
    client = TestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200
    document = response.json()
    fair_price = document["paths"]["/v1/rent/fair-price"]["post"]
    assert fair_price["summary"] == "Estimate fair residential rent"
    assert "429" in fair_price["responses"]
    assert "/health/metrics" in document["paths"]
    assert "/health/operational" in document["paths"]


def test_runtime_metrics_endpoint_uses_standard_envelope():
    client = TestClient(app)
    client.get("/health", headers={"X-Request-ID": "metrics-seed"})

    response = client.get("/health/metrics", headers={"X-Request-ID": "metrics-read"})

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["meta"]["request_id"] == "metrics-read"
    assert "counters" in body["data"]
    assert "histograms" in body["data"]
    assert "recent_events" in body["data"]


def test_operational_health_endpoint_exposes_slo_summary():
    client = TestClient(app)

    response = client.get("/health/operational", headers={"X-Request-ID": "operational-read"})

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["meta"]["request_id"] == "operational-read"
    assert body["data"]["status"] in {"ok", "degraded"}
    assert "checks" in body["data"]
    assert "distributions" in body["data"]
    assert "recent" in body["data"]


def test_public_enum_values_remain_stable_for_api_clients():
    assert {item.value for item in ConfidenceLevel} == {"High", "Medium", "Low"}
    assert {item.value for item in PriceFlag} == {
        "INSUFFICIENT_DATA",
        "NO_TARGET",
        "TOO_HIGH",
        "TOO_LOW",
        "OK",
    }
    assert "Apartment" in {item.value for item in PropertyType}
    assert "Villa" in {item.value for item in PropertyType}
    assert {item.value for item in PropertyCategory} == {
        "residential_rent",
        "residential_sale",
        "villa_sale",
        "office_rent",
        "retail_rent",
        "commercial_rent",
        "land_sale",
    }
