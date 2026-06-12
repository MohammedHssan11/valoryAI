-- Production blocker resolution: attributable broker sessions, precise
-- workspace cascade restore provenance, and complete tenant constraints.

ALTER TABLE chats ADD COLUMN IF NOT EXISTS deleted_by_workspace_id BIGINT;
ALTER TABLE messages ADD COLUMN IF NOT EXISTS deleted_by_workspace_id BIGINT;
ALTER TABLE property_states ADD COLUMN IF NOT EXISTS deleted_by_workspace_id BIGINT;
ALTER TABLE scenario_states ADD COLUMN IF NOT EXISTS deleted_by_workspace_id BIGINT;
ALTER TABLE assumptions ADD COLUMN IF NOT EXISTS deleted_by_workspace_id BIGINT;

ALTER TABLE broker_sessions ADD COLUMN IF NOT EXISTS scenario_id BIGINT REFERENCES scenario_states(id) ON DELETE RESTRICT;

-- Quarantine unattributed pre-release broker rows under one explicit legacy
-- context so no durable session remains ownerless after an interrupted rollout.
DO $$
DECLARE
  legacy_user_id BIGINT;
  legacy_workspace_id BIGINT;
  legacy_property_id BIGINT;
  legacy_scenario_id BIGINT;
BEGIN
  IF EXISTS (
    SELECT 1
    FROM broker_sessions
    WHERE user_id IS NULL OR workspace_id IS NULL OR scenario_id IS NULL
  ) THEN
    SELECT id INTO legacy_user_id
    FROM users
    WHERE external_subject = 'legacy-default-user';

    SELECT id INTO legacy_workspace_id
    FROM workspaces
    WHERE user_id = legacy_user_id AND name = 'Legacy Broker Sessions'
    ORDER BY id
    LIMIT 1;

    IF legacy_workspace_id IS NULL THEN
      INSERT INTO workspaces (user_id, name)
      VALUES (legacy_user_id, 'Legacy Broker Sessions')
      RETURNING id INTO legacy_workspace_id;
    END IF;

    SELECT id INTO legacy_property_id
    FROM property_states
    WHERE user_id = legacy_user_id
      AND workspace_id = legacy_workspace_id
      AND label = 'Legacy Broker Session Context'
    ORDER BY id
    LIMIT 1;

    IF legacy_property_id IS NULL THEN
      INSERT INTO property_states (
        user_id, workspace_id, label, location, area, bedrooms, bathrooms, amenities
      )
      VALUES (
        legacy_user_id, legacy_workspace_id, 'Legacy Broker Session Context', 'Legacy', 1, 0, 0, '{}'::jsonb
      )
      RETURNING id INTO legacy_property_id;
    END IF;

    SELECT id INTO legacy_scenario_id
    FROM scenario_states
    WHERE user_id = legacy_user_id
      AND workspace_id = legacy_workspace_id
      AND property_state_id = legacy_property_id
      AND name = 'Legacy Broker Session Context'
    ORDER BY id
    LIMIT 1;

    IF legacy_scenario_id IS NULL THEN
      INSERT INTO scenario_states (
        user_id, workspace_id, property_state_id, name, modifications
      )
      VALUES (
        legacy_user_id, legacy_workspace_id, legacy_property_id, 'Legacy Broker Session Context', '{}'::jsonb
      )
      RETURNING id INTO legacy_scenario_id;
    END IF;

    UPDATE broker_sessions
    SET user_id = legacy_user_id,
        workspace_id = legacy_workspace_id,
        scenario_id = legacy_scenario_id,
        updated_at = NOW(),
        version = version + 1
    WHERE user_id IS NULL OR workspace_id IS NULL OR scenario_id IS NULL;
  END IF;
END $$;

ALTER TABLE broker_sessions ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE broker_sessions ALTER COLUMN workspace_id SET NOT NULL;
ALTER TABLE broker_sessions ALTER COLUMN scenario_id SET NOT NULL;

