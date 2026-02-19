"""
Database Infrastructure: Connection and Session Management.

This module configures the SQLAlchemy engine via SQLModel and defines
the dependency injection pattern used by the API endpoints to interact
with the PostgreSQL database.
"""

import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

# Load environment variables from .env file
load_dotenv()

# Retrieve the PostgreSQL connection string
DATABASE_URL = os.getenv("DATABASE_URL")
# The Engine is the 'source' of connectivity.
# echo=True logs all generated SQL statements to the terminal—great for debugging!
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """
    Scans all SQLModel classes with 'table=True' and creates them in PostgreSQL.

    This is called during the FastAPI 'lifespan' startup phase to ensure
    the database schema stays in sync with your Python models.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Provides a transactional scope for database operations.

    Yields a Session object and ensures it is properly closed after the
    request is finished, even if an error occurs.
    """
    # Use of Generator here so FastAPI can handle the 'teardown'.
    # This prevents the database from running out of connections.
    with Session(engine) as session:
        yield session


# SessionDep is a type alias that simplifies dependency injection in main.py.
# It tells FastAPI: "Whenever you see SessionDep, call get_session() and give me the result."
SessionDep = Annotated[Session, Depends(get_session)]