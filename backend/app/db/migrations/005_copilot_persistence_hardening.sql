-- Canonical forward-only Copilot persistence migration.
-- Historical 000..004 migrations remain immutable.

CREATE TABLE IF NOT EXISTS users (
  id               BIGSERIAL PRIMARY KEY,
  external_subject TEXT NOT NULL UNIQUE,
  display_name     TEXT NOT NULL,
  created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  version          INTEGER NOT NULL DEFAULT 1 CHECK (version > 0),
  is_deleted       BOOLEAN NOT NULL DEFAULT FALSE,
  deleted_at       TIMESTAMPTZ
);

INSERT INTO users (external_subject, display_name)
VALUES ('legacy-default-user', 'Legacy Default User')
ON CONFLICT (external_subject) DO NOTHING;

CREATE TABLE IF NOT EXISTS workspaces (
  id          BIGSERIAL PRIMARY KEY,
  user_id     BIGINT REFERENCES users(id) ON DELETE RESTRICT,
  name        TEXT NOT NULL,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  version     INTEGER NOT NULL DEFAULT 1,
  is_deleted  BOOLEAN NOT NULL DEFAULT FALSE,
  deleted_at  TIMESTAMPTZ
);

ALTER TABLE workspaces
  ADD COLUMN IF NOT EXISTS user_id BIGINT REFERENCES users(id) ON DELETE RESTRICT,
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ADD COLUMN IF NOT EXISTS version INTEGER NOT NULL DEFAULT 1,
  ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMPTZ;

UPDATE workspaces
SET user_id = (SELECT id FROM users WHERE external_subject = 'legacy-default-user')
WHERE user_id IS NULL;
ALTER TABLE workspaces ALTER COLUMN user_id SET NOT NULL;

CREATE TABLE IF NOT EXISTS chats (
  id            BIGSERIAL PRIMARY KEY,
  user_id       BIGINT REFERENCES users(id) ON DELETE RESTRICT,
  workspace_id  BIGINT NOT NULL REFERENCES workspaces(id) ON DELETE RESTRICT,
  title         TEXT NOT NULL,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  version       INTEGER NOT NULL DEFAULT 1,
  is_deleted    BOOLEAN NOT NULL DEFAULT FALSE,
  deleted_at    TIMESTAMPTZ
);

ALTER TABLE chats
  ADD COLUMN IF NOT EXISTS user_id BIGINT REFERENCES users(id) ON DELETE RESTRICT,
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ADD COLUMN IF NOT EXISTS version INTEGER NOT NULL DEFAULT 1,
  ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMPTZ;
UPDATE chats SET user_id = workspaces.user_id FROM workspaces WHERE chats.workspace_id = workspaces.id AND chats.user_id IS NULL;
ALTER TABLE chats ALTER COLUMN user_id SET NOT NULL;

CREATE TABLE IF NOT EXISTS messages (
  id            BIGSERIAL PRIMARY KEY,
  user_id       BIGINT REFERENCES users(id) ON DELETE RESTRICT,
  workspace_id  BIGINT REFERENCES workspaces(id) ON DELETE RESTRICT,
  chat_id       BIGINT NOT NULL REFERENCES chats(id) ON DELETE RESTRICT,
  role          TEXT NOT NULL,
  content       TEXT NOT NULL,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  version       INTEGER NOT NULL DEFAULT 1,
  is_deleted    BOOLEAN NOT NULL DEFAULT FALSE,
  deleted_at    TIMESTAMPTZ
);

ALTER TABLE messages
  ADD COLUMN IF NOT EXISTS user_id BIGINT REFERENCES users(id) ON DELETE RESTRICT,
  ADD COLUMN IF NOT EXISTS workspace_id BIGINT REFERENCES workspaces(id) ON DELETE RESTRICT,
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ADD COLUMN IF NOT EXISTS version INTEGER NOT NULL DEFAULT 1,
  ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMPTZ;
UPDATE messages SET user_id = chats.user_id, workspace_id = chats.workspace_id FROM chats WHERE messages.chat_id = chats.id AND messages.user_id IS NULL;
ALTER TABLE messages ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE messages ALTER COLUMN workspace_id SET NOT NULL;

