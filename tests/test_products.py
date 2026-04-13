def test_create_product_isolated(client):
    response = client.post(
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
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Garment"
    assert data["color"] == "Teal"
    assert data["price"] == 39.90
    assert data["collection"] == "SS26"
    assert data["coming_soon"] is True


def test_create_product_invalid_missing_fields(client):
    response = client.post(
        "/products/",
        json={
            "category": "Tees",
            "color": "Teal",
            "price": 39.90,
            "collection": "SS26",
            "coming_soon": True,
        },
    )
    assert response.status_code == 422
    data = response.json()
    errors = data["error"]["details"]["errors"]
    assert errors[0]["loc"] == [
        "body",
        "name",
    ]  # Check that the error is about the missing 'name' field


def test_create_product_invalid_category(client):
    response = client.post(
        "/products/",
        json={
            "category": "Socks",  # Invalid category not in the predefined list
            "name": "Test Garment",
            "color": "Teal",
            "price": 39.90,
            "collection": "SS26",
            "coming_soon": True,
        },
    )
    assert response.status_code == 422
    data = response.json()
    errors = data["error"]["details"]["errors"]
    assert errors[0]["loc"] == [
        "body",
        "category",
    ]  # Check that the error is about the invalid 'category' value


def test_create_product_invalid_negative_price(client):
    response = client.post(
        "/products/",
        json={
            "category": "Tees",
            "name": "Test Garment",
            "color": "Teal",
            "price": -11.90,  # Invalid negative price
            "collection": "SS26",
            "coming_soon": True,
        },
    )
    assert response.status_code == 422
    data = response.json()
    errors = data["error"]["details"]["errors"]
    assert errors[0]["loc"] == [
        "body",
        "price",
    ]  # Check that the error is about the invalid 'price' value


def test_get_all_products(client):
    # Empty list case
    response = client.get("/products/")
    assert response.status_code == 200
    assert response.json() == []

    # Add a product to test retrieval
    client.post(
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
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Garment"


def test_get_product_found(client):
    # Create a product to retrieve
    create_response = client.post(
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
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    # Retrieve the product
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Test Garment"


def test_get_product_not_found(client):
    response = client.get(
        "/products/00000000-0000-0000-0000-000000000000"
    )  # Assuming this ID does not exist
    assert response.status_code == 404
    data = response.json()
    assert data["error"]["code"] == "PRODUCT_NOT_FOUND"


def test_update_product_success(client):
    # Create a product to update
    create_response = client.post(
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
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    # Update the product
    update_response = client.patch(
        f"/products/{product_id}",
        json={
            "name": "Updated Garment",
            "price": 49.90,
        },
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["id"] == product_id
    assert data["name"] == "Updated Garment"
    assert data["price"] == 49.90


def test_update_product_invalid_data(client):
    # Create a product to update
    create_response = client.post(
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
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    # Attempt to update with invalid data (negative price)
    update_response = client.patch(
        f"/products/{product_id}",
        json={
            "price": -10.00,  # Invalid negative price
        },
    )
    assert update_response.status_code == 422
    data = update_response.json()
    errors = data["error"]["details"]["errors"]
    assert errors[0]["loc"] == [
        "body",
        "price",
    ]  # Check that the error is about the invalid 'price' value


def test_update_product_not_found(client):
    update_response = client.patch(
        "/products/00000000-0000-0000-0000-000000000000",  # Assuming this ID does not exist
        json={
            "name": "Updated Garment",
            "price": 49.90,
        },
    )
    assert update_response.status_code == 404
    data = update_response.json()
    assert data["error"]["code"] == "PRODUCT_NOT_FOUND"


def test_delete_product_success(client):
    # Create a product to delete
    create_response = client.post(
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
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    # Delete the product
    delete_response = client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 204

    # Verify the product is deleted
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404
    data = get_response.json()
    assert data["error"]["code"] == "PRODUCT_NOT_FOUND"


def test_delete_product_not_found(client):
    delete_response = client.delete(
        "/products/00000000-0000-0000-0000-000000000000"
    )  # Assuming this ID does not exist
    assert delete_response.status_code == 404
    data = delete_response.json()
    assert data["error"]["code"] == "PRODUCT_NOT_FOUND"
