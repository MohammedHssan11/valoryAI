from unittest.mock import patch

import pytest

from app.geo.address_resolver import ResolvedLocation, resolve_address, resolve_canonical_entity


class FakeResult:
    def __init__(self, first=None, all_rows=None):
        self._first = first
        self._all = all_rows if all_rows is not None else ([] if first is None else [first])

    def mappings(self):
        return self

    def first(self):
        return self._first

    def all(self):
        return self._all


class FakeDb:
    def __init__(self, results):
        self.results = list(results)
        self.committed = False
        self.rolled_back = False

    def execute(self, *_args, **_kwargs):
        if self.results:
            return self.results.pop(0)
        return FakeResult()

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True


def test_resolve_address_cache_hit_uses_normalized_governed_cache():
    db = FakeDb(
        [
            FakeResult(
                first={
                    "lat": 30.0,
                    "lng": 31.0,
                    "precision_level": "COMPOUND",
                    "matched_name": "Madinaty",
                    "source": "CANONICAL_ENTITY",
                    "normalized_input": "مدينتي",
                    "confidence": 0.92,
                    "ambiguity_status": "UNAMBIGUOUS",
                    "resolver_version": "3A.1b.1",
                    "resolution_strategy": "CANONICAL_ALIAS_MATCH",
                    "area_distance_m": None,
                    "matched_entity": {"entity_id": "eg.compound.madinaty"},
                    "source_metadata": {},
                }
            )
        ]
    )

    loc = resolve_address(db, "Madinty")

    assert loc.cache_hit is True
    assert loc.normalized_input == "مدينتي"
    assert loc.confidence == 0.92
    assert loc.matched_entity["entity_id"] == "eg.compound.madinaty"


def test_resolve_address_uses_canonical_entity_alias_before_external_geocoder():
    entity = {
        "entity_id": "eg.compound.madinaty",
        "entity_type": "compound",
        "canonical_name": "Madinaty",
        "normalized_name": "مدينتي",
        "canonical_area_id": None,
        "centroid_lat": 30.082,
        "centroid_lng": 31.638,
        "authority_source": "VALORAI_STATIC_GAZETTEER",
        "version": "3A.1b.1",
        "priority": 100,
    }
    db = FakeDb([FakeResult(), FakeResult(all_rows=[entity]), FakeResult()])

    with patch("app.geo.address_resolver._geocode_google_maps") as geocode:
        loc = resolve_address(db, "Madinaty")

    assert loc.source == "CANONICAL_ENTITY"
    assert loc.precision_level == "COMPOUND"
    assert loc.normalized_input == "مدينتي"
    assert loc.cache_hit is False
    geocode.assert_not_called()


def test_resolve_address_rejects_ambiguous_alias():
    rows = [
        {
            "entity_id": "eg.city.new_cairo",
            "entity_type": "city",
            "canonical_name": "New Cairo",
            "centroid_lat": 30.0,
            "centroid_lng": 31.4,
        },
        {
            "entity_id": "eg.city.other_cairo",
            "entity_type": "city",
            "canonical_name": "Other Cairo",
            "centroid_lat": 30.1,
            "centroid_lng": 31.5,
        },
    ]
    db = FakeDb([FakeResult(), FakeResult(all_rows=rows)])

    with pytest.raises(ValueError, match="Ambiguous address alias"):
        resolve_address(db, "tagamoa")


def test_resolve_address_hierarchical_success():
    # Villette in New Cairo. Distance is small.
    rows = [
        {
            "entity_id": "eg.compound.villette",
            "entity_type": "compound",
            "canonical_name": "Villette",
            "centroid_lat": 30.02,
            "centroid_lng": 31.48,
        },
        {
            "entity_id": "eg.district.fifth_settlement",
            "entity_type": "district",
            "canonical_name": "Fifth Settlement",
            "centroid_lat": 30.01,
            "centroid_lng": 31.45,
        },
    ]
    db = FakeDb([FakeResult(), FakeResult(all_rows=rows)])

    with patch("app.geo.address_resolver._geocode_google_maps") as geocode:
        loc = resolve_address(db, "Villette, 5th Settlement")

    assert loc.source == "CANONICAL_ENTITY"
    assert loc.matched_entity["entity_id"] == "eg.compound.villette"
    assert loc.resolution_strategy == "HIERARCHICAL_CANONICAL_MATCH"
    assert "eg.district.fifth_settlement" in loc.source_metadata["matched_entities"]
    geocode.assert_not_called()


def test_resolve_address_hierarchical_conflict():
    # Villette (New Cairo) and Sheikh Zayed (Giza). Distance > 30km.
    rows = [
        {
            "entity_id": "eg.compound.villette",
            "entity_type": "compound",
            "canonical_name": "Villette",
            "centroid_lat": 30.02, # New Cairo
            "centroid_lng": 31.48,
        },
        {
            "entity_id": "eg.city.sheikh_zayed",
            "entity_type": "city",
            "canonical_name": "Sheikh Zayed",
            "centroid_lat": 30.01, # Sheikh Zayed (west of Cairo)
            "centroid_lng": 30.97,
        },
    ]
    db = FakeDb([FakeResult(), FakeResult(all_rows=rows)])

    with pytest.raises(ValueError, match="Ambiguous address alias: conflicting hierarchy"):
        resolve_address(db, "Villette, Sheikh Zayed")


