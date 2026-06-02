import pytest
from pydantic import ValidationError

from app.api.schemas.pricing import RentFairPriceRequest
from app.pricing.contracts import category_contract, public_category_contract


def test_property_category_contracts_map_to_distinct_market_segments():
    rent = category_contract("residential_rent")
    sale = category_contract("residential_sale")
    office = category_contract("office_rent")
    land = category_contract("land_sale")

    assert rent.listing_category.value == "rent"
    assert rent.period.value == "monthly"
    assert sale.listing_category.value == "buy"
    assert sale.period.value == "sale"
    assert office.listing_category.value == "commercial_rent"
    assert land.guardrails.max_size_sqm > rent.guardrails.max_size_sqm
    assert public_category_contract("retail_rent")["governance"]["amenities_override_pricing"] is False


def test_request_bounds_are_category_specific_and_backward_compatible():
    with pytest.raises(ValidationError):
        RentFairPriceRequest(
            lat=30.0,
            lng=31.0,
            property_type="Apartment",
            size_sqm=120,
            target_price_egp=500001,
        )

    sale = RentFairPriceRequest(
        lat=30.0,
        lng=31.0,
        property_category="residential_sale",
        property_type="Apartment",
        size_sqm=120,
        target_price_egp=5_000_000,
    )

    assert sale.property_category == "residential_sale"
    assert sale.target_price_egp == 5_000_000


def test_land_category_accepts_larger_size_without_relaxing_residential_contract():
    land = RentFairPriceRequest(
        lat=30.0,
        lng=31.0,
        property_category="land_sale",
        property_type="Land",
        size_sqm=5000,
        target_price_egp=10_000_000,
    )

    assert land.property_category == "land_sale"
    assert land.size_sqm == 5000
