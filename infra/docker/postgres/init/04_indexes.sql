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
