def address_payload(**overrides):
    data = {
        "recipient": "Cliente",
        "line1": "Calle 1",
        "city": "San José",
        "province": "San José",
        "country": "CR",
    }
    data.update(overrides)
    return data


def test_address_crud_normalizes_country(client, client_headers):
    created = client.post(
        "/api/users/2/addresses",
        headers=client_headers,
        json=address_payload(country=" cr "),
    )
    assert created.status_code == 201
    address = created.get_json()["address"]
    assert address["country"] == "CR"

    listing = client.get("/api/users/2/addresses", headers=client_headers)
    assert listing.status_code == 200
    assert [item["id"] for item in listing.get_json()["addresses"]] == [address["id"]]

    updated = client.patch(
        f"/api/users/2/addresses/{address['id']}",
        headers=client_headers,
        json={"country": "us", "city": "Heredia"},
    )
    assert updated.status_code == 200
    assert updated.get_json()["address"]["country"] == "US"
    assert updated.get_json()["address"]["city"] == "Heredia"

    deleted = client.delete(
        f"/api/users/2/addresses/{address['id']}",
        headers=client_headers,
    )
    assert deleted.status_code == 204


def test_create_address_rejects_invalid_country(client, client_headers):
    response = client.post(
        "/api/users/2/addresses",
        headers=client_headers,
        json=address_payload(country="Costa Rica"),
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "country debe ser un código de país de 2 letras"


def test_update_address_rejects_invalid_country(client, client_headers):
    address = client.post(
        "/api/users/2/addresses",
        headers=client_headers,
        json=address_payload(),
    ).get_json()["address"]
    response = client.patch(
        f"/api/users/2/addresses/{address['id']}",
        headers=client_headers,
        json={"country": "123"},
    )
    assert response.status_code == 400


def test_client_cannot_manage_another_users_addresses(client, client_headers):
    registered = client.post(
        "/api/auth/register",
        json={"name": "Otro", "email": "otro@example.com", "password": "password123"},
    )
    other_id = registered.get_json()["user"]["id"]
    response = client.post(
        f"/api/users/{other_id}/addresses",
        headers=client_headers,
        json=address_payload(),
    )
    assert response.status_code == 403

