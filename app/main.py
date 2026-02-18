"""
API Gateway: FastAPI application entry point.

This module defines the RESTful endpoints for the Retail Inventory system.
It acts as the Presentation Layer, handling HTTP requests/responses and
orchestrating data persistence through SQLModel and PostgreSQL.
"""

# Standard Library Imports
import logging
import time
from contextlib import asynccontextmanager

# Third-Party Imports
from fastapi import FastAPI

# Local/First-Party Imports
import app.logger_config  # noqa: F401
from app.database import create_db_and_tables
from app.models import HealthResponse
from app.routers import products

# ----------------------------------------------------
# LOGGING & INITIALIZATION
# ----------------------------------------------------
START_TIME = time.time()


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles the application startup and shutdown events.

    Ensures the database engine is ready and tables are created before
    the API starts accepting traffic. This replaces the deprecated @app.on_event logic.
    """
    logger.info(
        "Lifespan Startup: Verifying database connectivity and creating tables."
    )
    # This replaces the old @app.on_event("startup") logic.
    # It ensures the database is ready before the first request arrives.
    create_db_and_tables()
    yield
    logger.info("Lifespan Shutdown: Cleaning up resources.")


app = FastAPI(
    title="Retail Inventory API",
    description="A robust FastAPI service for managing warehouse stock using PostgreSQL and SQLModel.",
    version="1.2.0",  # Updated to reflect Mock tests, input validation, structured JSON logging milestone
    lifespan=lifespan,
)

app.include_router(products.router)

@app.head("/health")
@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    return HealthResponse(
        status="healthy",
        version="1.2.0",
        uptime=time.time() - START_TIME
    )

@app.get("/")
def read_root():
    return {
        "message": "Retail Inventory API",
        "version": "1.2.0",
        "docs": "/docs",
        "endpoints": "/products"
    }