CREATE TABLE IF NOT EXISTS property_states (
  id            BIGSERIAL PRIMARY KEY,
  user_id       BIGINT REFERENCES users(id) ON DELETE RESTRICT,
  workspace_id  BIGINT NOT NULL REFERENCES workspaces(id) ON DELETE RESTRICT,
  label         TEXT NOT NULL DEFAULT 'Property',
  location      TEXT NOT NULL,
  area          NUMERIC(12,2) NOT NULL,
  bedrooms      INTEGER NOT NULL,
  bathrooms     INTEGER NOT NULL,
  amenities     JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  version       INTEGER NOT NULL DEFAULT 1,
  is_deleted    BOOLEAN NOT NULL DEFAULT FALSE,
  deleted_at    TIMESTAMPTZ
);

ALTER TABLE property_states
  ADD COLUMN IF NOT EXISTS user_id BIGINT REFERENCES users(id) ON DELETE RESTRICT,
  ADD COLUMN IF NOT EXISTS label TEXT NOT NULL DEFAULT 'Property',
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ADD COLUMN IF NOT EXISTS version INTEGER NOT NULL DEFAULT 1,
  ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMPTZ;
UPDATE property_states SET user_id = workspaces.user_id FROM workspaces WHERE property_states.workspace_id = workspaces.id AND property_states.user_id IS NULL;
ALTER TABLE property_states ALTER COLUMN user_id SET NOT NULL;

CREATE TABLE IF NOT EXISTS scenario_states (
  id                  BIGSERIAL PRIMARY KEY,
  user_id             BIGINT REFERENCES users(id) ON DELETE RESTRICT,
  workspace_id        BIGINT REFERENCES workspaces(id) ON DELETE RESTRICT,
  property_state_id   BIGINT NOT NULL REFERENCES property_states(id) ON DELETE RESTRICT,
  parent_scenario_id  BIGINT REFERENCES scenario_states(id) ON DELETE RESTRICT,
  name                TEXT NOT NULL,
  modifications       JSONB NOT NULL DEFAULT '{}'::jsonb,
  delta_value         NUMERIC(18,2),
  created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  version             INTEGER NOT NULL DEFAULT 1,
  is_deleted          BOOLEAN NOT NULL DEFAULT FALSE,
  deleted_at          TIMESTAMPTZ
);

ALTER TABLE scenario_states
  ADD COLUMN IF NOT EXISTS user_id BIGINT REFERENCES users(id) ON DELETE RESTRICT,
  ADD COLUMN IF NOT EXISTS workspace_id BIGINT REFERENCES workspaces(id) ON DELETE RESTRICT,
  ADD COLUMN IF NOT EXISTS parent_scenario_id BIGINT REFERENCES scenario_states(id) ON DELETE RESTRICT,
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ADD COLUMN IF NOT EXISTS version INTEGER NOT NULL DEFAULT 1,
  ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMPTZ;
UPDATE scenario_states
SET user_id = property_states.user_id, workspace_id = property_states.workspace_id
FROM property_states
WHERE scenario_states.property_state_id = property_states.id AND scenario_states.user_id IS NULL;
ALTER TABLE scenario_states ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE scenario_states ALTER COLUMN workspace_id SET NOT NULL;

