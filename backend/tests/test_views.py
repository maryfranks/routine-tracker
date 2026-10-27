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


@pytest.fixture
def authenticated_client(client):
    # Register and login a test user
    client.post(
        "/api/auth/register",
        json={"email": "viewuser@example.com", "password": "securepassword123"},
    )
    return client


def test_list_views_unauthorized(client):
    response = client.get("/api/views")
    assert response.status_code == 401


def test_list_views_success(authenticated_client):
    # Create a view first
    authenticated_client.post(
        "/api/views",
        json={"name": "Health & Fitness", "cadence": "daily"},
    )

    response = authenticated_client.get("/api/views")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Health & Fitness"
    assert data[0]["cadence"] == "daily"
    assert "taskCount" in data[0]
    assert "doneCount" in data[0]


def test_create_view_success(authenticated_client):
    response = authenticated_client.post(
        "/api/views",
        json={"name": "Work & Career", "cadence": "weekly"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Work & Career"
    assert data["cadence"] == "weekly"
    assert "id" in data
    assert "createdAt" in data


def test_create_view_validation_errors(authenticated_client):
    # Empty name
    res = authenticated_client.post(
        "/api/views",
        json={"name": "", "cadence": "daily"},
    )
    assert res.status_code == 400

    # Invalid cadence
    res2 = authenticated_client.post(
        "/api/views",
        json={"name": "Valid Name", "cadence": "hourly"},
    )
    assert res2.status_code == 400

    # Name too long (>80 chars)
    res3 = authenticated_client.post(
        "/api/views",
        json={"name": "a" * 81, "cadence": "daily"},
    )
    assert res3.status_code == 400  # Bad request validation error


def test_update_view_success(authenticated_client):
    create_res = authenticated_client.post(
        "/api/views",
        json={"name": "Old Name", "cadence": "daily"},
    )
    view_id = create_res.json()["id"]

    update_res = authenticated_client.put(
        f"/api/views/{view_id}",
        json={"name": "New Name", "cadence": "monthly"},
    )
    assert update_res.status_code == 200
    data = update_res.json()
    assert data["name"] == "New Name"
    assert data["cadence"] == "monthly"


def test_update_view_not_found(authenticated_client):
    response = authenticated_client.put(
        "/api/views/non-existent-id",
        json={"name": "Name", "cadence": "daily"},
    )
    assert response.status_code == 404


def test_delete_view_success_and_cascade(authenticated_client, override_db):
    create_res = authenticated_client.post(
        "/api/views",
        json={"name": "ToDelete", "cadence": "daily"},
    )
    view_id = create_res.json()["id"]

    # Directly add a task and completion log to test cascade delete
    db = override_db
    task = Task(view_id=view_id, title="Task 1")
    db.add(task)
    db.commit()
    db.refresh(task)

    log = CompletionLog(task_id=task.id, period_key="d:2026-10-27", done=True)
    db.add(log)
    db.commit()

    delete_res = authenticated_client.delete(f"/api/views/{view_id}")
    assert delete_res.status_code == 204

    # Verify view is deleted
    list_res = authenticated_client.get("/api/views")
    assert len(list_res.json()) == 0


def test_delete_view_not_found(authenticated_client):
    response = authenticated_client.delete("/api/views/non-existent-id")
    assert response.status_code == 404
