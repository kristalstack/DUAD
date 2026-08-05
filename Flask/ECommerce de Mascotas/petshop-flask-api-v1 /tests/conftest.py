import pytest

from app import create_app
from app.extensions import db
from app.models import User


@pytest.fixture()
def app():
    application = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "CACHE_TYPE": "SimpleCache",
        "JWT_SECRET_KEY": "test-secret",
    })
    with application.app_context():
        db.create_all()
        admin = User(name="Admin", email="admin@example.com", role="admin")
        admin.set_password("password123")
        client_user = User(name="Cliente", email="client@example.com", role="client")
        client_user.set_password("password123")
        db.session.add_all([admin, client_user])
        db.session.commit()
    yield application
    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client, email):
    response = client.post("/api/auth/login", json={"email": email, "password": "password123"})
    return {"Authorization": f"Bearer {response.get_json()['access_token']}"}


@pytest.fixture()
def admin_headers(client):
    return login(client, "admin@example.com")


@pytest.fixture()
def client_headers(client):
    return login(client, "client@example.com")

