from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from app.api.routes.broker import router as broker_router
from app.api.routes.pricing import router as pricing_router
from app.api.routes.copilot import router as copilot_router
from app.api.routes.copilot_orchestrator import router as copilot_orchestrator_router
from app.api.routes.copilot_tools import router as copilot_tools_router
from app.core.config import settings
from app.core.error_handlers import register_exception_handlers
from app.core.logging import add_request_logging_middleware, setup_logging
from app.db.session import dispose_engine, wait_for_database

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "application_starting",
        extra={
            "environment": settings.ENV,
            "debug": settings.DEBUG,
            "json_logs": settings.use_json_logs,
            "db_startup_retries": settings.DB_STARTUP_RETRIES,
            "request_timeout_seconds": settings.API_REQUEST_TIMEOUT_SECONDS,
        },
    )
    wait_for_database()
    try:
        logger.info("application_ready", extra={"environment": settings.ENV})
        yield
    finally:
        logger.info("application_stopping", extra={"environment": settings.ENV})
        dispose_engine()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description="ValorAI deterministic governed valuation API for explainable real estate intelligence.",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
    add_request_logging_middleware(app)
    register_exception_handlers(app)

    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(pricing_router)
    app.include_router(broker_router)
    app.include_router(copilot_router)
    app.include_router(copilot_tools_router)
    app.include_router(copilot_orchestrator_router)
    return app


app = create_app()
