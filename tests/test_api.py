from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_cloud_connection():
    """Test that GET /products endpoint works on Cloud DB and returns  a 200 status."""
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_product():
    """Test that POST /products actually creates a product."""
    payload = {
        "name": "Test Laptop",
        "price": 999.99,
        "quantity": 10,
        "in_stock": True
    }
    response = client.post("/products", json=payload)
    assert response.status_code == 201 
    data = response.json()
    assert data["name"] == "Test Laptop"
    assert data["in_stock"] == True
    assert "id" in data

def test_read_single_product():
    """Test that GET /products/{product_id} returns a single product."""
    payload = {
        "name": "Single Test Item",
        "price": 25.00,
        "quantity": 7,
        "in_stock": True
    }
    create_response = client.post("/products", json=payload)
    product_id = create_response.json()["id"]

    read_response = client.get(f"/products/{product_id}")

    assert read_response.status_code == 200
    assert read_response.json()["name"] == "Single Test Item"
    assert read_response.json()["id"] == product_id

