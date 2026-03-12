def test_get_total_value_empty_inventory(client):
    response = client.get("/products/total_value")
    assert response.status_code == 200
    data = response.json()
    assert data["Total Inventory Value $"] == 0.0


def test_get_total_value_with_products(client):
    # Create some products to populate the inventory
    # Create a product to associate the variant with
    create_product_response = client.post(
        "/products/",
        json={
            "category": "Tees",
            "name": "Test Garment",
            "color": "Teal",
            "price": 39.90,
            "collection": "SS26",
            "coming_soon": True,
        },
    )
    assert create_product_response.status_code == 201
    product_id = create_product_response.json()["id"]

    # Create a variant for that product
    client.post(
        f"/products/{product_id}/variants/",
        json={
            "size": "OS",
            "quantity": 10,
            "in_stock": True,
        },
    )
    response = client.get("/products/total_value")
    assert response.status_code == 200
    data = response.json()
    assert data["Total Inventory Value $"] == 399.00