@patch("app.geo.address_resolver._geocode_google_maps")
def test_resolve_address_google_maps_fallback_is_versioned(mock_geocode):
    db = FakeDb([FakeResult(), FakeResult(all_rows=[]), FakeResult(all_rows=[]), FakeResult()])
    mock_geocode.return_value = ResolvedLocation(
        lat=30.2,
        lng=31.2,
        precision_level="CITY",
        matched_name="Cairo",
        source="GOOGLE_MAPS",
        normalized_input="cairo",
        confidence=0.40,
        resolution_strategy="EXTERNAL_GEOCODER_SINGLE_RESULT",
    )

    loc = resolve_address(db, "Cairo")

    assert loc.source == "GOOGLE_MAPS"
    assert loc.resolver_version == "3A.1b.1"
    assert loc.confidence == 0.40


def test_resolve_canonical_entity_by_id():
    entity = {
        "entity_id": "eg.city.sheikh_zayed",
        "entity_type": "city",
        "canonical_name": "Sheikh Zayed",
        "normalized_name": "الشيخ زايد",
        "canonical_area_id": None,
        "centroid_lat": 30.0131,
        "centroid_lng": 30.9764,
        "authority_source": "VALORAI_STATIC_GAZETTEER",
        "version": "3A.1b.1",
    }
    db = FakeDb([FakeResult(first=entity)])

    loc = resolve_canonical_entity(db, "eg.city.sheikh_zayed")

    assert loc.source == "CANONICAL_ENTITY"
    assert loc.resolution_strategy == "CANONICAL_ENTITY_ID"
    assert loc.precision_level == "CITY"


def test_resolve_address_broad_parent_cannot_override_compound():
    rows = [
        {
            "entity_id": "eg.compound.villette",
            "entity_type": "compound",
            "canonical_name": "Villette",
            "centroid_lat": 30.02,
            "centroid_lng": 31.48,
            "area_level": 4,
        },
        {
            "entity_id": "eg.city.new_cairo",
            "entity_type": "city",
            "canonical_name": "New Cairo City",
            "centroid_lat": 30.03,
            "centroid_lng": 31.47,
            "area_level": 2,
        },
        {
            "entity_id": "eg.governorate.cairo",
            "entity_type": "governorate",
            "canonical_name": "Cairo",
            "centroid_lat": 30.04,
            "centroid_lng": 31.23,
            "area_level": 1,
        },
    ]
    db = FakeDb([FakeResult(), FakeResult(all_rows=rows)])

    with patch("app.geo.address_resolver._geocode_google_maps") as geocode:
        loc = resolve_address(db, "Villette, The 5th Settlement, New Cairo City")

    assert loc.source == "CANONICAL_ENTITY"
    assert loc.matched_entity["entity_id"] == "eg.compound.villette"
    geocode.assert_not_called()


def test_resolve_address_unknown_broad_entity_does_not_escalate():
    rows = [
        {
            "entity_id": "eg.compound.villette",
            "entity_type": "compound",
            "canonical_name": "Villette",
            "centroid_lat": 30.02,
            "centroid_lng": 31.48,
            "area_level": 4,
        },
        {
            "entity_id": "eg.unknown.broad_region",
            "entity_type": "unknown_type",
            "canonical_name": "Broad Region",
            "centroid_lat": 30.04,
            "centroid_lng": 31.23,
            "area_level": 1,  # Broad area level
        },
    ]
    db = FakeDb([FakeResult(), FakeResult(all_rows=rows)])

    with patch("app.geo.address_resolver._geocode_google_maps") as geocode:
        loc = resolve_address(db, "Villette Broad Region")

    assert loc.source == "CANONICAL_ENTITY"
    # Specific compound should win against unclassified broad region (level 1)
    assert loc.matched_entity["entity_id"] == "eg.compound.villette"
    geocode.assert_not_called()


def test_resolve_address_valid_unknown_compounds_preserved():
    rows = [
        {
            "entity_id": "eg.unclassified.new_compound",
            "entity_type": None,  # Unknown type
            "canonical_name": "New Secret Compound",
            "centroid_lat": 30.02,
            "centroid_lng": 31.48,
            "area_level": 4,  # Highly specific level
        },
        {
            "entity_id": "eg.city.new_cairo",
            "entity_type": "city",
            "canonical_name": "New Cairo City",
            "centroid_lat": 30.03,
            "centroid_lng": 31.47,
            "area_level": 2,
        },
    ]
    db = FakeDb([FakeResult(), FakeResult(all_rows=rows)])

    with patch("app.geo.address_resolver._geocode_google_maps") as geocode:
        loc = resolve_address(db, "New Secret Compound New Cairo City")

    assert loc.source == "CANONICAL_ENTITY"
    # The unclassified specific compound (level 4) should beat the city
    assert loc.matched_entity["entity_id"] == "eg.unclassified.new_compound"
    geocode.assert_not_called()

