from tests.test_sales import setup_sale


def complete_sale(client, admin_headers, client_headers):
    product, address, cart = setup_sale(client, admin_headers, client_headers)
    client.put(
        f"/api/carts/{cart['id']}/items/{product['id']}",
        headers=client_headers,
        json={"quantity": 1},
    )
    response = client.post(
        f"/api/carts/{cart['id']}/checkout",
        headers=client_headers,
        json={
            "address_id": address["id"],
            "payment_method": "SINPE",
            "payment_reference": "INVOICE-TEST",
        },
    )
    assert response.status_code == 201
    return response.get_json()["invoice"]


def test_client_and_admin_can_list_invoices(client, admin_headers, client_headers):
    invoice = complete_sale(client, admin_headers, client_headers)

    client_response = client.get("/api/invoices", headers=client_headers)
    assert client_response.status_code == 200
    assert [item["number"] for item in client_response.get_json()["invoices"]] == [invoice["number"]]

    admin_response = client.get("/api/invoices", headers=admin_headers)
    assert admin_response.status_code == 200
    assert [item["number"] for item in admin_response.get_json()["invoices"]] == [invoice["number"]]


def test_only_admin_can_update_invoice_and_cache_is_invalidated(
    client, admin_headers, client_headers
):
    invoice = complete_sale(client, admin_headers, client_headers)
    number = invoice["number"]

    # Prime the invoice cache before changing its status.
    cached = client.get(f"/api/invoices/{number}", headers=client_headers)
    assert cached.get_json()["invoice"]["status"] == "paid"

    forbidden = client.patch(
        f"/api/invoices/{number}",
        headers=client_headers,
        json={"status": "cancelled"},
    )
    assert forbidden.status_code == 403

    updated = client.patch(
        f"/api/invoices/{number}",
        headers=admin_headers,
        json={"status": "cancelled"},
    )
    assert updated.status_code == 200
    assert updated.get_json()["invoice"]["status"] == "cancelled"

    refreshed = client.get(f"/api/invoices/{number}", headers=client_headers)
    assert refreshed.get_json()["invoice"]["status"] == "cancelled"


def test_update_invoice_rejects_invalid_status(client, admin_headers, client_headers):
    invoice = complete_sale(client, admin_headers, client_headers)
    response = client.patch(
        f"/api/invoices/{invoice['number']}",
        headers=admin_headers,
        json={"status": "unknown"},
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Estado de factura inválido"
