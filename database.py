"""
Database configuration for the Retail Inventory API.

Handles PostgreSQL connection using SQLModel.
"""

import os
from dotenv import load_dotenv
from typing import Annotated, Generator, Any
from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel

# Load environment variables from .env file
load_dotenv()

# Retrieve the secure URL
DATABASE_URL = os.getenv("DATABASE_URL")
# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """Create database tables based on the defined SQLModel models."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get a new database session."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
"""Dependency to inject a database session into FastAPI routes."""
