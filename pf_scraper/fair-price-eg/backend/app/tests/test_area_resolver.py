from app.geo.area_resolver import nearest_area


class FakeResult:
    def __init__(self, rows):
        self.rows = rows

    def mappings(self):
        return self

    def all(self):
        return self.rows


class FakeDb:
    def __init__(self, result_sets):
        self.result_sets = list(result_sets)

    def execute(self, *_args, **_kwargs):
        return FakeResult(self.result_sets.pop(0))


def test_polygon_containment_wins_before_nearest_fallback():
    db = FakeDb(
        [
            [{"area_id": 4, "name": "Fifth Settlement", "level": 4, "parent_area_id": 3, "dist_m": 0, "resolution_strategy": "POLYGON_CONTAINMENT"}],
        ]
    )

    area = nearest_area(db, 30.0, 31.4)

    assert area["area_id"] == 4
    assert area["resolution_strategy"] == "POLYGON_CONTAINMENT"
    assert area["ambiguity_status"] == "UNAMBIGUOUS"


def test_polygon_containment_rejects_same_level_ambiguity():
    db = FakeDb(
        [
            [
                {"area_id": 4, "name": "A", "level": 4, "parent_area_id": 3, "dist_m": 0, "resolution_strategy": "POLYGON_CONTAINMENT"},
                {"area_id": 5, "name": "B", "level": 4, "parent_area_id": 3, "dist_m": 0, "resolution_strategy": "POLYGON_CONTAINMENT"},
            ],
        ]
    )

    area = nearest_area(db, 30.0, 31.4)

    assert area["ambiguity_status"] == "AMBIGUOUS_CONTAINMENT"
    assert len(area["candidates"]) == 2


def test_nearest_fallback_rejects_distance_ties():
    db = FakeDb(
        [
            [],
            [
                {"area_id": 4, "name": "A", "level": 4, "parent_area_id": 3, "dist_m": 100.0},
                {"area_id": 5, "name": "B", "level": 4, "parent_area_id": 3, "dist_m": 110.0},
            ],
        ]
    )

    area = nearest_area(db, 30.0, 31.4)

    assert area["ambiguity_status"] == "AMBIGUOUS_NEAREST_AREA"
