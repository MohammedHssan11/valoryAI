from app.pricing.estimator import compute_weights
from app.pricing.explain import pick_top_comps
from app.pricing.weights import weighted_median, weighted_quantile


def test_weighted_quantile_uses_weighted_ordering():
    values = [100, 200, 300]
    weights = [1, 8, 1]

    assert weighted_median(values, weights) == 200
    assert weighted_quantile(values, weights, 0.80) == 200


def test_compute_weights_adds_positive_weight_without_mutating_input():
    comps = [{"price_egp": 10000, "size_sqm": 100, "dist_m": 500, "age_days": 30}]

    weighted = compute_weights(comps, target_size=100)

    assert "weight" not in comps[0]
    assert weighted[0]["weight"] > 0


def test_size_similarity_is_bounded_without_absurd_bonus():
    comps = [{"price_egp": 10000, "size_sqm": 250, "dist_m": 0, "age_days": 0}]

    weighted = compute_weights(comps, target_size=100)

    assert weighted[0]["weight_components"]["size_similarity"] == 0.0
    assert weighted[0]["weight"] == 0.0


def test_distance_and_recency_weights_decay_predictably():
    comps = [
        {"listing_id": "near-new", "price_egp": 10000, "size_sqm": 100, "dist_m": 100, "age_days": 5},
        {"listing_id": "far-old", "price_egp": 10000, "size_sqm": 100, "dist_m": 5000, "age_days": 180},
    ]

    weighted = compute_weights(comps, target_size=100)

    assert weighted[0]["weight_components"]["distance"] > weighted[1]["weight_components"]["distance"]
    assert weighted[0]["weight_components"]["recency"] > weighted[1]["weight_components"]["recency"]
    assert weighted[0]["weight"] > weighted[1]["weight"]


def test_top_comps_use_stable_tie_breakers():
    weighted = [
        {"listing_id": "b", "price_egp": 10000, "size_sqm": 100, "dist_m": 100, "age_days": 10, "weight": 0.5},
        {"listing_id": "a", "price_egp": 10000, "size_sqm": 100, "dist_m": 100, "age_days": 10, "weight": 0.5},
    ]

    assert [comp["listing_id"] for comp in pick_top_comps(weighted, n=2)] == ["a", "b"]
