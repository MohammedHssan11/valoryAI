from fastapi.testclient import TestClient

from app.main import app


def test_routes_are_registered_once():
    route_keys = [
        (tuple(sorted(route.methods)), route.path)
        for route in app.routes
        if hasattr(route, "methods")
    ]

    assert route_keys.count((("GET",), "/health")) == 1
    assert route_keys.count((("POST",), "/v1/rent/fair-price")) == 1
    assert route_keys.count((("POST",), "/v1/auth/token-exchange")) == 1
    assert route_keys.count((("POST",), "/v1/broker/analyze")) == 1
    assert route_keys.count((("POST",), "/v1/broker/chat")) == 1
    assert route_keys.count((("POST",), "/v1/broker/intent")) == 1
    assert route_keys.count((("POST",), "/v1/broker/reason")) == 1
    assert route_keys.count((("POST",), "/v1/broker/stream")) == 1
    assert route_keys.count((("POST",), "/v1/copilot/tools/comparable")) == 1
    assert route_keys.count((("POST",), "/v1/copilot/tools/fairness")) == 1
    assert route_keys.count((("POST",), "/v1/copilot/tools/negotiation")) == 1
    assert route_keys.count((("POST",), "/v1/copilot/tools/what-if")) == 1


def test_health_endpoint_is_backward_compatible_and_enveloped():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "ok"
    assert "meta" in body


def test_cors_allows_configured_local_frontend_origin():
    client = TestClient(app)

    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
