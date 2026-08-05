from app.extensions import db
from app.models import Product


def setup_sale(client, admin_headers, client_headers, stock=5):
    product = client.post("/api/products", headers=admin_headers, json={
        "sku": "CAT-001", "name": "Arena", "price": "8.00", "stock": stock
    }).get_json()["product"]
    user_id = client.get("/api/users/2", headers=client_headers).get_json()["user"]["id"]
    address = client.post(f"/api/users/{user_id}/addresses", headers=client_headers, json={
        "recipient": "Cliente", "line1": "Calle 1", "city": "San José", "province": "San José"
    }).get_json()["address"]
    cart = client.post("/api/carts", headers=client_headers).get_json()["cart"]
    return product, address, cart


def test_checkout_reduces_stock_and_return_restores_it(client, app, admin_headers, client_headers):
    product, address, cart = setup_sale(client, admin_headers, client_headers)
    assert client.put(f"/api/carts/{cart['id']}/items/{product['id']}", headers=client_headers, json={"quantity": 2}).status_code == 200
    checkout = client.post(f"/api/carts/{cart['id']}/checkout", headers=client_headers, json={
        "address_id": address["id"], "payment_method": "SINPE", "payment_reference": "SINPE-123"
    })
    assert checkout.status_code == 201
    invoice = checkout.get_json()["invoice"]
    assert invoice["total"] == "16.00"
    with app.app_context():
        assert db.session.get(Product, product["id"]).stock == 3
    invoice_item_id = invoice["items"][0]["id"]
    returned = client.post(f"/api/invoices/{invoice['number']}/returns", headers=client_headers, json={
        "reason": "Producto sin abrir", "items": [{"invoice_item_id": invoice_item_id, "quantity": 2}]
    })
    assert returned.status_code == 201
    assert returned.get_json()["invoice"]["status"] == "refunded"
    with app.app_context():
        assert db.session.get(Product, product["id"]).stock == 5


def test_checkout_revalidates_stock(client, app, admin_headers, client_headers):
    product, address, cart = setup_sale(client, admin_headers, client_headers, stock=2)
    client.put(f"/api/carts/{cart['id']}/items/{product['id']}", headers=client_headers, json={"quantity": 2})
    with app.app_context():
        db.session.get(Product, product["id"]).stock = 1
        db.session.commit()
    response = client.post(f"/api/carts/{cart['id']}/checkout", headers=client_headers, json={
        "address_id": address["id"], "payment_method": "SINPE", "payment_reference": "REF"
    })
    assert response.status_code == 409
    assert "Stock insuficiente" in response.get_json()["error"]


def test_user_cannot_read_another_users_cart(client, admin_headers, client_headers):
    cart = client.post("/api/carts", headers=client_headers).get_json()["cart"]
    second = client.post("/api/auth/register", json={"name": "Otro", "email": "otro@example.com", "password": "password123"})
    other_headers = {"Authorization": f"Bearer {second.get_json()['access_token']}"}
    assert client.get(f"/api/carts/{cart['id']}", headers=other_headers).status_code == 403


def test_return_cannot_exceed_purchase(client, admin_headers, client_headers):
    product, address, cart = setup_sale(client, admin_headers, client_headers)
    client.put(f"/api/carts/{cart['id']}/items/{product['id']}", headers=client_headers, json={"quantity": 1})
    invoice = client.post(f"/api/carts/{cart['id']}/checkout", headers=client_headers, json={
        "address_id": address["id"], "payment_method": "SINPE", "payment_reference": "REF"
    }).get_json()["invoice"]
    response = client.post(f"/api/invoices/{invoice['number']}/returns", headers=client_headers, json={
        "reason": "Error", "items": [{"invoice_item_id": invoice["items"][0]["id"], "quantity": 2}]
    })
    assert response.status_code == 409

