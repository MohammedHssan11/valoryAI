-- Phase 5.5B.7: read-path indexes for descriptive Market Insight analytics.

CREATE INDEX IF NOT EXISTS ix_prediction_logs_market_filters
  ON prediction_logs(compound, h3_res9, property_type, created_at);

CREATE INDEX IF NOT EXISTS ix_shadow_logs_market_filters
  ON shadow_logs(compound_name, h3_res9, created_at);
