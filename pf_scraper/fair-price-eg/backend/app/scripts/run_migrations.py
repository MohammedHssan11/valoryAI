import argparse
import hashlib
import logging
import os
import sys
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings

logger = logging.getLogger(__name__)

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / "db" / "migrations"
LOCK_ID = 42069  # Arbitrary 32-bit integer for the advisory lock

# Migration 005 predates production evidence that historical monitoring tables
# used "timestamp". Keep the immutable migration checksum stable and normalize
# only the legacy shape immediately before applying it.
MIGRATION_COMPATIBILITY_SQL = {
    "005_copilot_persistence_hardening.sql": """
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_schema = 'public' AND table_name = 'prediction_logs'
  ) THEN
    ALTER TABLE prediction_logs ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ;
    IF EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public' AND table_name = 'prediction_logs' AND column_name = 'timestamp'
    ) THEN
      UPDATE prediction_logs SET created_at = COALESCE(created_at, "timestamp", NOW()) WHERE created_at IS NULL;
    ELSE
      UPDATE prediction_logs SET created_at = NOW() WHERE created_at IS NULL;
    END IF;
    ALTER TABLE prediction_logs ALTER COLUMN created_at SET DEFAULT NOW();
    ALTER TABLE prediction_logs ALTER COLUMN created_at SET NOT NULL;
  END IF;

  IF EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_schema = 'public' AND table_name = 'shadow_logs'
  ) THEN
    ALTER TABLE shadow_logs ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ;
    IF EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public' AND table_name = 'shadow_logs' AND column_name = 'timestamp'
    ) THEN
      UPDATE shadow_logs SET created_at = COALESCE(created_at, "timestamp", NOW()) WHERE created_at IS NULL;
    ELSE
      UPDATE shadow_logs SET created_at = NOW() WHERE created_at IS NULL;
    END IF;
    ALTER TABLE shadow_logs ALTER COLUMN created_at SET DEFAULT NOW();
    ALTER TABLE shadow_logs ALTER COLUMN created_at SET NOT NULL;
  END IF;
END $$;
""",
}

# Hardening Requirement 1: Migration Checksums
SCHEMA_MIGRATIONS_SQL = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version TEXT PRIMARY KEY,
    checksum TEXT NOT NULL,
    applied_at TIMESTAMPTZ DEFAULT NOW()
);
"""

def compute_checksum(filepath: Path) -> str:
    content = filepath.read_text(encoding="utf-8")
    # Normalize line endings to avoid checksum mismatch between OS
    content = content.replace("\r\n", "\n").strip()
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def acquire_lock(conn):
    logger.info("migration_lock_attempt", extra={"lock_id": LOCK_ID})
    # Wait for the lock
    conn.execute(text("SELECT pg_advisory_lock(:id)"), {"id": LOCK_ID})
    logger.info("migration_lock_acquired", extra={"lock_id": LOCK_ID})

def release_lock(conn):
    conn.execute(text("SELECT pg_advisory_unlock(:id)"), {"id": LOCK_ID})
    logger.info("migration_lock_released", extra={"lock_id": LOCK_ID})

def run_migrations(verify_only: bool = False):
    logger.info("migration_start", extra={"verify_only": verify_only, "dir": str(MIGRATIONS_DIR)})
    
    # Sort files alphabetically to guarantee deterministic ordering
    migration_files = sorted([f for f in MIGRATIONS_DIR.glob("*.sql")])
    
    if not migration_files:
        logger.warning("migration_no_files_found", extra={"dir": str(MIGRATIONS_DIR)})
        return

    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    
    try:
        with engine.connect() as conn:
            # Hardening Requirement 3: Advisory Locking
            acquire_lock(conn)
            conn.commit()  # commit autobegun transaction
            
            try:
                # Ensure the migrations table exists
                if not verify_only:
                    conn.execute(text(SCHEMA_MIGRATIONS_SQL))
                    conn.commit()
                else:
                    # In verify mode, just check if it exists
                    res = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'schema_migrations')")).scalar()
                    if not res:
                        logger.error("migration_verify_failed", extra={"reason": "schema_migrations table does not exist"})
                        sys.exit(1)
                
                applied_migrations = {}
                rows = conn.execute(text("SELECT version, checksum FROM schema_migrations")).fetchall()
                conn.commit()  # commit the select
                for row in rows:
                    applied_migrations[row[0]] = row[1]

                unapplied_count = 0
                
                for filepath in migration_files:
                    version = filepath.name
                    current_checksum = compute_checksum(filepath)
                    
                    # Hardening Requirement 2: Immutable Migration Enforcement
                    if version in applied_migrations:
                        applied_checksum = applied_migrations[version]
                        if current_checksum != applied_checksum:
                            logger.error("migration_checksum_mismatch", extra={
                                "version": version,
                                "expected_checksum": applied_checksum,
                                "actual_checksum": current_checksum
                            })
                            sys.exit(1)
                        continue
                    
                    unapplied_count += 1
                    
                    if verify_only:
                        logger.warning("migration_verify_unapplied_detected", extra={"version": version})
                        continue
                        
                    logger.info("migration_applying", extra={"version": version, "checksum": current_checksum})
                    
                    # Hardening Requirement 4: Atomic Migration Transactions
                    with conn.begin():
                        try:
                            compatibility_sql = MIGRATION_COMPATIBILITY_SQL.get(filepath.name)
                            if compatibility_sql:
                                logger.info("migration_compatibility_applying", extra={"version": filepath.name})
                                conn.exec_driver_sql(compatibility_sql)
                            sql_content = filepath.read_text(encoding="utf-8")
                            conn.exec_driver_sql(sql_content)
                            
                            conn.execute(
                                text("INSERT INTO schema_migrations (version, checksum) VALUES (:version, :checksum)"),
                                {"version": version, "checksum": current_checksum}
                            )
                            logger.info("migration_success", extra={"version": version})
                        except SQLAlchemyError as e:
                            logger.error("migration_failure", extra={"version": version, "error": str(e)})
                            raise  # Let the context manager handle the rollback
                
                if verify_only and unapplied_count > 0:
                    logger.error("migration_verify_failed", extra={"reason": f"{unapplied_count} unapplied migrations detected."})
                    sys.exit(1)
                elif verify_only:
                    logger.info("migration_verify_success", extra={"details": "All migrations are applied and checksums match."})
                else:
                    logger.info("migration_summary", extra={"total_unapplied_processed": unapplied_count})

            finally:
                release_lock(conn)

    except SQLAlchemyError as e:
        logger.critical("migration_critical_db_error", extra={"error": str(e)})
        logger.exception(e)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deterministic Migration Runner")
    parser.add_argument("--verify", action="store_true", help="Run in dry-run/verification mode")
    args = parser.parse_args()
    
    # Configure basic logging to stdout for the runner
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    run_migrations(verify_only=args.verify)
