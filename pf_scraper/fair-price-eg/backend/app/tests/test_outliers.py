from app.pricing.filters import mad_filter


def test_mad_filter_removes_price_per_sqm_outlier_before_weighting():
    comps = [
        {"listing_id": f"normal-{i}", "price_egp": 10000, "size_sqm": 100}
        for i in range(10)
    ]
    comps.append({"listing_id": "outlier", "price_egp": 100000, "size_sqm": 100})

    filtered, stats = mad_filter(comps)

    assert stats["metric"] == "price_per_sqm"
    assert stats["removed"] == 1
    assert [comp["listing_id"] for comp in filtered] == [f"normal-{i}" for i in range(10)]
