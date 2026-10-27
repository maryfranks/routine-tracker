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
def test_view(client):
    client.post(
        "/api/auth/register",
        json={"email": "taskuser@example.com", "password": "securepassword123"},
    )
    res = client.post(
        "/api/views",
        json={"name": "Daily Routines", "cadence": "daily"},
    )
    return res.json()


def test_list_tasks_success(client, test_view):
    view_id = test_view["id"]
    client.post(f"/api/views/{view_id}/tasks", json={"title": "Morning Walk"})

    response = client.get(f"/api/views/{view_id}/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Morning Walk"
    assert data[0]["done"] is False


def test_list_tasks_view_not_found(client):
    client.post(
        "/api/auth/register",
        json={"email": "taskuser@example.com", "password": "securepassword123"},
    )
    response = client.get("/api/views/non-existent-view/tasks")
    assert response.status_code == 404


def test_create_task_success(client, test_view):
    view_id = test_view["id"]
    response = client.post(f"/api/views/{view_id}/tasks", json={"title": "Read a book"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Read a book"
    assert data["viewId"] == view_id
    assert "id" in data


def test_create_task_validation_errors(client, test_view):
    view_id = test_view["id"]
    # Empty title
    res = client.post(f"/api/views/{view_id}/tasks", json={"title": ""})
    assert res.status_code == 400

    # Non-existent view
    res2 = client.post("/api/views/bad-view/tasks", json={"title": "Task"})
    assert res2.status_code == 404


def test_update_task_success(client, test_view):
    view_id = test_view["id"]
    create_res = client.post(f"/api/views/{view_id}/tasks", json={"title": "Old Title"})
    task_id = create_res.json()["id"]

    update_res = client.put(f"/api/tasks/{task_id}", json={"title": "New Title"})
    assert update_res.status_code == 200
    assert update_res.json()["title"] == "New Title"


def test_update_task_not_found(client):
    client.post(
        "/api/auth/register",
        json={"email": "taskuser@example.com", "password": "securepassword123"},
    )
    response = client.put("/api/tasks/non-existent-task", json={"title": "New"})
    assert response.status_code == 404


def test_delete_task_success_and_cascade(client, test_view, override_db):
    view_id = test_view["id"]
    create_res = client.post(f"/api/views/{view_id}/tasks", json={"title": "To Delete"})
    task_id = create_res.json()["id"]

    delete_res = client.delete(f"/api/tasks/{task_id}")
    assert delete_res.status_code == 204

    tasks_res = client.get(f"/api/views/{view_id}/tasks")
    assert len(tasks_res.json()) == 0


def test_delete_task_not_found(client):
    client.post(
        "/api/auth/register",
        json={"email": "taskuser@example.com", "password": "securepassword123"},
    )
    response = client.delete("/api/tasks/non-existent-task")
    assert response.status_code == 404


def test_set_task_done(client, test_view):
    view_id = test_view["id"]
    create_res = client.post(f"/api/views/{view_id}/tasks", json={"title": "Drink Water"})
    task_id = create_res.json()["id"]

    done_res = client.post(f"/api/tasks/{task_id}/done", json={"done": True})
    assert done_res.status_code == 200
    assert done_res.json()["done"] is True

    # Check task status in list
    list_res = client.get(f"/api/views/{view_id}/tasks")
    assert list_res.json()[0]["done"] is True
