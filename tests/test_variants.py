def test_create_variant_success(client):
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
    create_variant_response = client.post(
        f"/products/{product_id}/variants/",
        json={
            "size": "OS",
            "quantity": 10,
            "in_stock": True,
        },
    )
    assert create_variant_response.status_code == 201
    variant_data = create_variant_response.json()
    assert variant_data["size"] == "OS"
    assert variant_data["quantity"] == 10
    assert variant_data["in_stock"] is True


def test_create_variant_product_invalid_size(client):
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

    # Attempt to create a variant with an invalid size
    create_variant_response = client.post(
        f"/products/{product_id}/variants/",
        json={
            "size": "XXL",  # Invalid size, should be one of the predefined sizes
            "quantity": 10,
            "in_stock": True,
        },
    )
    assert create_variant_response.status_code == 422
    data = create_variant_response.json()
    errors = data["error"]["details"]["errors"]
    assert errors[0]["loc"] == [
        "body",
        "size",
    ]  # Check that the error is about the invalid 'size' field


def test_create_variant_product_invalid_quantity(client):
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

    # Attempt to create a variant with an invalid quantity
    create_variant_response = client.post(
        f"/products/{product_id}/variants/",
        json={
            "size": "OS",
            "quantity": -5,  # Invalid quantity, should be non-negative
            "in_stock": True,
        },
    )
    assert create_variant_response.status_code == 422
    data = create_variant_response.json()
    errors = data["error"]["details"]["errors"]
    assert errors[0]["loc"] == [
        "body",
        "quantity",
    ]  # Check that the error is about the invalid 'quantity' field


def test_create_variant_product_not_found(client):
    # Attempt to create a variant for a non-existent product
    create_variant_response = client.post(
        "/products/9999/variants/",  # Assuming this product ID does not exist
        json={
            "size": "OS",
            "quantity": 10,
            "in_stock": True,
        },
    )
    assert create_variant_response.status_code == 404
    data = create_variant_response.json()
    assert data["error"]["code"] == "PRODUCT_NOT_FOUND"


def test_get_variants(client):
    # Create a product to associate the variants with
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

    # Initially, there should be no variants
    get_variants_response = client.get(f"/products/{product_id}/variants/")
    assert get_variants_response.status_code == 200
    data = get_variants_response.json()
    assert isinstance(data, list)
    assert len(data) == 0

    # Create a variant for that product
    create_variant_response = client.post(
        f"/products/{product_id}/variants/",
        json={
            "size": "OS",
            "quantity": 10,
            "in_stock": True,
        },
    )
    assert create_variant_response.status_code == 201

    # Now there should be one variant
    get_variants_response = client.get(f"/products/{product_id}/variants/")
    assert get_variants_response.status_code == 200
    data = get_variants_response.json()
    assert isinstance(data, list)
    assert len(data) == 1


def test_get_variants_product_not_found(client):
    # Attempt to get variants for a non-existent product
    get_variants_response = client.get(
        "/products/9999/variants/"
    )  # Assuming this product ID does not exist
    assert get_variants_response.status_code == 404
    data = get_variants_response.json()
    assert data["error"]["code"] == "PRODUCT_NOT_FOUND"


def test_update_variant_success(client):
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
    create_variant_response = client.post(
        f"/products/{product_id}/variants/",
        json={
            "size": "OS",
            "quantity": 10,
            "in_stock": True,
        },
    )
    assert create_variant_response.status_code == 201
    variant_id = create_variant_response.json()["id"]

    # Update the variant's quantity and in_stock status
    update_variant_response = client.patch(
        f"/products/{product_id}/variants/{variant_id}",
        json={
            "quantity": 5,
            "in_stock": False,
        },
    )
    assert update_variant_response.status_code == 200
    updated_data = update_variant_response.json()
    assert updated_data["quantity"] == 5
    assert updated_data["in_stock"] is False


def test_update_variant_invalid_data(client):
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
    create_variant_response = client.post(
        f"/products/{product_id}/variants/",
        json={
            "size": "OS",
            "quantity": 10,
            "in_stock": True,
        },
    )
    assert create_variant_response.status_code == 201
    variant_id = create_variant_response.json()["id"]

    # Attempt to update the variant with invalid quantity
    update_variant_response = client.patch(
        f"/products/{product_id}/variants/{variant_id}",
        json={
            "quantity": -5,  # Invalid quantity, should be non-negative
        },
    )
    assert update_variant_response.status_code == 422
    data = update_variant_response.json()
    errors = data["error"]["details"]["errors"]
    assert errors[0]["loc"] == [
        "body",
        "quantity",
    ]  # Check that the error is about the invalid 'quantity' field


def test_update_variant_not_found(client):
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

    # Attempt to update a non-existent variant
    update_variant_response = client.patch(
        f"/products/{product_id}/variants/9999",  # Assuming this variant ID does not exist
        json={
            "quantity": 5,
            "in_stock": False,
        },
    )
    assert update_variant_response.status_code == 404
    data = update_variant_response.json()
    assert data["error"]["code"] == "VARIANT_NOT_FOUND"


def test_update_variant_product_not_found(client):
    # Attempt to update a variant for a non-existent product
    update_variant_response = client.patch(
        "/products/9999/variants/1",  # Assuming this product ID does not exist
        json={
            "quantity": 5,
            "in_stock": False,
        },
    )
    assert update_variant_response.status_code == 404
    data = update_variant_response.json()
    assert data["error"]["code"] == "PRODUCT_NOT_FOUND"


def test_delete_variant_success(client):
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
    create_variant_response = client.post(
        f"/products/{product_id}/variants/",
        json={
            "size": "OS",
            "quantity": 10,
            "in_stock": True,
        },
    )
    assert create_variant_response.status_code == 201
    variant_id = create_variant_response.json()["id"]

    # Delete the variant
    delete_variant_response = client.delete(
        f"/products/{product_id}/variants/{variant_id}"
    )
    assert delete_variant_response.status_code == 204

    # Attempt to get the deleted variant to confirm it's gone
    get_variant_response = client.get(f"/products/{product_id}/variants/")
    assert get_variant_response.status_code == 200
    assert get_variant_response.json() == []


def test_delete_variant_not_found(client):
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
    # Attempt to delete a non-existent variant
    delete_variant_response = client.delete(
        f"/products/{product_id}/variants/9999"  # Assuming this variant ID does not exist
    )
    assert delete_variant_response.status_code == 404
    data = delete_variant_response.json()
    assert data["error"]["code"] == "VARIANT_NOT_FOUND"


def test_delete_variant_product_not_found(client):
    # Attempt to delete a variant for a non-existent product
    delete_variant_response = client.delete(
        "/products/9999/variants/1"  # Assuming this product ID does not exist
    )
    assert delete_variant_response.status_code == 404
    data = delete_variant_response.json()
    assert data["error"]["code"] == "PRODUCT_NOT_FOUND"
