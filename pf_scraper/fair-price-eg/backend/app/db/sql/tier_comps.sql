-- Deterministic hierarchy-aware comparable retrieval.
-- Scope is supplied by the tier settings:
-- same_area, same_district, nearby_districts, same_city, same_governorate.

WITH RECURSIVE
target AS (
  SELECT
    ST_SetSRID(ST_MakePoint(:lng, :lat), 4326) AS geom,
    ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography AS geog
),
target_area AS (
  SELECT area_id, name, level, parent_area_id
  FROM areas
  WHERE area_id = :area_id
),
target_ancestors AS (
  SELECT area_id, name, level, parent_area_id
  FROM target_area

  UNION ALL

  SELECT parent.area_id, parent.name, parent.level, parent.parent_area_id
  FROM areas parent
  JOIN target_ancestors child ON child.parent_area_id = parent.area_id
),
target_hierarchy AS (
  SELECT
    :area_id AS requested_area_id,
    MAX(area_id) FILTER (WHERE level = 1) AS governorate_id,
    MAX(area_id) FILTER (WHERE level = 2) AS city_id,
    MAX(area_id) FILTER (WHERE level = 3) AS district_id,
    MAX(area_id) FILTER (WHERE level = 4) AS leaf_id
  FROM target_ancestors
),
scope_root AS (
  SELECT
    CASE :scope
      WHEN 'same_area' THEN requested_area_id
      WHEN 'same_district' THEN COALESCE(district_id, requested_area_id)
      WHEN 'nearby_districts' THEN COALESCE(city_id, governorate_id, requested_area_id)
      WHEN 'same_city' THEN COALESCE(city_id, requested_area_id)
      WHEN 'same_governorate' THEN COALESCE(governorate_id, requested_area_id)
      ELSE requested_area_id
    END AS root_area_id,
    district_id
  FROM target_hierarchy
),
scope_areas(area_id) AS (
  SELECT root_area_id
  FROM scope_root
  WHERE root_area_id IS NOT NULL

  UNION ALL

  SELECT child.area_id
  FROM areas child
  JOIN scope_areas parent ON child.parent_area_id = parent.area_id
),
same_district_areas(area_id) AS (
  SELECT district_id
  FROM scope_root
  WHERE district_id IS NOT NULL

  UNION ALL

  SELECT child.area_id
  FROM areas child
  JOIN same_district_areas parent ON child.parent_area_id = parent.area_id
)
SELECT
  l.listing_id,
  l.price_egp,
  l.size_sqm,
  l.property_type,
  l.bedrooms,
  l.bathrooms,
  l.area_id,
  area.name AS area_name,
  area.level AS area_level,
  l.location_text,
  l.lat,
  l.lng,
  l.images_count,
  l.amenities,
  l.normalized_amenities,
  l.unknown_amenity_codes,
  l.furnishing_status,
  l.floor_number,
  l.compound_name,
  l.view_type,
  l.building_quality,
  CAST(:tier AS TEXT) AS reason_code,
  CAST(:tier_number AS INTEGER) AS retrieval_tier,
  CAST(:tier_label AS TEXT) AS tier_label,
  CAST(:radius_m AS INTEGER) AS radius_m,
  l.area_id = :area_id AS is_same_area,
  ST_Distance(l.geom::geography, target.geog) AS dist_m,
  GREATEST(EXTRACT(EPOCH FROM (:as_of_utc - l.scraped_at_utc)) / 86400.0, 0) AS age_days
FROM listings l
JOIN areas area ON area.area_id = l.area_id
CROSS JOIN target
WHERE
  l.category = :listing_category
  AND l.period = :listing_period
  AND l.area_id IN (SELECT area_id FROM scope_areas)
  AND (
    :scope <> 'nearby_districts'
    OR l.area_id NOT IN (SELECT area_id FROM same_district_areas)
  )
  AND l.property_type = :property_type
  AND l.bedrooms IS NOT DISTINCT FROM CAST(:bedrooms AS INTEGER)
  AND (CAST(:bathrooms AS INTEGER) IS NULL OR l.bathrooms IS NULL OR l.bathrooms = CAST(:bathrooms AS INTEGER))
  AND l.size_sqm BETWEEN (:size_sqm * :size_low) AND (:size_sqm * :size_high)
  AND l.scraped_at_utc >= (:as_of_utc - (:stale_days * INTERVAL '1 day'))
  AND l.price_egp BETWEEN :min_price_egp AND :max_price_egp
  AND l.size_sqm > 0
  AND l.size_sqm <= :max_size_sqm
  AND (l.price_egp / NULLIF(l.size_sqm, 0)) BETWEEN :min_price_per_sqm AND :max_price_per_sqm
  AND ST_DWithin(l.geom::geography, target.geog, :radius_m)
ORDER BY
  dist_m ASC,
  l.scraped_at_utc DESC,
  l.price_egp ASC,
  l.listing_id ASC
LIMIT :limit;
