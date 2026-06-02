from app.pricing.amenities import amenity_similarity, amenity_weight, normalize_amenities


def test_amenity_normalization_preserves_symbols_and_aliases():
    normalized = normalize_amenities(["balcony", "parking", "XY"], property_category="residential_rent")

    assert normalized["symbols"] == ["BA", "CP"]
    assert normalized["known"] == ["balcony", "covered_parking"]
    assert normalized["unknown"] == ["XY"]
    assert normalized["items"][0]["symbol"] == "BA"
    assert normalized["items"][0]["arabic"] == "بلكونة"
    assert normalized["items"][-1] == {"raw": "XY", "normalized": None, "known": False}


def test_amenity_weight_profiles_are_category_specific():
    assert amenity_weight("PG", "villa_sale") > amenity_weight("PG", "residential_rent")
    assert amenity_weight("RF", "retail_rent") > amenity_weight("RF", "residential_rent")
    assert amenity_weight("ZO", "land_sale") > amenity_weight("ZO", "residential_sale")


def test_amenity_similarity_is_weighted_and_explainable():
    result = amenity_similarity(["RF", "VI", "TR"], ["RF", "TR"], property_category="retail_rent")

    assert 0 < result["score"] < 1
    assert result["matched_symbols"] == ["RF", "TR"]
    assert result["missing_symbols"] == ["VI"]
    assert result["category"] == "retail_rent"
    assert result["weighted_intersection"] < result["weighted_union"]
