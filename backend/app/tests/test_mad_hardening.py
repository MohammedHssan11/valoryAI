from app.pricing.filters import mad_filter


def test_zero_mad_uses_tolerance_and_removes_anomaly_consistently():
    comps = [{"listing_id": f"stable-{index}", "price_egp": 10000, "size_sqm": 100} for index in range(10)]
    comps.append({"listing_id": "outside-tolerance", "price_egp": 10600, "size_sqm": 100})

    filtered, stats = mad_filter(comps)

    assert stats["reason"] == "zero_mad_tolerance"
    assert stats["mad"] == 0
    assert stats["removed"] == 1
    assert [comp["listing_id"] for comp in filtered] == [f"stable-{index}" for index in range(10)]


def test_mad_filter_does_not_filter_low_sample_sizes():
    comps = [{"listing_id": f"small-{index}", "price_egp": 10000 + index, "size_sqm": 100} for index in range(4)]

    filtered, stats = mad_filter(comps)

    assert filtered == comps
    assert stats["reason"] == "sample_too_small"
    assert stats["removed"] == 0


def test_mad_filter_falls_back_to_price_when_price_per_sqm_is_unavailable():
    comps = [{"listing_id": f"normal-{index}", "price_egp": 10000} for index in range(10)]
    comps.append({"listing_id": "price-outlier", "price_egp": 100000})

    filtered, stats = mad_filter(comps)

    assert stats["metric"] == "price"
    assert stats["removed"] == 1
    assert [comp["listing_id"] for comp in filtered] == [f"normal-{index}" for index in range(10)]
