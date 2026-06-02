import sys
sys.path.insert(0, r"c:\Users\mh978\Downloads\mobile computing project\pf_scraper\fair-price-eg\backend")
from app.db.session import SessionLocal
from sqlalchemy import text
from app.geo.spatial_authority import extract_candidate_tokens

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

db = SessionLocal()
try:
    candidates = extract_candidate_tokens("Villette, 5th Settlement Compounds")
    print("Candidates:", list(candidates))
    rows = db.execute(text(SQL), {"candidate_aliases": list(candidates)}).mappings().all()
    for r in rows:
        print(dict(r))
finally:
    db.close()
