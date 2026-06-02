import csv
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine, text

from app.core.config import settings
from app.core.property_features import normalize_property_features, parse_feature_list

DEFAULT_CSV_PATHS = settings.LISTINGS_CSV_PATHS
DATABASE_URL = settings.DATABASE_URL


CREATE_STAGING_SQL = """
CREATE TABLE IF NOT EXISTS listings_staging (
  listing_id      TEXT,
  category        TEXT,
  price_egp       DOUBLE PRECISION,
  period          TEXT,
  property_type   TEXT,
  bedrooms        DOUBLE PRECISION,
  bathrooms       DOUBLE PRECISION,
  size_sqm        DOUBLE PRECISION,
  location_text   TEXT,
  lat             DOUBLE PRECISION,
  lng             DOUBLE PRECISION,
  area_id         BIGINT,
  scraped_at_utc  TIMESTAMPTZ,
  images_count    INTEGER,
  amenities                 JSONB DEFAULT '[]'::jsonb,
  normalized_amenities      JSONB DEFAULT '[]'::jsonb,
  unknown_amenity_codes     JSONB DEFAULT '[]'::jsonb,
  furnishing_status         TEXT,
  floor_number              SMALLINT,
  compound_name             TEXT,
  view_type                 TEXT,
  building_quality          TEXT,
  feature_raw               JSONB DEFAULT '{}'::jsonb
);

ALTER TABLE listings_staging
  ADD COLUMN IF NOT EXISTS area_id BIGINT;

ALTER TABLE listings_staging
  ADD COLUMN IF NOT EXISTS amenities JSONB DEFAULT '[]'::jsonb,
  ADD COLUMN IF NOT EXISTS normalized_amenities JSONB DEFAULT '[]'::jsonb,
  ADD COLUMN IF NOT EXISTS unknown_amenity_codes JSONB DEFAULT '[]'::jsonb,
  ADD COLUMN IF NOT EXISTS furnishing_status TEXT,
  ADD COLUMN IF NOT EXISTS floor_number SMALLINT,
  ADD COLUMN IF NOT EXISTS compound_name TEXT,
  ADD COLUMN IF NOT EXISTS view_type TEXT,
  ADD COLUMN IF NOT EXISTS building_quality TEXT,
  ADD COLUMN IF NOT EXISTS feature_raw JSONB DEFAULT '{}'::jsonb;

TRUNCATE TABLE listings_staging;
"""

ENSURE_LISTINGS_FEATURE_SQL = """
ALTER TABLE listings
  ADD COLUMN IF NOT EXISTS amenities JSONB NOT NULL DEFAULT '[]'::jsonb,
  ADD COLUMN IF NOT EXISTS normalized_amenities JSONB NOT NULL DEFAULT '[]'::jsonb,
  ADD COLUMN IF NOT EXISTS unknown_amenity_codes JSONB NOT NULL DEFAULT '[]'::jsonb,
  ADD COLUMN IF NOT EXISTS furnishing_status TEXT,
  ADD COLUMN IF NOT EXISTS floor_number SMALLINT,
  ADD COLUMN IF NOT EXISTS compound_name TEXT,
  ADD COLUMN IF NOT EXISTS view_type TEXT,
  ADD COLUMN IF NOT EXISTS building_quality TEXT,
  ADD COLUMN IF NOT EXISTS feature_raw JSONB NOT NULL DEFAULT '{}'::jsonb;
"""

INSERT_STAGING_SQL = """
INSERT INTO listings_staging (
  listing_id, category, price_egp, period, property_type,
  bedrooms, bathrooms, size_sqm, location_text,
  lat, lng, area_id, scraped_at_utc, images_count,
  amenities, normalized_amenities, unknown_amenity_codes,
  furnishing_status, floor_number, compound_name, view_type,
  building_quality, feature_raw
)
VALUES (
  :listing_id, :category, :price_egp, :period, :property_type,
  :bedrooms, :bathrooms, :size_sqm, :location_text,
  :lat, :lng, :area_id, :scraped_at_utc, :images_count,
  CAST(:amenities AS jsonb),
  CAST(:normalized_amenities AS jsonb),
  CAST(:unknown_amenity_codes AS jsonb),
  :furnishing_status,
  :floor_number,
  :compound_name,
  :view_type,
  :building_quality,
  CAST(:feature_raw AS jsonb)
);
"""

