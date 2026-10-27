import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.main import app
from backend.database import Base, get_db
from backend.models import User, View, Task, CompletionLog


@pytest.fixture(autouse=True)
def override_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    app.dependency_overrides[get_db] = lambda: db
    yield db
    db.close()
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


def test_register_success(client):
    response = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "securepassword123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "createdAt" in data

    # Check cookie
    assert "session" in response.cookies


def test_register_duplicate_email(client):
    payload = {"email": "test@example.com", "password": "securepassword123"}
    res1 = client.post("/api/auth/register", json=payload)
    assert res1.status_code == 201

    res2 = client.post("/api/auth/register", json=payload)
    assert res2.status_code == 400
    assert "Email already registered" in res2.json()["detail"]


def test_register_validation_errors(client):
    # Short password
    res = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "short"},
    )
    assert res.status_code == 400

    # Invalid email
    res2 = client.post(
        "/api/auth/register",
        json={"email": "notanemail", "password": "securepassword123"},
    )
    assert res2.status_code == 400


def test_login_success_and_me(client):
    payload = {"email": "user@example.com", "password": "mypassword123"}
    client.post("/api/auth/register", json=payload)

    # Clear client cookies to test login setting cookie
    client.cookies.clear()

    res_login = client.post("/api/auth/login", json=payload)
    assert res_login.status_code == 200
    data = res_login.json()
    assert data["email"] == "user@example.com"
    assert "session" in res_login.cookies

    # Test GET /api/auth/me with cookie
    res_me = client.get("/api/auth/me")
    assert res_me.status_code == 200
    assert res_me.json()["email"] == "user@example.com"


def test_login_invalid_credentials(client):
    payload = {"email": "user@example.com", "password": "mypassword123"}
    client.post("/api/auth/register", json=payload)
    client.cookies.clear()

    # Wrong password
    res = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "wrongpassword"},
    )
    assert res.status_code == 401

    # Non-existent user
    res2 = client.post(
        "/api/auth/login",
        json={"email": "nobody@example.com", "password": "mypassword123"},
    )
    assert res2.status_code == 401


def test_logout(client):
    payload = {"email": "logout@example.com", "password": "mypassword123"}
    client.post("/api/auth/register", json=payload)

    # Logout
    res_logout = client.post("/api/auth/logout")
    assert res_logout.status_code == 204

    # GET /api/auth/me should now fail
    res_me = client.get("/api/auth/me")
    assert res_me.status_code == 401


def test_me_unauthorized(client):
    res = client.get("/api/auth/me")
    assert res.status_code == 401
