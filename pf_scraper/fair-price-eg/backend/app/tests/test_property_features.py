import json

from app.core.property_features import (
    amenity_similarity,
    extract_compound_name,
    normalize_amenities,
    normalize_property_features,
)


def test_normalize_amenities_preserves_unknown_codes():
    normalized = normalize_amenities(["BA", "SE", "XY", "BA"])

    assert normalized["known"] == ["balcony", "security"]
    assert normalized["unknown"] == ["XY"]
    assert normalized["symbols"] == ["BA", "SE"]
    assert normalized["items"][0]["symbol"] == "BA"
    assert normalized["items"][0]["normalized"] == "balcony"
    assert normalized["items"][0]["known"] is True
    assert normalized["items"][1]["symbol"] == "SE"
    assert normalized["items"][2] == {"raw": "XY", "normalized": None, "known": False}


def test_amenity_similarity_uses_jaccard_and_ignores_unknowns():
    target = normalize_amenities(["BA", "SE", "XY"])
    comp = normalize_amenities(["BA", "CP"])

    result = amenity_similarity(target["items"], comp["items"])

    assert round(result["score"], 6) == round(0.04 / (0.04 + 0.04 + 0.03), 6)
    assert result["matched"] == ["balcony"]
    assert result["missing"] == ["security"]
    assert result["extra"] == ["covered_parking"]
    assert result["matched_symbols"] == ["BA"]


def test_compound_extraction_uses_structured_location_hierarchy_only():
    assert (
        extract_compound_name(
            "Villette, 5th Settlement Compounds, The 5th Settlement, New Cairo City, Cairo"
        )
        == "Villette"
    )
    assert extract_compound_name("Hyde Park, New Cairo City, Cairo") is None


def test_property_feature_normalization_is_json_serializable():
    features = normalize_property_features(
        {
            "amenities": "['VW', 'BL', 'AN']",
            "location_text": "Lake View, 5th Settlement Compounds, Cairo",
            "furnishing_status": "Fully Furnished",
            "floor_number": "Ground floor",
        }
    )

    assert features["normalized_amenities"] == ["landmark_view", "water_view"]
    assert features["unknown_amenity_codes"] == ["AN"]
    assert features["view_type"] == "water_and_landmark"
    assert features["compound_name"] == "Lake View"
    assert features["furnishing_status"] == "furnished"
    assert features["floor_number"] == 0
    json.dumps(features)