SELECT_AREA_SQL = """
SELECT area_id
FROM areas
WHERE parent_area_id IS NOT DISTINCT FROM :parent_area_id
  AND level = :level
  AND lower(name) = lower(:name)
LIMIT 1;
"""

INSERT_AREA_SQL = """
INSERT INTO areas (
  name, level, parent_area_id, center_geom, fallback_radius_m
)
VALUES (
  :name,
  :level,
  :parent_area_id,
  ST_SetSRID(ST_MakePoint(:lng, :lat), 4326),
  :fallback_radius_m
)
RETURNING area_id;
"""

UPDATE_AREA_SQL = """
UPDATE areas
SET
  center_geom = ST_SetSRID(ST_MakePoint(:lng, :lat), 4326),
  fallback_radius_m = :fallback_radius_m
WHERE area_id = :area_id
  AND (
    fallback_radius_m IS DISTINCT FROM :fallback_radius_m
    OR NOT ST_Equals(center_geom, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326))
  );
"""

UPSERT_FINAL_SQL = """
INSERT INTO listings (
  listing_id, category, period, price_egp,
  property_type, bedrooms, bathrooms, size_sqm,
  location_text, lat, lng, geom, area_id, scraped_at_utc, images_count,
  amenities, normalized_amenities, unknown_amenity_codes,
  furnishing_status, floor_number, compound_name, view_type,
  building_quality, feature_raw
)
SELECT
  s.listing_id,
  s.category,
  s.period,
  ROUND(s.price_egp)::INT AS price_egp,
  NULLIF(TRIM(s.property_type), '') AS property_type,
  CASE
    WHEN s.bedrooms IS NULL THEN NULL
    ELSE GREATEST(0, ROUND(s.bedrooms))::SMALLINT
  END AS bedrooms,
  CASE
    WHEN s.bathrooms IS NULL THEN NULL
    ELSE GREATEST(0, ROUND(s.bathrooms))::SMALLINT
  END AS bathrooms,
  CASE
    WHEN s.size_sqm IS NULL OR s.size_sqm <= 0 THEN NULL
    ELSE ROUND(s.size_sqm::numeric, 2)
  END AS size_sqm,
  s.location_text,
  s.lat,
  s.lng,
  ST_SetSRID(ST_MakePoint(s.lng, s.lat), 4326) AS geom,
  s.area_id,
  s.scraped_at_utc,
  COALESCE(s.images_count, 0)::SMALLINT,
  COALESCE(s.amenities, '[]'::jsonb),
  COALESCE(s.normalized_amenities, '[]'::jsonb),
  COALESCE(s.unknown_amenity_codes, '[]'::jsonb),
  NULLIF(TRIM(s.furnishing_status), '') AS furnishing_status,
  s.floor_number,
  NULLIF(TRIM(s.compound_name), '') AS compound_name,
  NULLIF(TRIM(s.view_type), '') AS view_type,
  NULLIF(TRIM(s.building_quality), '') AS building_quality,
  COALESCE(s.feature_raw, '{}'::jsonb)
FROM listings_staging s
WHERE
  s.listing_id IS NOT NULL
  AND s.category IS NOT NULL
  AND s.period IS NOT NULL
  AND NULLIF(TRIM(s.property_type), '') IS NOT NULL
  AND s.price_egp IS NOT NULL AND s.price_egp > 0
  AND s.area_id IS NOT NULL
  AND s.lat BETWEEN 22 AND 32
  AND s.lng BETWEEN 24 AND 37
ON CONFLICT (listing_id) DO UPDATE
SET
  category = EXCLUDED.category,
  period = EXCLUDED.period,
  price_egp = EXCLUDED.price_egp,
  property_type = EXCLUDED.property_type,
  bedrooms = EXCLUDED.bedrooms,
  bathrooms = EXCLUDED.bathrooms,
  size_sqm = EXCLUDED.size_sqm,
  location_text = EXCLUDED.location_text,
  lat = EXCLUDED.lat,
  lng = EXCLUDED.lng,
  geom = EXCLUDED.geom,
  area_id = EXCLUDED.area_id,
  scraped_at_utc = EXCLUDED.scraped_at_utc,
  images_count = EXCLUDED.images_count,
  amenities = EXCLUDED.amenities,
  normalized_amenities = EXCLUDED.normalized_amenities,
  unknown_amenity_codes = EXCLUDED.unknown_amenity_codes,
  furnishing_status = EXCLUDED.furnishing_status,
  floor_number = EXCLUDED.floor_number,
  compound_name = EXCLUDED.compound_name,
  view_type = EXCLUDED.view_type,
  building_quality = EXCLUDED.building_quality,
  feature_raw = EXCLUDED.feature_raw
WHERE (
  listings.category,
  listings.period,
  listings.price_egp,
  listings.property_type,
  listings.bedrooms,
  listings.bathrooms,
  listings.size_sqm,
  listings.location_text,
  listings.lat,
  listings.lng,
  listings.area_id,
  listings.scraped_at_utc,
  listings.images_count,
  listings.amenities,
  listings.normalized_amenities,
  listings.unknown_amenity_codes,
  listings.furnishing_status,
  listings.floor_number,
  listings.compound_name,
  listings.view_type,
  listings.building_quality,
  listings.feature_raw
) IS DISTINCT FROM (
  EXCLUDED.category,
  EXCLUDED.period,
  EXCLUDED.price_egp,
  EXCLUDED.property_type,
  EXCLUDED.bedrooms,
  EXCLUDED.bathrooms,
  EXCLUDED.size_sqm,
  EXCLUDED.location_text,
  EXCLUDED.lat,
  EXCLUDED.lng,
  EXCLUDED.area_id,
  EXCLUDED.scraped_at_utc,
  EXCLUDED.images_count,
  EXCLUDED.amenities,
  EXCLUDED.normalized_amenities,
  EXCLUDED.unknown_amenity_codes,
  EXCLUDED.furnishing_status,
  EXCLUDED.floor_number,
  EXCLUDED.compound_name,
  EXCLUDED.view_type,
  EXCLUDED.building_quality,
  EXCLUDED.feature_raw
);
"""

