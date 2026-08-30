from tests.conftest import login


def test_register_and_login(client):
    response = client.post("/api/auth/register", json={
        "name": "Ana", "email": "ANA@example.com", "password": "segura123"
    })
    assert response.status_code == 201
    assert response.get_json()["user"]["role"] == "client"
    assert client.post("/api/auth/login", json={"email": "ana@example.com", "password": "segura123"}).status_code == 200


def test_rejects_duplicate_email_and_bad_password(client):
    duplicate = client.post("/api/auth/register", json={
        "name": "Otro", "email": "client@example.com", "password": "password123"
    })
    assert duplicate.status_code == 409
    bad_login = client.post("/api/auth/login", json={"email": "client@example.com", "password": "incorrecta"})
    assert bad_login.status_code == 401
    assert bad_login.get_json()["error"] == "Credenciales incorrectas"


def test_logout_revokes_token(client):
    headers = login(client, "client@example.com")
    assert client.post("/api/auth/logout", headers=headers).status_code == 200
    response = client.get("/api/products", headers=headers)
    assert response.status_code == 401
    assert response.get_json()["error"] == "Token revocado"


def test_protected_endpoint_requires_token(client):
    response = client.get("/api/products")
    assert response.status_code == 401

