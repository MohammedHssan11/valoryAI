from app.core.property_features import normalize_property_features
from app.pricing.estimator import compute_weights
from app.pricing.feature_similarity import compute_feature_similarity


def test_feature_similarity_details_include_amenity_matches_and_unknowns():
    target = normalize_property_features({"amenities": ["BA", "SE", "XY"]})
    comp = normalize_property_features({"amenities": ["BA", "CP", "ZZ"]})

    result = compute_feature_similarity(target, comp)

    assert round(result["score"], 6) == round(0.04 / (0.04 + 0.04 + 0.03), 6)
    assert round(result["components"]["amenities"], 6) == round(0.04 / (0.04 + 0.04 + 0.03), 6)
    assert result["details"]["matched_amenities"] == ["balcony"]
    assert result["details"]["missing_amenities"] == ["security"]
    assert result["details"]["matched_amenity_symbols"] == ["BA"]
    assert result["details"]["target_unknown_amenity_codes"] == ["XY"]
    assert result["details"]["comp_unknown_amenity_codes"] == ["ZZ"]


def test_feature_weight_is_bounded_and_deterministic():
    target = normalize_property_features({"amenities": ["BA", "SE"]})
    comps = [
        {
            "listing_id": "feature-match",
            "price_egp": 10000,
            "size_sqm": 100,
            "dist_m": 100,
            "age_days": 5,
            **normalize_property_features({"amenities": ["BA", "SE"]}),
        },
        {
            "listing_id": "feature-miss",
            "price_egp": 10000,
            "size_sqm": 100,
            "dist_m": 100,
            "age_days": 5,
            **normalize_property_features({"amenities": ["CP"]}),
        },
    ]

    first = compute_weights(comps, target_size=100, target_features=target)
    second = compute_weights(comps, target_size=100, target_features=target)

    assert first == second
    assert first[0]["weight_components"]["feature_similarity"] == 1.0
    assert 0.92 <= first[1]["weight_components"]["feature_similarity"] <= 1.0
    assert first[0]["weight"] > first[1]["weight"]


def test_feature_weight_does_not_apply_without_target_features():
    weighted = compute_weights(
        [
            {
                "listing_id": "no-target",
                "price_egp": 10000,
                "size_sqm": 100,
                "dist_m": 100,
                "age_days": 5,
                **normalize_property_features({"amenities": ["BA"]}),
            }
        ],
        target_size=100,
    )

    assert weighted[0]["feature_similarity"] is None
    assert weighted[0]["weight_components"]["feature_similarity"] == 1.0


def test_category_amenity_weighting_changes_similarity_deterministically():
    target = normalize_property_features({"amenities": ["RF", "VI"]})
    comp = normalize_property_features({"amenities": ["RF"]})

    retail = compute_feature_similarity(target, comp, property_category="retail_rent")
    residential = compute_feature_similarity(target, comp, property_category="residential_rent")

    assert retail["components"]["amenities"] < 1.0
    assert retail["components"]["amenities"] != residential["components"]["amenities"]
    assert retail["details"]["property_category"] == "retail_rent"
