from app.services.valuation_service import _combine_confidence


def test_final_confidence_is_capped_by_location_resolution_dimension():
    evidence = {
        "score": 0.92,
        "label": "High",
        "factors": {"count": 1.0, "tier": 1.0},
    }
    city_level_location = {
        "score": 0.40,
        "source": "GOOGLE_MAPS",
        "precision_level": "CITY",
        "ambiguity_status": "UNAMBIGUOUS",
    }

    combined = _combine_confidence(evidence, city_level_location)

    assert combined["score"] == 0.40
    assert combined["label"] == "Low"
    assert combined["dimensions"]["valuation_evidence"]["score"] == 0.92
    assert combined["dimensions"]["location_resolution"]["score"] == 0.40
