-- Phase 5.5B.2: Copilot valuation and explainability tool adapters.

ALTER TABLE property_states
  ADD COLUMN IF NOT EXISTS property_type TEXT NOT NULL DEFAULT 'Apartment',
  ADD COLUMN IF NOT EXISTS property_category TEXT NOT NULL DEFAULT 'residential_rent',
  ADD COLUMN IF NOT EXISTS valuation_inputs JSONB NOT NULL DEFAULT '{}'::jsonb;

CREATE TABLE IF NOT EXISTS valuation_snapshots (
  valuation_id            TEXT PRIMARY KEY,
  user_id                 BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  workspace_id            BIGINT NOT NULL REFERENCES workspaces(id) ON DELETE RESTRICT,
  property_state_id       BIGINT NOT NULL REFERENCES property_states(id) ON DELETE RESTRICT,
  scenario_state_id       BIGINT REFERENCES scenario_states(id) ON DELETE RESTRICT,
  router_request          JSONB NOT NULL,
  normalized_response     JSONB NOT NULL,
  explainability_payload  JSONB,
  created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  version                 INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS ix_valuation_snapshots_user_workspace_created
  ON valuation_snapshots(user_id, workspace_id, created_at);

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_valuation_snapshots_workspace_user') THEN
    ALTER TABLE valuation_snapshots ADD CONSTRAINT fk_valuation_snapshots_workspace_user
      FOREIGN KEY (workspace_id, user_id) REFERENCES workspaces(id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_valuation_snapshots_property_workspace_user') THEN
    ALTER TABLE valuation_snapshots ADD CONSTRAINT fk_valuation_snapshots_property_workspace_user
      FOREIGN KEY (property_state_id, workspace_id, user_id)
      REFERENCES property_states(id, workspace_id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_valuation_snapshots_scenario_workspace_user') THEN
    ALTER TABLE valuation_snapshots ADD CONSTRAINT fk_valuation_snapshots_scenario_workspace_user
      FOREIGN KEY (scenario_state_id, workspace_id, user_id)
      REFERENCES scenario_states(id, workspace_id, user_id) ON DELETE RESTRICT;
  END IF;
END $$;
