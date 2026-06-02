from app.core.enums import ConfidenceLevel
from app.pricing.confidence import compute_confidence


def test_compute_confidence_high_label_for_strong_signal():
    result = compute_confidence(
        comps_count=90,
        tier_used=1,
        kept_ratio=0.95,
        dispersion_ratio=0.20,
        avg_distance_m=400,
        avg_age_days=10,
        avg_similarity=0.95,
    )

    assert result["label"] == ConfidenceLevel.HIGH.value
    assert 0.75 <= result["score"] <= 1.0
    assert result["factors"]["distance"] > 0.9


def test_compute_confidence_low_label_for_weak_signal():
    result = compute_confidence(
        comps_count=5,
        tier_used=5,
        kept_ratio=0.50,
        dispersion_ratio=0.90,
        avg_distance_m=14000,
        avg_age_days=250,
        avg_similarity=0.40,
    )

    assert result["label"] == ConfidenceLevel.LOW.value
    assert 0.0 <= result["score"] < 0.50
    assert result["factors"]["distance"] < 0.1
