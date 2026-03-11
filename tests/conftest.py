# Third-Party Imports
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

# Local/First-Party Imports
from app.database import get_session
from main import app

engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)


@pytest.fixture(name="session")
def session_fixture():
    # create tables, yield session, drop tables
    with Session(engine) as session:
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
        yield session
        SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session):
    # override dependency, yield TestClient, clear override
    app.dependency_overrides[get_session] = lambda: session
    with TestClient(app, lifespan="off") as client:
        yield client
    app.dependency_overrides.clear()
