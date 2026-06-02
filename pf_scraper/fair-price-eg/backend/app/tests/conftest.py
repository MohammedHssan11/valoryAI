import os
import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[2]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

if os.environ.get("RUN_POSTGIS_INTEGRATION") == "1":
    os.environ.setdefault(
        "DATABASE_URL",
        "postgresql+psycopg://fairprice:fairprice@localhost:5432/fairprice",
    )
else:
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["ENV"] = "test"
os.environ["DB_STARTUP_RETRIES"] = "1"
os.environ["LOG_LEVEL"] = "ERROR"

from app.db.base import Base  # noqa: E402
from app.db.session import engine  # noqa: E402
import app.models.copilot  # noqa: E402,F401

Base.metadata.create_all(bind=engine)
