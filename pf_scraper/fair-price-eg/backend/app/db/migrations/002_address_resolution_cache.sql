CREATE TABLE IF NOT EXISTS address_resolution_cache (
  id              BIGSERIAL PRIMARY KEY,
  raw_input       TEXT NOT NULL UNIQUE,
  matched_name    TEXT,
  lat             DOUBLE PRECISION NOT NULL,
  lng             DOUBLE PRECISION NOT NULL,
  precision_level TEXT NOT NULL,
  source          TEXT NOT NULL,
  created_at_utc  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_address_resolution_cache_input
  ON address_resolution_cache(lower(raw_input));
