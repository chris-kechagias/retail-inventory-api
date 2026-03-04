"""
Application launcher.

Creates the FastAPI app, registers routers, and manages the database lifespan.
"""

# Standard Library Imports
import logging
from contextlib import asynccontextmanager

# Third-Party Imports
from fastapi import FastAPI

# Local/First-Party Imports
import logger_config  # noqa: F401
from config import config
from database import create_db_and_tables
from health import router as health_router
from home import router as home_router
from products import router as products_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles the application startup and shutdown events.

    Ensures the database engine is ready and tables are created before
    the API starts accepting traffic.
    """
    logger.info(
        "Lifespan Startup: Verifying database connectivity and creating tables."
    )
    # This ensures the database is ready before the first request arrives.
    create_db_and_tables()
    yield
    logger.info("Lifespan Shutdown: Cleaning up resources.")


app = FastAPI(
    title=config.app_name,
    description="A robust FastAPI service for managing warehouse stock using PostgreSQL and SQLModel.",
    version=config.version,
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(home_router)
app.include_router(products_router)
