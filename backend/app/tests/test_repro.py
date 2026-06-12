import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)
def test_repro_office_rent(client: TestClient):
    payload = {
        'lat': 30.0444,
        'lng': 31.2357,
        'property_type': 'Office Space',
        'property_category': 'office_rent',
        'bedrooms': 0,
        'bathrooms': 1,
        'size_sqm': 150,
        'amenities': []
    }
    response = client.post('/v1/valuation/fair-price', json=payload)
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())
    assert response.status_code == 200

def test_repro_residential_sale(client: TestClient):
    payload = {
        'lat': 30.0444,
        'lng': 31.2357,
        'property_type': 'Apartment',
        'property_category': 'residential_sale',
        'bedrooms': 3,
        'bathrooms': 2,
        'size_sqm': 150,
        'amenities': []
    }
    response = client.post('/v1/valuation/fair-price', json=payload)
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())
    assert response.status_code == 200
