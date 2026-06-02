from app.core.enums import ConfidenceLevel
from app.pricing.confidence import compute_confidence


def test_confidence_degrades_for_stale_far_and_poor_similarity_signals():
    strong = compute_confidence(
        comps_count=90,
        tier_used=1,
        kept_ratio=0.98,
        dispersion_ratio=0.15,
        avg_distance_m=200,
        avg_age_days=5,
        avg_similarity=0.95,
    )
    stale_far_poor = compute_confidence(
        comps_count=90,
        tier_used=1,
        kept_ratio=0.98,
        dispersion_ratio=0.15,
        avg_distance_m=14000,
        avg_age_days=360,
        avg_similarity=0.15,
    )

    assert strong["score"] > stale_far_poor["score"]
    assert stale_far_poor["factors"]["distance"] < 0.10
    assert stale_far_poor["factors"]["recency"] < 0.20
    assert stale_far_poor["factors"]["similarity"] == 0.15


def test_confidence_never_high_for_sparse_governorate_fallback():
    result = compute_confidence(
        comps_count=10,
        tier_used=5,
        kept_ratio=1.0,
        dispersion_ratio=0.10,
        avg_distance_m=13000,
        avg_age_days=250,
        avg_similarity=1.0,
    )

    assert result["label"] == ConfidenceLevel.LOW.value
    assert result["score"] < 0.50
    assert result["factors"]["count"] < 0.20
    assert result["factors"]["tier"] < 0.15


def test_confidence_penalizes_sparse_and_noisy_markets():
    stable_market = compute_confidence(
        comps_count=80,
        tier_used=1,
        kept_ratio=0.95,
        dispersion_ratio=0.20,
        avg_distance_m=500,
        avg_age_days=20,
        avg_similarity=0.90,
    )
    sparse_noisy_market = compute_confidence(
        comps_count=11,
        tier_used=3,
        kept_ratio=0.55,
        dispersion_ratio=0.90,
        avg_distance_m=5000,
        avg_age_days=120,
        avg_similarity=0.50,
    )

    assert stable_market["label"] == ConfidenceLevel.HIGH.value
    assert sparse_noisy_market["label"] == ConfidenceLevel.LOW.value
    assert sparse_noisy_market["score"] < stable_market["score"]
