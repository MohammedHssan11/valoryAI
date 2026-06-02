CREATE EXTENSION IF NOT EXISTS postgis;


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

CREATE TABLE IF NOT EXISTS listings (
  listing_id      TEXT PRIMARY KEY,
  category        TEXT NOT NULL,
  period          TEXT NOT NULL,
  price_egp       INTEGER NOT NULL CHECK (price_egp > 0),

  property_type   TEXT NOT NULL,
  bedrooms        SMALLINT,
  bathrooms       SMALLINT,
  size_sqm        NUMERIC(8,2),

  location_text   TEXT,
  lat             DOUBLE PRECISION NOT NULL,
  lng             DOUBLE PRECISION NOT NULL,
  geom            geometry(Point, 4326) NOT NULL,

  area_id         BIGINT NOT NULL,
  scraped_at_utc  TIMESTAMPTZ NOT NULL,

  images_count    SMALLINT DEFAULT 0,

  amenities                 JSONB NOT NULL DEFAULT '[]'::jsonb,
  normalized_amenities      JSONB NOT NULL DEFAULT '[]'::jsonb,
  unknown_amenity_codes     JSONB NOT NULL DEFAULT '[]'::jsonb,
  furnishing_status         TEXT,
  floor_number              SMALLINT,
  compound_name             TEXT,
  view_type                 TEXT,
  building_quality          TEXT,
  feature_raw               JSONB NOT NULL DEFAULT '{}'::jsonb
);


CREATE TABLE IF NOT EXISTS areas (
  area_id            BIGSERIAL PRIMARY KEY,
  name               TEXT NOT NULL,
  level              SMALLINT NOT NULL,
  parent_area_id     BIGINT,
  geom               geometry(MultiPolygon, 4326),
  center_geom        geometry(Point, 4326) NOT NULL,
  fallback_radius_m  INTEGER,

  CONSTRAINT ck_areas_level CHECK (level BETWEEN 1 AND 4),
  CONSTRAINT ck_areas_parent_not_self CHECK (
    parent_area_id IS NULL OR parent_area_id <> area_id
  ),
  CONSTRAINT fk_areas_parent FOREIGN KEY (parent_area_id)
    REFERENCES areas(area_id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

COMMENT ON COLUMN areas.level IS
  '1=governorate, 2=city, 3=district, 4=compound/neighborhood';


CREATE UNIQUE INDEX IF NOT EXISTS ux_areas_parent_level_name
  ON areas (COALESCE(parent_area_id, 0), level, lower(name));

CREATE INDEX IF NOT EXISTS ix_areas_parent
  ON areas(parent_area_id);

CREATE INDEX IF NOT EXISTS ix_areas_center_gist
  ON areas USING gist(center_geom);

CREATE INDEX IF NOT EXISTS ix_areas_center_geog_gist
  ON areas USING gist((center_geom::geography));

CREATE INDEX IF NOT EXISTS ix_areas_geom_gist
  ON areas USING gist(geom)
  WHERE geom IS NOT NULL;

CREATE INDEX IF NOT EXISTS ix_listings_geom_gist
  ON listings USING gist(geom);

CREATE INDEX IF NOT EXISTS ix_listings_geom_geog_gist
  ON listings USING gist((geom::geography));

CREATE INDEX IF NOT EXISTS ix_listings_category_period_area
  ON listings(category, period, area_id);

CREATE INDEX IF NOT EXISTS ix_listings_area_type_bedrooms
  ON listings(area_id, property_type, bedrooms);

CREATE INDEX IF NOT EXISTS ix_listings_match_area_recency
  ON listings(category, period, property_type, bedrooms, area_id, scraped_at_utc DESC);

CREATE INDEX IF NOT EXISTS ix_listings_market_snapshot
  ON listings(category, period, scraped_at_utc DESC);

CREATE INDEX IF NOT EXISTS ix_listings_scraped_at_utc
  ON listings(scraped_at_utc);

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM pg_constraint
    WHERE conname = 'fk_listings_area_id'
      AND conrelid = 'listings'::regclass
  ) THEN
    ALTER TABLE listings
      ADD CONSTRAINT fk_listings_area_id
      FOREIGN KEY (area_id)
      REFERENCES areas(area_id)
      ON UPDATE CASCADE
      ON DELETE RESTRICT;
  END IF;
END $$;
