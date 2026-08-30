def create_product(client, headers, stock=10):
    return client.post("/api/products", headers=headers, json={
        "sku": "DOG-001", "name": "Alimento", "price": "12.50", "stock": stock
    })


def test_admin_can_create_update_and_disable_product(client, admin_headers):
    created = create_product(client, admin_headers)
    assert created.status_code == 201
    product_id = created.get_json()["product"]["id"]
    updated = client.patch(f"/api/products/{product_id}", headers=admin_headers, json={"price": "13.75"})
    assert updated.status_code == 200
    assert updated.get_json()["product"]["price"] == "13.75"
    assert client.delete(f"/api/products/{product_id}", headers=admin_headers).status_code == 204
    listing = client.get("/api/products", headers=admin_headers).get_json()["products"]
    assert listing == []


def test_client_cannot_mutate_products(client, client_headers):
    response = create_product(client, client_headers)
    assert response.status_code == 403
    assert "administrador" in response.get_json()["error"]


def test_product_validation_and_duplicate_sku(client, admin_headers):
    assert create_product(client, admin_headers).status_code == 201
    assert create_product(client, admin_headers).status_code == 409
    invalid = client.post("/api/products", headers=admin_headers, json={
        "sku": "BAD", "name": "Inválido", "price": -1, "stock": 1
    })
    assert invalid.status_code == 400

