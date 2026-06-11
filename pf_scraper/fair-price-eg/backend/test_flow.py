import os

import pytest
from sqlalchemy import text

from app.geo.spatial_authority import extract_candidate_tokens, haversine_distance

pytestmark = pytest.mark.integration

SQL = """
WITH matches AS (
  SELECT
    e.entity_id,
    e.entity_type,
    e.canonical_name,
    e.normalized_name,
    e.canonical_area_id,
    e.centroid_lat,
    e.centroid_lng,
    e.authority_source,
    e.version,
    a.priority,
    a.normalized_alias,
    ar.level AS area_level
  FROM location_aliases a
  JOIN location_entities e ON e.entity_id = a.entity_id
  LEFT JOIN areas ar ON ar.area_id = e.canonical_area_id
  WHERE a.normalized_alias = ANY(:candidate_aliases)
    AND a.active = TRUE

  UNION ALL

  SELECT
    'area_' || ar.area_id::text AS entity_id,
    CASE
      WHEN ar.level = 4 THEN 'compound'
      WHEN ar.level = 3 THEN 'district'
      WHEN ar.level = 2 THEN 'city'
      WHEN ar.level = 1 THEN 'governorate'
      ELSE 'neighborhood'
    END AS entity_type,
    ar.name AS canonical_name,
    lower(ar.name) AS normalized_name,
    ar.area_id AS canonical_area_id,
    ST_Y(ar.center_geom::geometry) AS centroid_lat,
    ST_X(ar.center_geom::geometry) AS centroid_lng,
    'VALORAI_AREAS_FALLBACK' AS authority_source,
    '1.0' AS version,
    0 AS priority,
    lower(ar.name) AS normalized_alias,
    ar.level AS area_level
  FROM areas ar
  WHERE lower(ar.name) = ANY(:candidate_aliases)
)
SELECT DISTINCT * FROM matches
ORDER BY priority DESC, entity_type ASC, entity_id ASC;
"""

def _type_rank(entity):
    ranks = {
        "compound": 1,
        "landmark": 2,
        "neighborhood": 3,
        "district": 4,
        "city": 5,
        "governorate": 6,
        "region": 7,
        "state": 8,
        "province": 9,
        "country": 10,
    }
    entity_type = entity.get("entity_type")
    primary_rank = ranks.get(str(entity_type).casefold() if entity_type else "", 99)

    level = entity.get("area_level")
    if primary_rank == 99 and level is not None:
        level = int(level)
        if level == 4:
            primary_rank = 1
        elif level == 3:
            primary_rank = 3
        elif level == 2:
            primary_rank = 5
        elif level == 1:
            primary_rank = 6
    secondary_rank = (10 - int(level)) if level is not None else 99
    return (primary_rank, secondary_rank)


def _select_candidate(matched_entities):
    matched_entities.sort(key=lambda entity: (_type_rank(entity), -entity.get("priority", 0)))
    top_rank = _type_rank(matched_entities[0])
    top_entities = [entity for entity in matched_entities if _type_rank(entity) == top_rank]

    if len(top_entities) > 1 and len(matched_entities) > len(top_entities):
        parents = [entity for entity in matched_entities if _type_rank(entity) > top_rank]
        for potential_candidate in top_entities:
            is_valid = True
            for parent in parents:
                dist = haversine_distance(
                    potential_candidate["centroid_lat"],
                    potential_candidate["centroid_lng"],
                    parent["centroid_lat"],
                    parent["centroid_lng"],
                )
                if dist > 30000:
                    is_valid = False
                    break
            if is_valid:
                return potential_candidate
        return None

    if len(top_entities) > 1:
        return None
    return top_entities[0]


def test_location_authority_flow_selects_consistent_villette_candidate():
    if os.environ.get("RUN_POSTGIS_INTEGRATION") != "1":
        pytest.skip("Set RUN_POSTGIS_INTEGRATION=1 with a seeded PostGIS database to run.")

    from app.db.session import SessionLocal

    db = SessionLocal()
    try:
        candidates = extract_candidate_tokens("Villette, 5th Settlement Compounds")
        rows = [dict(row) for row in db.execute(text(SQL), {"candidate_aliases": list(candidates)}).mappings().all()]
    finally:
        db.close()

    entities_by_id = {}
    for row in rows:
        entity_id = str(row["entity_id"])
        if entity_id not in entities_by_id:
            entities_by_id[entity_id] = row

    matched_entities = list(entities_by_id.values())
    assert matched_entities

    candidate = _select_candidate(matched_entities)
    assert candidate is not None

    for other in matched_entities:
        if other["entity_id"] == candidate["entity_id"]:
            continue
        dist = haversine_distance(
            candidate["centroid_lat"],
            candidate["centroid_lng"],
            other["centroid_lat"],
            other["centroid_lng"],
        )
        assert dist <= 30000
