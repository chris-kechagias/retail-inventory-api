from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database import get_session
from main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

def get_test_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

SQLModel.metadata.create_all(engine)
client = TestClient(app)

def test_create_product_isolated():
    response = client.post("/products/", json={
        "name": "Test Widget",
        "price": 9.99,
        "quantity": 71,
        "in_stock": True
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Widget"
    assert data["price"] == 9.99
    assert data["quantity"] == 71
    assert data["in_stock"] is True

def test_create_product_empty_name():
    response = client.post("/products/", json={
        "name": "",
        "price": 9.99,
        "quantity": 71,
        "in_stock": True
    })
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "name"]

def test_create_product_negative_price():
    response = client.post("/products/", json={
        "name": "Test Widget",
        "price": -5.00,
        "quantity": 71,
        "in_stock": True
    })
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "price"]


    