from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_cloud_connection():
    """Test that GET /products endpoint works on Cloud DB and returns  a 200 status."""
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

#def test_create_product():
#    """Test that POST /products actually creates a product."""
#    payload = {
#        "name": "Test Laptop",
#        "price": 999.99,
#        "quantity": 10,
#        "in_stock": True
#    }
#    response = client.post("/products", json=payload)
#    assert response.status_code == 201 
#    product_id = response.json()["id"]
#    assert product_id is not None
#    
#    print(f"Successfully created product {product_id} in the cloud!")
    