QC_SQL = """
SELECT COUNT(*) AS listings_count FROM listings;
SELECT category, period, COUNT(*) AS cnt FROM listings GROUP BY category, period ORDER BY category, period;
SELECT COUNT(*) AS areas_count FROM areas;
SELECT level, COUNT(*) AS cnt FROM areas GROUP BY level ORDER BY level;
SELECT COUNT(*) AS orphan_area_refs
FROM listings l
LEFT JOIN areas a ON l.area_id = a.area_id
WHERE a.area_id IS NULL;
"""


def parse_float(x):
    if x is None:
        return None
    x = str(x).strip()
    if x == "" or x.lower() == "null":
        return None
    try:
        return float(x)
    except ValueError:
        return None


def parse_text(x):
    if x is None:
        return None
    x = str(x).strip()
    return x if x else None


def parse_ts(x):
    if x is None:
        return None
    x = str(x).strip()
    if x == "" or x.lower() == "null":
        return None
    try:
        return datetime.fromisoformat(x.replace("Z", "+00:00"))
    except ValueError:
        return None


def configured_csv_paths():
    return DEFAULT_CSV_PATHS


def normalize_area_name(value):
    return re.sub(r"\s+", " ", value.strip())


def location_parts(location_text):
    if not location_text:
        return []
    return [
        normalize_area_name(part)
        for part in location_text.split(",")
        if normalize_area_name(part)
    ]