CREATE INDEX IF NOT EXISTS ix_chats_workspace_cascade_restore ON chats(user_id, workspace_id, deleted_by_workspace_id);
CREATE INDEX IF NOT EXISTS ix_messages_workspace_cascade_restore ON messages(user_id, workspace_id, deleted_by_workspace_id);
CREATE INDEX IF NOT EXISTS ix_property_states_workspace_cascade_restore ON property_states(user_id, workspace_id, deleted_by_workspace_id);
CREATE INDEX IF NOT EXISTS ix_scenario_states_workspace_cascade_restore ON scenario_states(user_id, workspace_id, deleted_by_workspace_id);
CREATE INDEX IF NOT EXISTS ix_assumptions_workspace_cascade_restore ON assumptions(user_id, workspace_id, deleted_by_workspace_id);
CREATE INDEX IF NOT EXISTS ix_broker_sessions_owner_scenario_updated ON broker_sessions(user_id, workspace_id, scenario_id, updated_at);

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_chats_workspace_cascade_delete') THEN
    ALTER TABLE chats ADD CONSTRAINT ck_chats_workspace_cascade_delete
      CHECK (deleted_by_workspace_id IS NULL OR is_deleted);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_messages_workspace_cascade_delete') THEN
    ALTER TABLE messages ADD CONSTRAINT ck_messages_workspace_cascade_delete
      CHECK (deleted_by_workspace_id IS NULL OR is_deleted);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_property_states_workspace_cascade_delete') THEN
    ALTER TABLE property_states ADD CONSTRAINT ck_property_states_workspace_cascade_delete
      CHECK (deleted_by_workspace_id IS NULL OR is_deleted);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_scenario_states_workspace_cascade_delete') THEN
    ALTER TABLE scenario_states ADD CONSTRAINT ck_scenario_states_workspace_cascade_delete
      CHECK (deleted_by_workspace_id IS NULL OR is_deleted);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_assumptions_workspace_cascade_delete') THEN
    ALTER TABLE assumptions ADD CONSTRAINT ck_assumptions_workspace_cascade_delete
      CHECK (deleted_by_workspace_id IS NULL OR is_deleted);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_scenario_states_id_workspace_user') THEN
    ALTER TABLE scenario_states ADD CONSTRAINT uq_scenario_states_id_workspace_user
      UNIQUE (id, workspace_id, user_id);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_assumptions_scenario_property_workspace_user') THEN
    ALTER TABLE assumptions ADD CONSTRAINT fk_assumptions_scenario_property_workspace_user
      FOREIGN KEY (scenario_state_id, property_state_id, workspace_id, user_id)
      REFERENCES scenario_states(id, property_state_id, workspace_id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_scenario_lineage_property_workspace_user') THEN
    ALTER TABLE scenario_lineage ADD CONSTRAINT fk_scenario_lineage_property_workspace_user
      FOREIGN KEY (property_state_id, workspace_id, user_id)
      REFERENCES property_states(id, workspace_id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_scenario_lineage_child_property_workspace_user') THEN
    ALTER TABLE scenario_lineage ADD CONSTRAINT fk_scenario_lineage_child_property_workspace_user
      FOREIGN KEY (child_scenario_id, property_state_id, workspace_id, user_id)
      REFERENCES scenario_states(id, property_state_id, workspace_id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_scenario_lineage_parent_property_workspace_user') THEN
    ALTER TABLE scenario_lineage ADD CONSTRAINT fk_scenario_lineage_parent_property_workspace_user
      FOREIGN KEY (parent_scenario_id, property_state_id, workspace_id, user_id)
      REFERENCES scenario_states(id, property_state_id, workspace_id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_tool_events_workspace_user') THEN
    ALTER TABLE tool_events ADD CONSTRAINT fk_tool_events_workspace_user
      FOREIGN KEY (workspace_id, user_id) REFERENCES workspaces(id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_tool_events_chat_workspace_user') THEN
    ALTER TABLE tool_events ADD CONSTRAINT fk_tool_events_chat_workspace_user
      FOREIGN KEY (chat_id, workspace_id, user_id) REFERENCES chats(id, workspace_id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_tool_events_property_workspace_user') THEN
    ALTER TABLE tool_events ADD CONSTRAINT fk_tool_events_property_workspace_user
      FOREIGN KEY (property_state_id, workspace_id, user_id)
      REFERENCES property_states(id, workspace_id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_tool_events_scenario_workspace_user') THEN
    ALTER TABLE tool_events ADD CONSTRAINT fk_tool_events_scenario_workspace_user
      FOREIGN KEY (scenario_state_id, workspace_id, user_id)
      REFERENCES scenario_states(id, workspace_id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_decision_history_workspace_user') THEN
    ALTER TABLE decision_history ADD CONSTRAINT fk_decision_history_workspace_user
      FOREIGN KEY (workspace_id, user_id) REFERENCES workspaces(id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_decision_history_chat_workspace_user') THEN
    ALTER TABLE decision_history ADD CONSTRAINT fk_decision_history_chat_workspace_user
      FOREIGN KEY (chat_id, workspace_id, user_id) REFERENCES chats(id, workspace_id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_decision_history_property_workspace_user') THEN
    ALTER TABLE decision_history ADD CONSTRAINT fk_decision_history_property_workspace_user
      FOREIGN KEY (property_state_id, workspace_id, user_id)
      REFERENCES property_states(id, workspace_id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_decision_history_scenario_workspace_user') THEN
    ALTER TABLE decision_history ADD CONSTRAINT fk_decision_history_scenario_workspace_user
      FOREIGN KEY (scenario_state_id, workspace_id, user_id)
      REFERENCES scenario_states(id, workspace_id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_broker_sessions_workspace_user') THEN
    ALTER TABLE broker_sessions ADD CONSTRAINT fk_broker_sessions_workspace_user
      FOREIGN KEY (workspace_id, user_id) REFERENCES workspaces(id, user_id) ON DELETE RESTRICT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_broker_sessions_scenario_workspace_user') THEN
    ALTER TABLE broker_sessions ADD CONSTRAINT fk_broker_sessions_scenario_workspace_user
      FOREIGN KEY (scenario_id, workspace_id, user_id)
      REFERENCES scenario_states(id, workspace_id, user_id) ON DELETE RESTRICT;
  END IF;
END $$;
