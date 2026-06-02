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

CREATE TABLE IF NOT EXISTS address_resolution_cache (
  id              BIGSERIAL PRIMARY KEY,
  raw_input       TEXT NOT NULL,
  matched_name    TEXT,
  lat             DOUBLE PRECISION NOT NULL,
  lng             DOUBLE PRECISION NOT NULL,
  precision_level TEXT NOT NULL,
  source          TEXT NOT NULL,
  created_at_utc  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE address_resolution_cache
  DROP CONSTRAINT IF EXISTS address_resolution_cache_raw_input_key;

ALTER TABLE address_resolution_cache
  ADD COLUMN IF NOT EXISTS normalized_input TEXT,
  ADD COLUMN IF NOT EXISTS confidence DOUBLE PRECISION NOT NULL DEFAULT 0 CHECK (confidence BETWEEN 0 AND 1),
  ADD COLUMN IF NOT EXISTS ambiguity_status TEXT NOT NULL DEFAULT 'UNAMBIGUOUS',
  ADD COLUMN IF NOT EXISTS resolver_version TEXT NOT NULL DEFAULT '3A.1b.1',
  ADD COLUMN IF NOT EXISTS resolution_strategy TEXT NOT NULL DEFAULT 'LEGACY_CACHE',
  ADD COLUMN IF NOT EXISTS area_distance_m DOUBLE PRECISION,
  ADD COLUMN IF NOT EXISTS matched_entity JSONB NOT NULL DEFAULT '{}'::jsonb,
  ADD COLUMN IF NOT EXISTS source_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  ADD COLUMN IF NOT EXISTS expires_at_utc TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS invalidated_at_utc TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS updated_at_utc TIMESTAMPTZ NOT NULL DEFAULT NOW();

UPDATE address_resolution_cache
SET normalized_input = lower(regexp_replace(trim(raw_input), '[[:space:]]+', ' ', 'g'))
WHERE normalized_input IS NULL;

ALTER TABLE address_resolution_cache
  ALTER COLUMN normalized_input SET NOT NULL;

DELETE FROM address_resolution_cache newer
USING address_resolution_cache older
WHERE newer.normalized_input = older.normalized_input
  AND newer.resolver_version = older.resolver_version
  AND newer.id > older.id;

CREATE UNIQUE INDEX IF NOT EXISTS ux_address_resolution_cache_normalized_version
  ON address_resolution_cache(normalized_input, resolver_version);

CREATE INDEX IF NOT EXISTS ix_address_resolution_cache_governed_lookup
  ON address_resolution_cache(normalized_input, resolver_version, invalidated_at_utc, expires_at_utc);

CREATE INDEX IF NOT EXISTS ix_listings_compound_name_lower
  ON listings(lower(compound_name))
  WHERE compound_name IS NOT NULL;

CREATE INDEX IF NOT EXISTS ix_areas_name_lower
  ON areas(lower(name));

INSERT INTO location_entities (
  entity_id, entity_type, canonical_name, normalized_name, canonical_area_id,
  centroid_lat, centroid_lng, authority_source, version
) VALUES
  ('eg.compound.madinaty', 'compound', 'Madinaty', 'مدينتي', NULL, 30.0820, 31.6380, 'VALORAI_STATIC_GAZETTEER', '3A.1b.1'),
  ('eg.compound.rehab', 'compound', 'Al Rehab', 'الرحاب', NULL, 30.0630, 31.4910, 'VALORAI_STATIC_GAZETTEER', '3A.1b.1'),
  ('eg.city.sheikh_zayed', 'city', 'Sheikh Zayed', 'الشيخ زايد', NULL, 30.0131, 30.9764, 'VALORAI_STATIC_GAZETTEER', '3A.1b.1'),
  ('eg.city.sixth_october', 'city', '6th of October', 'السادس من اكتوبر', NULL, 29.9668, 30.9430, 'VALORAI_STATIC_GAZETTEER', '3A.1b.1'),
  ('eg.city.new_cairo', 'city', 'New Cairo', 'القاهره الجديده', NULL, 30.0074, 31.4913, 'VALORAI_STATIC_GAZETTEER', '3A.1b.1'),
  ('eg.district.fifth_settlement', 'district', 'Fifth Settlement', 'التجمع الخامس', NULL, 30.0086, 31.4507, 'VALORAI_STATIC_GAZETTEER', '3A.1b.1'),
  ('eg.city.new_capital', 'city', 'New Administrative Capital', 'العاصمه الاداريه الجديده', NULL, 30.0169, 31.7044, 'VALORAI_STATIC_GAZETTEER', '3A.1b.1')
ON CONFLICT (entity_id) DO UPDATE
SET
  entity_type = EXCLUDED.entity_type,
  canonical_name = EXCLUDED.canonical_name,
  normalized_name = EXCLUDED.normalized_name,
  centroid_lat = EXCLUDED.centroid_lat,
  centroid_lng = EXCLUDED.centroid_lng,
  authority_source = EXCLUDED.authority_source,
  version = EXCLUDED.version,
  updated_at_utc = NOW();

INSERT INTO location_aliases (entity_id, raw_alias, normalized_alias, locale, priority) VALUES
  ('eg.compound.madinaty', 'مدينتي', 'مدينتي', 'ar', 100),
  ('eg.compound.madinaty', 'مدينتى', 'مدينتي', 'ar', 100),
  ('eg.compound.madinaty', 'Madinaty', 'مدينتي', 'en', 100),
  ('eg.compound.madinaty', 'Madinty', 'مدينتي', 'en', 95),
  ('eg.compound.rehab', 'الرحاب', 'الرحاب', 'ar', 100),
  ('eg.compound.rehab', 'Al Rehab', 'الرحاب', 'en', 100),
  ('eg.compound.rehab', 'El Rehab', 'الرحاب', 'en', 100),
  ('eg.compound.rehab', 'Rehab', 'الرحاب', 'en', 90),
  ('eg.city.sheikh_zayed', 'الشيخ زايد', 'الشيخ زايد', 'ar', 100),
  ('eg.city.sheikh_zayed', 'Sheikh Zayed', 'الشيخ زايد', 'en', 100),
  ('eg.city.sheikh_zayed', 'Zayed', 'الشيخ زايد', 'en', 80),
  ('eg.city.sixth_october', '6 October', 'السادس من اكتوبر', 'en', 100),
  ('eg.city.sixth_october', '6th October', 'السادس من اكتوبر', 'en', 100),
  ('eg.city.sixth_october', 'October', 'السادس من اكتوبر', 'en', 75),
  ('eg.city.sixth_october', 'اكتوبر', 'السادس من اكتوبر', 'ar', 75),
  ('eg.city.new_cairo', 'New Cairo', 'القاهره الجديده', 'en', 100),
  ('eg.city.new_cairo', 'القاهرة الجديدة', 'القاهره الجديده', 'ar', 100),
  ('eg.district.fifth_settlement', 'التجمع الخامس', 'التجمع الخامس', 'ar', 100),
  ('eg.district.fifth_settlement', 'Tagamoa', 'التجمع الخامس', 'franco', 95),
  ('eg.district.fifth_settlement', 'tagamo3', 'التجمع الخامس', 'franco', 95),
  ('eg.district.fifth_settlement', 'tgamo3', 'التجمع الخامس', 'franco', 90),
  ('eg.district.fifth_settlement', 'Fifth Settlement', 'التجمع الخامس', 'en', 100),
  ('eg.city.new_capital', 'New Capital', 'العاصمه الاداريه الجديده', 'en', 100),
  ('eg.city.new_capital', 'NAC', 'العاصمه الاداريه الجديده', 'en', 95),
  ('eg.city.new_capital', 'العاصمة الإدارية', 'العاصمه الاداريه الجديده', 'ar', 100),
  ('eg.city.new_capital', 'العاصمة الإدارية الجديدة', 'العاصمه الاداريه الجديده', 'ar', 100)
ON CONFLICT (entity_id, normalized_alias, raw_alias) DO UPDATE
SET
  locale = EXCLUDED.locale,
  priority = EXCLUDED.priority,
  active = TRUE;