def level_for_path_length(path_length):
    return min(path_length, 4)


def fallback_radius_for_level(level):
    return {
        1: settings.AREA_LEVEL1_FALLBACK_RADIUS_M,
        2: settings.AREA_LEVEL2_FALLBACK_RADIUS_M,
        3: settings.AREA_LEVEL3_FALLBACK_RADIUS_M,
        4: settings.AREA_LEVEL4_FALLBACK_RADIUS_M,
    }[level]


def top_down_path(parts):
    return tuple(reversed(parts))


def row_value(row, *keys):
    for key in keys:
        if key in row and parse_text(row.get(key)) is not None:
            return row.get(key)
    return None


def normalize_period_value(category, value):
    period = parse_text(value)
    if period:
        return period
    category_text = (category or "").casefold()
    if "rent" in category_text:
        return "monthly"
    if "buy" in category_text or "sale" in category_text:
        return "sale"
    return None


def parse_images_count(row):
    explicit = parse_float(row_value(row, "images_count"))
    if explicit is not None:
        return int(explicit)
    return len(parse_feature_list(row.get("images")))


def json_param(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def read_rows(paths):
    rows = []
    skipped = defaultdict(int)
    area_stats = {}

    for path in paths:
        if not Path(path).exists():
            skipped[f"missing_file:{path}"] += 1
            continue

        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames:
                reader.fieldnames = [fn.strip().lstrip("\ufeff") for fn in reader.fieldnames]

            if not reader.fieldnames:
                skipped[f"empty_file:{path}"] += 1
                continue

            for row in reader:
                listing_id = parse_text(row_value(row, "listing_id", "id", "property_id"))
                category = parse_text(row_value(row, "category"))
                period = normalize_period_value(category, row_value(row, "period", "price_period"))
                price_egp = parse_float(row_value(row, "price_egp", "price", "price_raw_value"))
                property_type = parse_text(row_value(row, "property_type"))
                lat = parse_float(row_value(row, "lat", "latitude"))
                lng = parse_float(row_value(row, "lng", "longitude"))
                scraped_at_utc = parse_ts(row_value(row, "scraped_at_utc", "listed_date"))
                location_text = parse_text(row_value(row, "location_text", "location"))
                parts = location_parts(location_text)

                if not listing_id:
                    skipped["missing_listing_id"] += 1
                    continue
                if not category or not period or not property_type:
                    skipped["missing_classification"] += 1
                    continue
                if price_egp is None or price_egp <= 0:
                    skipped["invalid_price"] += 1
                    continue
                if lat is None or lng is None or not (22 <= lat <= 32) or not (24 <= lng <= 37):
                    skipped["invalid_coordinates"] += 1
                    continue
                if not scraped_at_utc:
                    skipped["missing_scraped_at_utc"] += 1
                    continue
                if not parts:
                    skipped["missing_location_text"] += 1
                    continue

                path_key = top_down_path(parts)
                for i in range(1, len(path_key) + 1):
                    prefix = path_key[:i]
                    stats = area_stats.setdefault(
                        prefix,
                        {"name": prefix[-1], "lat_sum": 0.0, "lng_sum": 0.0, "count": 0},
                    )
                    stats["lat_sum"] += lat
                    stats["lng_sum"] += lng
                    stats["count"] += 1

                features = normalize_property_features(
                    {
                        "amenities": row.get("amenities"),
                        "furnishing_status": row_value(row, "furnishing_status", "furnishing", "furnished"),
                        "floor_number": row_value(row, "floor_number", "floor", "floor_level"),
                        "compound_name": row_value(row, "compound_name", "compound", "project_name"),
                        "view_type": row_value(row, "view_type", "view"),
                        "building_quality": row_value(row, "building_quality", "quality", "finishing"),
                        "location_text": location_text,
                    }
                )
                rows.append(
                    {
                        "listing_id": listing_id,
                        "category": category,
                        "price_egp": price_egp,
                        "period": period,
                        "property_type": property_type,
                        "bedrooms": parse_float(row_value(row, "bedrooms")),
                        "bathrooms": parse_float(row_value(row, "bathrooms")),
                        "size_sqm": parse_float(row_value(row, "size_sqm", "size", "size_sqm_reported")),
                        "location_text": location_text,
                        "lat": lat,
                        "lng": lng,
                        "area_key": path_key,
                        "scraped_at_utc": scraped_at_utc,
                        "images_count": parse_images_count(row),
                        "amenities": json_param(features["amenities"]),
                        "normalized_amenities": json_param(features["normalized_amenities"]),
                        "unknown_amenity_codes": json_param(features["unknown_amenity_codes"]),
                        "furnishing_status": features["furnishing_status"],
                        "floor_number": features["floor_number"],
                        "compound_name": features["compound_name"],
                        "view_type": features["view_type"],
                        "building_quality": features["building_quality"],
                        "feature_raw": json_param(features["feature_raw"]),
                    }
                )

    return rows, skipped, area_stats


def upsert_areas(conn, area_stats):
    area_ids = {}

    for path_key in sorted(area_stats, key=len):
        stats = area_stats[path_key]
        parent_key = path_key[:-1]
        parent_id = area_ids.get(parent_key)
        level = level_for_path_length(len(path_key))
        lat = stats["lat_sum"] / stats["count"]
        lng = stats["lng_sum"] / stats["count"]
        params = {
            "name": stats["name"],
            "level": level,
            "parent_area_id": parent_id,
            "lat": lat,
            "lng": lng,
            "fallback_radius_m": fallback_radius_for_level(level),
        }

        row = conn.execute(text(SELECT_AREA_SQL), params).mappings().first()
        if row:
            area_id = row["area_id"]
            conn.execute(text(UPDATE_AREA_SQL), {**params, "area_id": area_id})
        else:
            area_id = conn.execute(text(INSERT_AREA_SQL), params).scalar_one()

        area_ids[path_key] = area_id

    return area_ids


def insert_staging(conn, rows, area_ids, chunk_size=None):
    chunk_size = settings.CSV_INSERT_CHUNK_SIZE if chunk_size is None else chunk_size
    batch = []
    for row in rows:
        payload = {k: v for k, v in row.items() if k != "area_key"}
        payload["area_id"] = area_ids[row["area_key"]]
        batch.append(payload)

        if len(batch) >= chunk_size:
            conn.execute(text(INSERT_STAGING_SQL), batch)
            batch.clear()

    if batch:
        conn.execute(text(INSERT_STAGING_SQL), batch)


def main():
    paths = configured_csv_paths()
    rows, skipped, area_stats = read_rows(paths)

    if not rows:
        print("ERROR: No valid listing rows found.")
        print(f"CSV paths checked: {paths}")
        print(f"Skipped: {dict(skipped)}")
        sys.exit(1)

    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    with engine.begin() as conn:
        conn.execute(text(ENSURE_LISTINGS_FEATURE_SQL))
        conn.execute(text(CREATE_STAGING_SQL))
        area_ids = upsert_areas(conn, area_stats)
        insert_staging(conn, rows, area_ids)
        conn.execute(text(UPSERT_FINAL_SQL))

        print(f"Loaded staging rows: {len(rows)}")
        print(f"Upserted area nodes: {len(area_ids)}")
        print(f"Skipped rows: {dict(skipped)}")

        for stmt in QC_SQL.strip().split(";"):
            stmt = stmt.strip()
            if not stmt:
                continue
            res = conn.execute(text(stmt))
            rows_out = res.fetchall()
            print(f"\n--- QC: {stmt[:80]} ---")
            for r in rows_out[:25]:
                print(dict(r._mapping))

    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        conn.execute(text("VACUUM (ANALYZE) areas"))
        conn.execute(text("VACUUM (ANALYZE) listings"))

    print("\nPlanner statistics refreshed.")
    print("\nDONE")


if __name__ == "__main__":
    main()
