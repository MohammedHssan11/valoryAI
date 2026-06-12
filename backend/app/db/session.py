import logging
import time

from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.observability import get_request_telemetry, metrics

logger = logging.getLogger(__name__)

engine_kwargs = {"pool_pre_ping": True, "future": True}
if settings.DATABASE_URL == "sqlite:///:memory:":
    engine_kwargs.update(
        {
            "connect_args": {"check_same_thread": False},
            "poolclass": StaticPool,
        }
    )
engine = create_engine(settings.DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def _statement_type(statement: str) -> str:
    first: list[str] = []
    for line in statement.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("--"):
            continue
        first = stripped.split(None, 1)
        break
    return first[0].upper() if first else "UNKNOWN"


@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(time.perf_counter())


@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    starts = conn.info.get("query_start_time", [])
    start = starts.pop() if starts else time.perf_counter()
    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    operation = _statement_type(statement)

    telemetry = get_request_telemetry()
    if telemetry is not None:
        telemetry.add_timing("db_query_ms", duration_ms)
        telemetry.increment("db_query_count")

    metrics.observe("db.query_latency_ms", duration_ms, {"operation": operation})

    if duration_ms >= settings.SLOW_QUERY_MS:
        if telemetry is not None:
            telemetry.increment("slow_query_count")
        metrics.increment("db.slow_query", {"operation": operation})
        metrics.record_event(
            "slow_query",
            {
                "duration_ms": duration_ms,
                "operation": operation,
                "threshold_ms": settings.SLOW_QUERY_MS,
                "executemany": bool(executemany),
            },
        )
        logger.warning(
            "slow_query",
            extra={
                "duration_ms": duration_ms,
                "operation": operation,
                "executemany": bool(executemany),
            },
        )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_database() -> None:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))


def wait_for_database() -> None:
    last_error: Exception | None = None
    for attempt in range(1, settings.DB_STARTUP_RETRIES + 1):
        try:
            check_database()
            logger.info("database_ready", extra={"attempt": attempt})
            return
        except Exception as exc:
            last_error = exc
            logger.warning(
                "database_not_ready",
                extra={
                    "attempt": attempt,
                    "max_attempts": settings.DB_STARTUP_RETRIES,
                    "error": str(exc),
                },
            )
            if attempt < settings.DB_STARTUP_RETRIES:
                time.sleep(settings.DB_STARTUP_RETRY_SECONDS)

    raise RuntimeError("Database is not ready after startup retries") from last_error


def dispose_engine() -> None:
    engine.dispose()
