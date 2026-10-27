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


def test_history_unauthorized(client):
    response = client.get("/api/history")
    assert response.status_code == 401


def test_history_empty(client):
    client.post(
        "/api/auth/register",
        json={"email": "histuser@example.com", "password": "securepassword123"},
    )
    response = client.get("/api/history")
    assert response.status_code == 200
    assert response.json() == []


def test_history_aggregation(client, override_db):
    client.post(
        "/api/auth/register",
        json={"email": "histuser2@example.com", "password": "securepassword123"},
    )
    view_res = client.post(
        "/api/views",
        json={"name": "Daily Goals", "cadence": "daily"},
    )
    view_id = view_res.json()["id"]

    task_res = client.post(
        f"/api/views/{view_id}/tasks",
        json={"title": "Exercise"},
    )
    task_id = task_res.json()["id"]

    # Add completion log for a past period
    db = override_db
    log = CompletionLog(task_id=task_id, period_key="d:2026-10-25", done=True)
    db.add(log)
    db.commit()

    response = client.get("/api/history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["view"]["id"] == view_id
    assert len(data[0]["periods"]) == 1
    assert data[0]["periods"][0]["key"] == "d:2026-10-25"
    assert len(data[0]["periods"][0]["tasks"]) == 1
    assert data[0]["periods"][0]["tasks"][0]["id"] == task_id
    assert data[0]["periods"][0]["tasks"][0]["done"] is True