CREATE TABLE IF NOT EXISTS assumptions (
  id                  BIGSERIAL PRIMARY KEY,
  user_id             BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  workspace_id        BIGINT NOT NULL REFERENCES workspaces(id) ON DELETE RESTRICT,
  property_state_id   BIGINT NOT NULL REFERENCES property_states(id) ON DELETE RESTRICT,
  scenario_state_id   BIGINT REFERENCES scenario_states(id) ON DELETE RESTRICT,
  key                 TEXT NOT NULL,
  value               JSONB,
  status              TEXT NOT NULL DEFAULT 'unknown' CHECK (status IN ('unknown', 'proposed', 'confirmed', 'overridden')),
  source              TEXT NOT NULL,
  confirmed_at        TIMESTAMPTZ,
  overridden_at       TIMESTAMPTZ,
  override_reason     TEXT,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  version             INTEGER NOT NULL DEFAULT 1,
  is_deleted          BOOLEAN NOT NULL DEFAULT FALSE,
  deleted_at          TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS scenario_lineage (
  id                  BIGSERIAL PRIMARY KEY,
  user_id             BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  workspace_id        BIGINT NOT NULL REFERENCES workspaces(id) ON DELETE RESTRICT,
  property_state_id   BIGINT NOT NULL REFERENCES property_states(id) ON DELETE RESTRICT,
  parent_scenario_id  BIGINT REFERENCES scenario_states(id) ON DELETE RESTRICT,
  child_scenario_id   BIGINT NOT NULL REFERENCES scenario_states(id) ON DELETE RESTRICT,
  action              TEXT NOT NULL DEFAULT 'forked',
  created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  version             INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS tool_events (
  id                  BIGSERIAL PRIMARY KEY,
  user_id             BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  workspace_id        BIGINT NOT NULL REFERENCES workspaces(id) ON DELETE RESTRICT,
  chat_id             BIGINT REFERENCES chats(id) ON DELETE RESTRICT,
  property_state_id   BIGINT REFERENCES property_states(id) ON DELETE RESTRICT,
  scenario_state_id   BIGINT REFERENCES scenario_states(id) ON DELETE RESTRICT,
  tool_name           TEXT NOT NULL,
  event_type          TEXT NOT NULL,
  payload             JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  version             INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS decision_history (
  id                  BIGSERIAL PRIMARY KEY,
  user_id             BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  workspace_id        BIGINT NOT NULL REFERENCES workspaces(id) ON DELETE RESTRICT,
  chat_id             BIGINT REFERENCES chats(id) ON DELETE RESTRICT,
  property_state_id   BIGINT REFERENCES property_states(id) ON DELETE RESTRICT,
  scenario_state_id   BIGINT REFERENCES scenario_states(id) ON DELETE RESTRICT,
  action              TEXT NOT NULL,
  details             JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  version             INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS broker_sessions (
  session_id    TEXT PRIMARY KEY,
  user_id       BIGINT REFERENCES users(id) ON DELETE RESTRICT,
  workspace_id  BIGINT REFERENCES workspaces(id) ON DELETE RESTRICT,
  state         JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  version       INTEGER NOT NULL DEFAULT 1
);

-- Existing monitoring writers already target these tables. This migration
-- supplies the missing durable schema without changing monitoring behavior.
CREATE TABLE IF NOT EXISTS prediction_logs (
  id                BIGSERIAL PRIMARY KEY,
  request_id        TEXT NOT NULL,
  price             NUMERIC(18,2),
  engine            TEXT,
  routing_decision  TEXT,
  lat               DOUBLE PRECISION,
  lng               DOUBLE PRECISION,
  property_type     TEXT,
  size_sqm          DOUBLE PRECISION,
  compound          TEXT,
  h3_res9           TEXT,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS shadow_logs (
  id                BIGSERIAL PRIMARY KEY,
  request_id        TEXT NOT NULL,
  actual_response   NUMERIC(18,2),
  router_prediction NUMERIC(18,2),
  ml_prediction     NUMERIC(18,2),
  cmt_prediction    NUMERIC(18,2),
  engine_used       TEXT,
  routing_reason    TEXT,
  comparable_count  INTEGER,
  confidence_score  DOUBLE PRECISION,
  compound_name     TEXT,
  h3_res9           TEXT,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_workspaces_user_active ON workspaces(user_id, is_deleted);
CREATE INDEX IF NOT EXISTS ix_chats_user_workspace_active ON chats(user_id, workspace_id, is_deleted);
CREATE INDEX IF NOT EXISTS ix_messages_chat_created_active ON messages(user_id, chat_id, is_deleted, created_at);
CREATE INDEX IF NOT EXISTS ix_property_states_user_workspace_active ON property_states(user_id, workspace_id, is_deleted);
CREATE INDEX IF NOT EXISTS ix_scenario_states_user_property_active ON scenario_states(user_id, property_state_id, is_deleted);
CREATE INDEX IF NOT EXISTS ix_scenario_states_parent ON scenario_states(parent_scenario_id);
CREATE INDEX IF NOT EXISTS ix_assumptions_user_property_active ON assumptions(user_id, property_state_id, is_deleted);
CREATE INDEX IF NOT EXISTS ix_assumptions_scenario_active ON assumptions(scenario_state_id, is_deleted);
CREATE INDEX IF NOT EXISTS ix_scenario_lineage_user_property ON scenario_lineage(user_id, property_state_id);
CREATE INDEX IF NOT EXISTS ix_scenario_lineage_child ON scenario_lineage(child_scenario_id);
CREATE INDEX IF NOT EXISTS ix_tool_events_user_workspace_created ON tool_events(user_id, workspace_id, created_at);
CREATE INDEX IF NOT EXISTS ix_decision_history_user_workspace_created ON decision_history(user_id, workspace_id, created_at);
CREATE INDEX IF NOT EXISTS ix_broker_sessions_workspace_updated ON broker_sessions(workspace_id, updated_at);
CREATE INDEX IF NOT EXISTS ix_prediction_logs_request_created ON prediction_logs(request_id, created_at);
CREATE INDEX IF NOT EXISTS ix_shadow_logs_request_created ON shadow_logs(request_id, created_at);

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_messages_role') THEN
    ALTER TABLE messages ADD CONSTRAINT ck_messages_role CHECK (role IN ('user', 'assistant', 'system', 'tool'));
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_property_states_area_positive') THEN
    ALTER TABLE property_states ADD CONSTRAINT ck_property_states_area_positive CHECK (area > 0);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_property_states_bedrooms_non_negative') THEN
    ALTER TABLE property_states ADD CONSTRAINT ck_property_states_bedrooms_non_negative CHECK (bedrooms >= 0);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_property_states_bathrooms_non_negative') THEN
    ALTER TABLE property_states ADD CONSTRAINT ck_property_states_bathrooms_non_negative CHECK (bathrooms >= 0);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_scenario_states_delta_non_negative') THEN
    ALTER TABLE scenario_states ADD CONSTRAINT ck_scenario_states_delta_non_negative CHECK (delta_value IS NULL OR delta_value >= 0);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_workspaces_id_user') THEN
    ALTER TABLE workspaces ADD CONSTRAINT uq_workspaces_id_user UNIQUE (id, user_id);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_chats_id_workspace_user') THEN
    ALTER TABLE chats ADD CONSTRAINT uq_chats_id_workspace_user UNIQUE (id, workspace_id, user_id);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_property_states_id_workspace_user') THEN
    ALTER TABLE property_states ADD CONSTRAINT uq_property_states_id_workspace_user UNIQUE (id, workspace_id, user_id);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_scenario_states_id_property_workspace_user') THEN
    ALTER TABLE scenario_states ADD CONSTRAINT uq_scenario_states_id_property_workspace_user UNIQUE (id, property_state_id, workspace_id, user_id);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_chats_workspace_user') THEN
    ALTER TABLE chats ADD CONSTRAINT fk_chats_workspace_user
      FOREIGN KEY (workspace_id, user_id) REFERENCES workspaces(id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_messages_chat_workspace_user') THEN
    ALTER TABLE messages ADD CONSTRAINT fk_messages_chat_workspace_user
      FOREIGN KEY (chat_id, workspace_id, user_id) REFERENCES chats(id, workspace_id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_property_states_workspace_user') THEN
    ALTER TABLE property_states ADD CONSTRAINT fk_property_states_workspace_user
      FOREIGN KEY (workspace_id, user_id) REFERENCES workspaces(id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_scenario_states_property_workspace_user') THEN
    ALTER TABLE scenario_states ADD CONSTRAINT fk_scenario_states_property_workspace_user
      FOREIGN KEY (property_state_id, workspace_id, user_id)
      REFERENCES property_states(id, workspace_id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_assumptions_property_workspace_user') THEN
    ALTER TABLE assumptions ADD CONSTRAINT fk_assumptions_property_workspace_user
      FOREIGN KEY (property_state_id, workspace_id, user_id)
      REFERENCES property_states(id, workspace_id, user_id) ON DELETE RESTRICT;
  END IF;
END $$;
