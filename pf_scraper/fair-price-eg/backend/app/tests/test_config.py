import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_settings_parse_env_lists(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000;http://127.0.0.1:5173")
    monkeypatch.setenv("LISTINGS_CSV_PATHS", "/data/a.csv,/data/b.csv")

    settings = Settings()

    assert settings.CORS_ORIGINS == ["http://localhost:3000", "http://127.0.0.1:5173"]
    assert settings.LISTINGS_CSV_PATHS == ["/data/a.csv", "/data/b.csv"]
    assert settings.RADIUS_EXPANSION_STEPS_M == [500, 1000, 2000, 5000, 10000, 15000]
    assert settings.TIER1_RADIUS_M == 500
    assert settings.TIER2_RADIUS_M == 2000
    assert settings.TIER3_RADIUS_M == 5000


def test_settings_normalize_environment_aliases(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("ENV", "prod")
    monkeypatch.setenv("LOG_JSON", "false")
    monkeypatch.setenv("CORS_ORIGINS", "https://valorai.example")
    monkeypatch.setenv("JWT_SECRET", "production-validation-secret-at-least-32-bytes")

    settings = Settings()

    assert settings.ENV == "production"
    assert settings.is_production is True
    assert settings.use_json_logs is True


def test_settings_require_explicit_jwt_secret_in_production(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("ENV", "production")
    monkeypatch.setenv("CORS_ORIGINS", "https://valorai.example")
    monkeypatch.setenv("JWT_SECRET", "local-development-secret-change-before-production")

    with pytest.raises(ValidationError, match="JWT_SECRET must be explicitly configured"):
        Settings()
