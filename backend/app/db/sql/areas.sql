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
