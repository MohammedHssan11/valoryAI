from app.core.property_features import normalize_property_features
from app.pricing.explain import build_explanation_trace, pick_top_comps


def test_top_comps_include_feature_explanation():
    comp = {
        "listing_id": "a",
        "price_egp": 10000,
        "size_sqm": 100,
        "lat": 30.0,
        "lng": 31.0,
        "retrieval_tier": 1,
        "radius_m": 500,
        "dist_m": 100,
        "age_days": 10,
        "weight": 0.5,
        "weight_components": {
            "distance": 0.9,
            "recency": 0.8,
            "size_similarity": 1.0,
            "bathrooms": 1.0,
            "bedrooms": 1.0,
            "property_type": 1.0,
            "feature_similarity": 0.9,
        },
        **normalize_property_features({"amenities": ["BA", "SE"]}),
        "feature_similarity": 0.5,
        "feature_similarity_components": {"amenities": 0.5},
        "feature_explanation": {
            "matched_amenities": ["balcony"],
            "missing_amenities": ["security"],
            "target_unknown_amenity_codes": ["XY"],
        },
    }

    top = pick_top_comps([comp], n=1)

    assert top[0]["normalized_amenities"] == ["balcony", "security"]
    assert top[0]["feature_similarity"] == 0.5
    assert top[0]["feature_explanation"]["matched_amenities"] == ["balcony"]
    assert top[0]["lat"] == 30.0
    assert top[0]["price_per_sqm"] == 100.0
    assert top[0]["weighted_contribution"] == 1.0
    assert top[0]["filter_status"]["mad_outlier"] == "kept"


def test_explanation_trace_summarizes_feature_similarity():
    target = normalize_property_features({"amenities": ["BA", "XY"]})
    trace = build_explanation_trace(
        retrieval_trace=[],
        guard_stats={"removed": 0},
        mad_stats={"kept": 10, "removed": 0},
        confidence={"score": 0.8, "factors": {}},
        target_features=target,
        weighted_comps=[{"feature_similarity": 0.5}, {"feature_similarity": 1.0}],
    )

    feature_entries = [item for item in trace if item["reason_code"] == "FEATURE_SIMILARITY_APPLIED"]

    assert len(feature_entries) == 1
    assert feature_entries[0]["weight"] == 0.75
    assert feature_entries[0]["details"]["target_normalized_amenities"] == ["balcony"]
    assert feature_entries[0]["details"]["target_unknown_amenity_codes"] == ["XY"]


def test_explanation_trace_includes_weighted_comparable_summary():
    trace = build_explanation_trace(
        retrieval_trace=[],
        guard_stats={"removed": 0},
        mad_stats={"kept": 10, "removed": 0},
        confidence={"score": 0.8, "factors": {}},
        weighted_comps=[
            {"listing_id": "b", "weight": 0.2, "dist_m": 20},
            {"listing_id": "a", "weight": 0.5, "dist_m": 50},
        ],
    )

    weighted_entries = [item for item in trace if item["reason_code"] == "WEIGHTED_COMPARABLE_EVIDENCE"]

    assert len(weighted_entries) == 1
    assert weighted_entries[0]["details"]["weighted_comp_count"] == 2
    assert weighted_entries[0]["details"]["top_listing_ids"] == ["a", "b"]
