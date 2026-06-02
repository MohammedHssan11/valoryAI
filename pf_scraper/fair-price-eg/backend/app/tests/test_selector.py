from datetime import datetime, timezone

from app.comps.selector import fetch_comps


class FakeResult:
    def __init__(self, rows=None, first_row=None):
        self.rows = rows or []
        self.first_row = first_row

    def mappings(self):
        return self

    def all(self):
        return self.rows

    def first(self):
        return self.first_row


class FakeDB:
    def __init__(self, counts):
        self.counts = counts
        self.calls = []

    def execute(self, statement, params=None):
        if params is None or "scope" not in params:
            return FakeResult(first_row={"as_of_utc": datetime(2026, 1, 1, tzinfo=timezone.utc)})

        self.calls.append(dict(params))
        count = self.counts.get((params["scope"], params["radius_m"]), 0)
        rows = [
            {
                "listing_id": f"{params['scope']}-{params['radius_m']}-{i:03d}",
                "price_egp": 10000,
                "size_sqm": 100,
                "property_type": params["property_type"],
                "bedrooms": params["bedrooms"],
                "bathrooms": params["bathrooms"],
                "dist_m": 100,
                "age_days": 10,
            }
            for i in range(count)
        ]
        return FakeResult(rows=rows)


def base_params():
    return {
        "lat": 30.0,
        "lng": 31.0,
        "area_id": 1,
        "property_type": "Apartment",
        "bedrooms": 2,
        "bathrooms": 2,
        "size_sqm": 120,
    }


def test_fetch_comps_uses_deterministic_radius_progression_and_tier_stop():
    db = FakeDB({("same_district", 2000): 45})

    rows, tier, trace = fetch_comps(db, base_params(), include_trace=True)

    assert tier == 2
    assert len(rows) == 45
    assert [(call["scope"], call["radius_m"]) for call in db.calls] == [
        ("same_area", 500),
        ("same_area", 1000),
        ("same_district", 2000),
    ]
    assert trace[-1]["reason_code"] == "SAME_DISTRICT_MATCH"
    assert trace[-1]["selected"] is True
    assert [entry["attempt_index"] for entry in trace] == [1, 2, 3]
    assert trace[0]["status"] == "below_threshold"


def test_fetch_comps_returns_best_deterministic_fallback_when_threshold_not_met():
    db = FakeDB({
        ("same_area", 500): 9,
        ("same_area", 1000): 9,
        ("same_district", 2000): 6,
        ("nearby_districts", 5000): 3,
    })

    rows, tier, trace = fetch_comps(db, base_params(), include_trace=True)

    assert tier == 1
    assert len(rows) == 9
    assert len(trace) == 6
    assert trace[0]["selected"] is True
    assert trace[0]["status"] == "selected"


def test_fetch_comps_does_not_randomly_fallback_without_area():
    db = FakeDB({})

    rows, tier, trace = fetch_comps(db, {**base_params(), "area_id": None}, include_trace=True)

    assert rows == []
    assert tier == 5
    assert trace[0]["reason_code"] == "AREA_UNRESOLVED"
    assert trace[0]["status"] == "blocked"
    assert db.calls == []
