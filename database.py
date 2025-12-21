"""
Database configuration for the Retail Inventory API.

Handles PostgreSQL connection using SQLModel.
"""

from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel

# Connection string to PostgreSQL database
DATABASE_URL = "postgresql+psycopg2://user:..Mystis_7337@localhost/retail_inventory"

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
