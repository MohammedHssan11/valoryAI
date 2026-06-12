import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.api.schemas.pricing import RentFairPriceRequest
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


def test_pricing_request_accepts_canonical_property_type():
    dto = RentFairPriceRequest(**valid_payload())

    assert dto.property_type == "Apartment"
    assert dto.location_mode == "manual_coordinates"


def test_pricing_request_rejects_ambiguous_address_and_coordinates_without_mode():
    payload = valid_payload()
    payload["address"] = "Madinaty"

    with pytest.raises(ValidationError):
        RentFairPriceRequest(**payload)


def test_pricing_request_rejects_hidden_precedence_even_with_mode():
    payload = valid_payload()
    payload["location_mode"] = "address_resolution"
    payload["address"] = "Madinaty"

    with pytest.raises(ValidationError):
        RentFairPriceRequest(**payload)


def test_pricing_request_accepts_explicit_address_resolution():
    dto = RentFairPriceRequest(
        location_mode="address_resolution",
        address="  Madinaty  ",
        property_type="Apartment",
        bedrooms=3,
        bathrooms=2,
        size_sqm=150,
    )

    assert dto.address == "Madinaty"
    assert dto.location_mode == "address_resolution"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("lat", 100),
        ("lng", 200),
        ("bedrooms", 21),
        ("bathrooms", -1),
        ("size_sqm", 0),
        ("target_price_egp", 0),
        ("target_price_egp", 500001),
    ],
)
def test_pricing_request_rejects_invalid_bounds(field, value):
    payload = valid_payload()
    payload[field] = value

    with pytest.raises(ValidationError):
        RentFairPriceRequest(**payload)


def test_error_handler_returns_stable_invalid_property_type_response():
    client = TestClient(app)
    payload = valid_payload()
    payload["property_type"] = "Castle"

    response = client.post("/v1/rent/fair-price", json=payload)

    assert response.status_code == 422
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "INVALID_PROPERTY_TYPE"
    assert body["error"]["details"][0]["field"] == "property_type"
    assert response.headers["X-Request-ID"]
