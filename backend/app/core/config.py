from __future__ import annotations

import json
import re
from typing import Annotated, Any

from pydantic import AliasChoices, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


def _split_env_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, tuple | set):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        raw = value.strip()
        if not raw:
            return []
        if raw.startswith("["):
            try:
                decoded = json.loads(raw)
            except json.JSONDecodeError:
                decoded = None
            if isinstance(decoded, list):
                return [str(item).strip() for item in decoded if str(item).strip()]
        return [item.strip() for item in re.split(r"[;,]", raw) if item.strip()]
    return [str(value).strip()]


def _split_env_int_list(value: Any) -> list[int]:
    return [int(item) for item in _split_env_list(value)]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    # App
    APP_NAME: str = Field(default="Fair Price Engine", description="FastAPI application name.")
    ENV: str = Field(default="dev", description="Runtime environment: dev, testing, staging, or production.")
    DEBUG: bool = Field(default=False, description="Enable debug response fields and verbose logs.")

    # Authentication
    JWT_SECRET: str = Field(
        default="local-development-secret-change-before-production",
        min_length=32,
        description="HMAC secret used to verify trusted bearer JWTs.",
    )
    JWT_ISSUER: str = Field(default="valorai", min_length=1, description="Required JWT issuer.")
    JWT_AUDIENCE: str = Field(default="valorai-api", min_length=1, description="Required JWT audience.")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, gt=0, description="ValorAI access token lifetime.")
    FIREBASE_PROJECT_ID: str | None = Field(default=None, description="Firebase project accepted by token exchange.")
    FIREBASE_CERT_URL: str = Field(
        default="https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com",
        description="Google certificate endpoint used to verify Firebase ID tokens.",
    )
    FIREBASE_CERT_CACHE_SECONDS: int = Field(default=3600, gt=0, description="Fallback Firebase certificate cache TTL.")

    # DB
    DATABASE_URL: str = Field(description="SQLAlchemy database URL.")
    DB_STARTUP_RETRIES: int = Field(default=10, ge=1, description="Database readiness retry attempts.")
    DB_STARTUP_RETRY_SECONDS: float = Field(default=1.0, gt=0, description="Seconds between DB retries.")

    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Python logging level.")
    LOG_JSON: bool = Field(default=False, description="Emit JSON logs when true.")

    # API reliability and safety
    API_REQUEST_TIMEOUT_SECONDS: float = Field(default=20.0, gt=0, description="Maximum API handler runtime.")
    MAX_REQUEST_BODY_BYTES: int = Field(default=64 * 1024, gt=0, description="Maximum accepted request body size.")
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="Enable in-process API rate limiting.")
    RATE_LIMIT_PER_MINUTE: int = Field(default=120, gt=0, description="Allowed requests per client and path window.")
    RATE_LIMIT_PATHS: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["/v1/rent/fair-price", "/v1/broker"],
        description="Path prefixes protected by in-process rate limiting.",
    )
    SLOW_QUERY_MS: float = Field(default=250.0, gt=0, description="DB queries slower than this emit warnings.")
    SLOW_REQUEST_MS: float = Field(default=1500.0, gt=0, description="API requests slower than this emit operational slow-request telemetry.")
    API_LATENCY_SLO_MS: float = Field(default=1200.0, gt=0, description="Staging SLO threshold for API p95 latency.")
    VALUATION_LATENCY_SLO_MS: float = Field(default=1500.0, gt=0, description="Staging SLO threshold for valuation p95 latency.")

    # CORS
    CORS_ORIGINS: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        description="Comma, semicolon, or JSON-list of browser origins allowed by CORS.",
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=False, description="Allow credentialed CORS requests.")
    CORS_ALLOW_METHODS: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["GET", "POST", "OPTIONS"],
        description="HTTP methods allowed by CORS.",
    )
    CORS_ALLOW_HEADERS: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["*"],
        description="HTTP headers allowed by CORS.",
    )

    # Comps selection defaults
    DEFAULT_RADIUS_KM: float = Field(default=2.0, gt=0, description="Default spatial search radius in km.")
    MAX_RADIUS_KM: float = Field(default=5.0, gt=0, description="Maximum spatial search radius in km.")
    RADIUS_EXPANSION_STEPS_M: Annotated[list[int], NoDecode] = Field(
        default_factory=lambda: [500, 1000, 2000, 5000, 10000, 15000],
        description="Deterministic comparable search radius progression in meters.",
    )
    TIER1_RADIUS_M: int = Field(default=500, gt=0, description="Legacy tier 1 radius in meters.")
    TIER2_RADIUS_M: int = Field(default=2000, gt=0, description="Tier 2 effective radius in meters.")
    TIER3_RADIUS_M: int = Field(default=5000, gt=0, description="Tier 3 effective radius in meters.")
    TIER4_RADIUS_M: int = Field(default=10000, gt=0, description="Tier 4 effective radius in meters.")
    TIER5_RADIUS_M: int = Field(default=15000, gt=0, description="Tier 5 effective radius in meters.")
    TIER_MATCH_THRESHOLD: int = Field(default=40, gt=0, description="Comps required before stopping expansion.")
    MIN_COMPS_REQUIRED: int = Field(default=10, gt=0, description="Minimum comps needed for valuation.")
    MAX_COMPS_RETURN: int = Field(default=800, gt=0, description="Hard cap for comparable rows.")
    TIER1_LIMIT: int = Field(default=600, gt=0, description="Tier 1 SQL row limit.")
    TIER2_LIMIT: int = Field(default=300, gt=0, description="Tier 2 SQL row limit.")
    TIER3_LIMIT: int = Field(default=800, gt=0, description="Tier 3 SQL row limit.")
    TIER4_LIMIT: int = Field(default=800, gt=0, description="Tier 4 SQL row limit.")
    TIER5_LIMIT: int = Field(default=800, gt=0, description="Tier 5 SQL row limit.")
    TIER1_STALE_DAYS: int = Field(default=90, gt=0, description="Tier 1 listing freshness window.")
    TIER2_STALE_DAYS: int = Field(default=120, gt=0, description="Tier 2 listing freshness window.")
    TIER3_STALE_DAYS: int = Field(default=180, gt=0, description="Tier 3 listing freshness window.")
    TIER4_STALE_DAYS: int = Field(default=270, gt=0, description="Tier 4 listing freshness window.")
    TIER5_STALE_DAYS: int = Field(default=365, gt=0, description="Tier 5 listing freshness window.")
    TIER1_SIZE_LOW: float = Field(default=0.85, gt=0, description="Tier 1 lower size multiplier.")
    TIER1_SIZE_HIGH: float = Field(default=1.15, gt=0, description="Tier 1 upper size multiplier.")
    TIER2_SIZE_LOW: float = Field(default=0.80, gt=0, description="Tier 2 lower size multiplier.")
    TIER2_SIZE_HIGH: float = Field(default=1.20, gt=0, description="Tier 2 upper size multiplier.")
    TIER3_SIZE_LOW: float = Field(default=0.80, gt=0, description="Tier 3 lower size multiplier.")
    TIER3_SIZE_HIGH: float = Field(default=1.20, gt=0, description="Tier 3 upper size multiplier.")
    TIER4_SIZE_LOW: float = Field(default=0.75, gt=0, description="Tier 4 lower size multiplier.")
    TIER4_SIZE_HIGH: float = Field(default=1.25, gt=0, description="Tier 4 upper size multiplier.")
    TIER5_SIZE_LOW: float = Field(default=0.70, gt=0, description="Tier 5 lower size multiplier.")
    TIER5_SIZE_HIGH: float = Field(default=1.30, gt=0, description="Tier 5 upper size multiplier.")

    # Hard guardrails
    MIN_PRICE_EGP: int = Field(default=1000, gt=0, description="Minimum monthly rent comp price.")
    MAX_PRICE_EGP: int = Field(default=500000, gt=0, description="Maximum monthly rent comp price.")
    MAX_TARGET_PRICE_EGP: int = Field(default=500000, gt=0, description="Maximum accepted target rent price.")
    MAX_SIZE_SQM: float = Field(default=1000.0, gt=0, description="Maximum accepted residential size.")
    MIN_PRICE_PER_SQM: float = Field(default=30.0, gt=0, description="Minimum accepted comp price per sqm.")
    MAX_PRICE_PER_SQM: float = Field(default=20000.0, gt=0, description="Maximum accepted comp price per sqm.")
    MAX_ROOM_COUNT: int = Field(default=20, gt=0, description="Maximum bedrooms or bathrooms accepted.")

    # Area resolution
    AREA_LOOKUP_MAX_RADIUS_M: int = Field(default=50000, gt=0, description="Max nearest-area search radius.")
    AREA_FALLBACK_RADIUS_DEFAULT_M: int = Field(default=2500, gt=0, description="Default leaf area radius.")
    AREA_LEVEL1_FALLBACK_RADIUS_M: int = Field(default=50000, gt=0, description="Governorate fallback radius.")
    AREA_LEVEL2_FALLBACK_RADIUS_M: int = Field(default=15000, gt=0, description="City fallback radius.")
    AREA_LEVEL3_FALLBACK_RADIUS_M: int = Field(default=6000, gt=0, description="District fallback radius.")
    AREA_LEVEL4_FALLBACK_RADIUS_M: int = Field(default=2500, gt=0, description="Neighborhood fallback radius.")
    AREA_AMBIGUITY_DISTANCE_M: float = Field(default=25.0, ge=0, description="Nearest-area distance delta that is treated as ambiguous.")
    GOOGLE_MAPS_API_KEY: str | None = Field(default=None, description="Google Maps API Key for geocoding.")
    ADDRESS_RESOLVER_VERSION: str = Field(default="3A.1b.1", description="Versioned deterministic address resolver contract.")
    ADDRESS_CACHE_EXTERNAL_TTL_DAYS: int = Field(default=30, gt=0, description="TTL for externally sourced address resolutions.")

    # Explainability
    TOP_COMPS_N: int = Field(default=10, gt=0, description="Number of top comparable listings returned.")

    # Broker orchestration
    BROKER_MAX_CONTEXT_TOKENS: int = Field(default=4000, gt=0, description="Maximum grounded context token budget.")
    BROKER_MAX_CONTEXT_COMPS: int = Field(default=5, gt=0, description="Comparable evidence items exposed to broker context.")
    BROKER_SESSION_HISTORY_LIMIT: int = Field(default=10, gt=0, description="Broker turns retained in lightweight session state.")
    BROKER_INTENT_FALLBACK_CONFIDENCE_THRESHOLD: float = Field(
        default=0.35,
        ge=0,
        le=1,
        description="Minimum classifier confidence before routing to deterministic-safe fallback.",
    )
    BROKER_REASONING_STAGE_TIMEOUT_MS: float = Field(
        default=5000.0,
        gt=0,
        description="Soft timeout budget used by broker reasoning stage telemetry.",
    )
    COPILOT_NARRATION_ENABLED: bool = Field(
        default=False,
        description="Enable the Phase 5.5C.6 Copilot Orchestrator narration pipeline.",
    )
    COPILOT_NARRATION_INTENTS: Annotated[list[str], NoDecode] = Field(
        default_factory=list,
        description="Explicit per-intent allowlist for governed narration activation.",
    )
    COPILOT_GEMINI_API_KEY: str | None = Field(
        default=None,
        description="Out-of-band Gemini API credential for the stateless Copilot narrator.",
    )
    COPILOT_GEMINI_DATA_GOVERNANCE_ACKNOWLEDGED: bool = Field(
        default=False,
        description="Operational acknowledgement that Gemini data-governance controls are configured.",
    )

    # Pricing statistics
    PRICE_RANGE_LOW_QUANTILE: float = Field(default=0.20, ge=0, le=1, description="Low range quantile.")
    PRICE_RANGE_HIGH_QUANTILE: float = Field(default=0.80, ge=0, le=1, description="High range quantile.")
    MAD_Z_THRESHOLD: float = Field(default=3.5, gt=0, description="MAD modified z-score cutoff.")
    MAD_MIN_SAMPLE_SIZE: int = Field(default=10, gt=0, description="Minimum samples before MAD filtering.")
    MAD_MODIFIED_Z_SCALE: float = Field(default=0.6745, gt=0, description="MAD modified z-score scale.")
    MAD_ZERO_TOLERANCE_RATIO: float = Field(default=0.05, ge=0, description="Tolerance ratio used when MAD is zero.")

    # Weighting
    DISTANCE_WEIGHT_FALLBACK: float = Field(default=0.2, ge=0, description="Weight when comp distance is missing.")
    DISTANCE_DECAY_M: float = Field(default=1000.0, gt=0, description="Distance decay denominator.")
    SIZE_WEIGHT_FALLBACK: float = Field(default=0.6, ge=0, description="Weight when comp size is missing.")
    SIZE_WEIGHT_MIN: float = Field(default=0.05, ge=0, description="Minimum size similarity weight.")
    RECENCY_WEIGHT_FALLBACK: float = Field(default=0.6, ge=0, description="Weight when comp recency is missing.")
    RECENCY_DECAY_DAYS: float = Field(default=60.0, gt=0, description="Recency decay denominator.")
    BATHROOM_WEIGHT_FALLBACK: float = Field(default=0.85, ge=0, le=1, description="Weight when bathroom match data is missing.")
    BATHROOM_MISMATCH_WEIGHT: float = Field(default=0.50, ge=0, le=1, description="Weight when bathroom count is known and mismatched.")
    NON_SAME_AREA_WEIGHT: float = Field(default=0.95, ge=0, le=1, description="Weight for fallback-tier comps outside the resolved leaf area.")
    FEATURE_WEIGHT_MAX_DELTA: float = Field(default=0.08, ge=0, le=0.10, description="Maximum conservative feature-similarity influence.")

    # Confidence scoring
    CONFIDENCE_HIGH_THRESHOLD: float = Field(default=0.75, ge=0, le=1, description="High confidence threshold.")
    CONFIDENCE_MEDIUM_THRESHOLD: float = Field(default=0.50, ge=0, le=1, description="Medium confidence threshold.")
    CONFIDENCE_COUNT_HIGH: int = Field(default=80, gt=0, description="High comp count threshold.")
    CONFIDENCE_COUNT_MEDIUM: int = Field(default=40, gt=0, description="Medium comp count threshold.")
    CONFIDENCE_COUNT_LOW: int = Field(default=20, gt=0, description="Low comp count threshold.")
    CONFIDENCE_COUNT_HIGH_SCORE: float = Field(default=0.35, ge=0, le=1)
    CONFIDENCE_COUNT_MEDIUM_SCORE: float = Field(default=0.25, ge=0, le=1)
    CONFIDENCE_COUNT_LOW_SCORE: float = Field(default=0.15, ge=0, le=1)
    CONFIDENCE_COUNT_FALLBACK_SCORE: float = Field(default=0.05, ge=0, le=1)
    CONFIDENCE_TIER1_SCORE: float = Field(default=0.25, ge=0, le=1)
    CONFIDENCE_TIER2_SCORE: float = Field(default=0.18, ge=0, le=1)
    CONFIDENCE_TIER3_SCORE: float = Field(default=0.10, ge=0, le=1)
    CONFIDENCE_TIER4_SCORE: float = Field(default=0.06, ge=0, le=1)
    CONFIDENCE_TIER5_SCORE: float = Field(default=0.03, ge=0, le=1)
    CONFIDENCE_KEPT_RATIO_BASELINE: float = Field(default=0.6, ge=0, le=1)
    CONFIDENCE_KEPT_RATIO_MAX_SCORE: float = Field(default=0.20, ge=0, le=1)
    CONFIDENCE_DISPERSION_LOW: float = Field(default=0.35, ge=0)
    CONFIDENCE_DISPERSION_MEDIUM: float = Field(default=0.60, ge=0)
    CONFIDENCE_DISPERSION_LOW_SCORE: float = Field(default=0.20, ge=0, le=1)
    CONFIDENCE_DISPERSION_MEDIUM_SCORE: float = Field(default=0.12, ge=0, le=1)
    CONFIDENCE_DISPERSION_FALLBACK_SCORE: float = Field(default=0.05, ge=0, le=1)

    # Bootstrap data import
    LISTINGS_CSV_PATHS: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: [
            "/data/rent_residential.csv",
            "/data/buy_clean.csv",
            "/data/commercial_buy_clean.csv",
            "/data/commercial_rent_clean.csv",
        ],
        validation_alias=AliasChoices("LISTINGS_CSV_PATHS", "LISTINGS_CSV_FILES", "RENT_CSV_PATH"),
        description="CSV files used by the bootstrap importer.",
    )
    CSV_INSERT_CHUNK_SIZE: int = Field(default=1000, gt=0, description="Bootstrap staging insert batch size.")

    @field_validator(
        "CORS_ORIGINS",
        "CORS_ALLOW_METHODS",
        "CORS_ALLOW_HEADERS",
        "LISTINGS_CSV_PATHS",
        "RATE_LIMIT_PATHS",
        "COPILOT_NARRATION_INTENTS",
        mode="before",
    )
    @classmethod
    def parse_env_list(cls, value: Any) -> list[str]:
        return _split_env_list(value)

    @field_validator("RADIUS_EXPANSION_STEPS_M", mode="before")
    @classmethod
    def parse_radius_steps(cls, value: Any) -> list[int]:
        return _split_env_int_list(value)

    @field_validator("RADIUS_EXPANSION_STEPS_M")
    @classmethod
    def validate_radius_steps(cls, value: list[int]) -> list[int]:
        if len(value) != 6:
            raise ValueError("RADIUS_EXPANSION_STEPS_M must contain exactly 6 radius steps")
        if any(step <= 0 for step in value):
            raise ValueError("RADIUS_EXPANSION_STEPS_M values must be positive")
        if value != sorted(value) or len(set(value)) != len(value):
            raise ValueError("RADIUS_EXPANSION_STEPS_M must be strictly increasing")
        if value[-1] > 15000:
            raise ValueError("RADIUS_EXPANSION_STEPS_M cannot exceed 15000 meters")
        return value

    @field_validator("LOG_LEVEL", mode="before")
    @classmethod
    def normalize_log_level(cls, value: Any) -> str:
        level = str(value or "INFO").upper()
        allowed = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"}
        if level not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {sorted(allowed)}")
        return level

    @field_validator("ENV", mode="before")
    @classmethod
    def normalize_environment(cls, value: Any) -> str:
        env = str(value or "dev").strip().lower()
        aliases = {
            "development": "dev",
            "local": "dev",
            "test": "testing",
            "tests": "testing",
            "stage": "staging",
            "prod": "production",
        }
        env = aliases.get(env, env)
        allowed = {"dev", "testing", "staging", "production"}
        if env not in allowed:
            raise ValueError(f"ENV must be one of {sorted(allowed)}")
        return env

    @model_validator(mode="after")
    def validate_environment_safety(self):
        if self.DEBUG and self.ENV == "production":
            raise ValueError("DEBUG must be false in production")
        if self.ENV in {"staging", "production"} and self.JWT_SECRET == "local-development-secret-change-before-production":
            raise ValueError("JWT_SECRET must be explicitly configured in staging and production")
        if self.CORS_ALLOW_CREDENTIALS and "*" in self.CORS_ORIGINS:
            raise ValueError("CORS_ORIGINS cannot contain '*' when credentials are enabled")
        if self.ENV in {"staging", "production"} and "*" in self.CORS_ORIGINS:
            raise ValueError("Wildcard CORS origins are not allowed in staging or production")
        approved_narration_intents = {
            "VALUATION",
            "EXPLAINABILITY",
            "COMPARABLES",
            "FAIRNESS",
            "WHAT_IF",
            "NEGOTIATION",
            "INVESTMENT",
            "MARKET_INSIGHT",
            "PROPERTY_COMPARISON",
        }
        unknown_narration_intents = set(self.COPILOT_NARRATION_INTENTS) - approved_narration_intents
        if unknown_narration_intents:
            raise ValueError(
                f"COPILOT_NARRATION_INTENTS contains unapproved intent(s): {sorted(unknown_narration_intents)}"
            )
        if self.COPILOT_NARRATION_ENABLED:
            if not self.COPILOT_NARRATION_INTENTS:
                raise ValueError("COPILOT_NARRATION_INTENTS must explicitly allow at least one approved intent")
            if not self.COPILOT_GEMINI_API_KEY:
                raise ValueError("COPILOT_GEMINI_API_KEY must be configured when Copilot narration is enabled")
            if not self.COPILOT_GEMINI_DATA_GOVERNANCE_ACKNOWLEDGED:
                raise ValueError(
                    "COPILOT_GEMINI_DATA_GOVERNANCE_ACKNOWLEDGED must be true when Copilot narration is enabled"
                )
        return self

    @property
    def is_production(self) -> bool:
        return self.ENV == "production"

    @property
    def is_testing(self) -> bool:
        return self.ENV == "testing"

    @property
    def use_json_logs(self) -> bool:
        return self.LOG_JSON or self.ENV in {"staging", "production"}


settings = Settings()
