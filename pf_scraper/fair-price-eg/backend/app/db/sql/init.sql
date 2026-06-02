CREATE EXTENSION IF NOT EXISTS postgis;

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

CREATE INDEX IF NOT EXISTS ix_listings_amenities_gin
  ON listings USING gin(amenities);

CREATE INDEX IF NOT EXISTS ix_listings_normalized_amenities_gin
  ON listings USING gin(normalized_amenities);

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

CREATE TABLE IF NOT EXISTS address_resolution_cache (
  id              BIGSERIAL PRIMARY KEY,
  raw_input       TEXT NOT NULL,
  normalized_input TEXT NOT NULL,
  matched_name    TEXT,
  lat             DOUBLE PRECISION NOT NULL,
  lng             DOUBLE PRECISION NOT NULL,
  precision_level TEXT NOT NULL,
  source          TEXT NOT NULL,
  confidence      DOUBLE PRECISION NOT NULL DEFAULT 0 CHECK (confidence BETWEEN 0 AND 1),
  ambiguity_status TEXT NOT NULL DEFAULT 'UNAMBIGUOUS',
  resolver_version TEXT NOT NULL DEFAULT '3A.1b.1',
  resolution_strategy TEXT NOT NULL DEFAULT 'LEGACY_CACHE',
  area_distance_m DOUBLE PRECISION,
  matched_entity JSONB NOT NULL DEFAULT '{}'::jsonb,
  source_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  expires_at_utc TIMESTAMPTZ,
  invalidated_at_utc TIMESTAMPTZ,
  created_at_utc  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at_utc  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_address_resolution_cache_input
  ON address_resolution_cache(lower(raw_input));

CREATE UNIQUE INDEX IF NOT EXISTS ux_address_resolution_cache_normalized_version
  ON address_resolution_cache(normalized_input, resolver_version);

CREATE TABLE IF NOT EXISTS location_entities (
  entity_id          TEXT PRIMARY KEY,
  entity_type        TEXT NOT NULL CHECK (entity_type IN ('city', 'district', 'neighborhood', 'compound', 'landmark')),
  canonical_name     TEXT NOT NULL,
  normalized_name    TEXT NOT NULL,
  canonical_area_id  BIGINT REFERENCES areas(area_id) ON UPDATE CASCADE ON DELETE SET NULL,
  centroid_lat       DOUBLE PRECISION NOT NULL CHECK (centroid_lat BETWEEN 22 AND 32),
  centroid_lng       DOUBLE PRECISION NOT NULL CHECK (centroid_lng BETWEEN 24 AND 37),
  authority_source   TEXT NOT NULL,
  version            TEXT NOT NULL,
  created_at_utc     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at_utc     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS location_aliases (
  alias_id          BIGSERIAL PRIMARY KEY,
  entity_id         TEXT NOT NULL REFERENCES location_entities(entity_id) ON UPDATE CASCADE ON DELETE CASCADE,
  raw_alias         TEXT NOT NULL,
  normalized_alias  TEXT NOT NULL,
  locale            TEXT NOT NULL DEFAULT 'mixed',
  priority          INTEGER NOT NULL DEFAULT 100,
  active            BOOLEAN NOT NULL DEFAULT TRUE,
  created_at_utc    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (entity_id, normalized_alias, raw_alias)
);

CREATE INDEX IF NOT EXISTS ix_location_aliases_normalized_active
  ON location_aliases(normalized_alias, active, priority DESC);

CREATE INDEX IF NOT EXISTS ix_location_entities_type_name
  ON location_entities(entity_type, normalized_name);

CREATE TABLE IF NOT EXISTS property_category_contracts (
  category              TEXT PRIMARY KEY,
  label                 TEXT NOT NULL,
  listing_category      TEXT NOT NULL,
  period                TEXT NOT NULL,
  value_basis           TEXT NOT NULL,
  compatible_property_types JSONB NOT NULL DEFAULT '[]'::jsonb,
  valuation_constraints JSONB NOT NULL DEFAULT '{}'::jsonb,
  retrieval_strategy    JSONB NOT NULL DEFAULT '{}'::jsonb,
  weighting_profile     JSONB NOT NULL DEFAULT '{}'::jsonb,
  confidence_profile    JSONB NOT NULL DEFAULT '{}'::jsonb,
  governance            JSONB NOT NULL DEFAULT '{}'::jsonb,
  active                BOOLEAN NOT NULL DEFAULT TRUE,
  created_at_utc        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at_utc        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS amenity_governance_registry (
  symbol                TEXT PRIMARY KEY,
  canonical_name        TEXT NOT NULL,
  normalized_name       TEXT NOT NULL,
  arabic_name           TEXT,
  classification        TEXT NOT NULL,
  aliases               JSONB NOT NULL DEFAULT '[]'::jsonb,
  weight_profile        JSONB NOT NULL DEFAULT '{}'::jsonb,
  retrieval_metadata    JSONB NOT NULL DEFAULT '{}'::jsonb,
  active                BOOLEAN NOT NULL DEFAULT TRUE,
  created_at_utc        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at_utc        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_amenity_governance_normalized_name
  ON amenity_governance_registry(normalized_name);

CREATE INDEX IF NOT EXISTS ix_amenity_governance_active_classification
  ON amenity_governance_registry(active, classification);
