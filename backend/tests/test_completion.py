import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.main import app
from backend.database import Base, get_db
from backend.models import User, View, Task, CompletionLog
from backend.routers.tasks import get_current_period_key


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


def test_period_key_generation():
    from datetime import datetime
    dt = datetime(2026, 10, 27, 12, 0, 0) # Monday
    assert get_current_period_key("daily", dt) == "d:2026-10-27"
    assert get_current_period_key("weekly", dt) == "w:2026-10-26"
    assert get_current_period_key("monthly", dt) == "m:2026-10"


def test_task_completion_toggling(client):
    client.post(
        "/api/auth/register",
        json={"email": "compuser@example.com", "password": "securepassword123"},
    )
    view_res = client.post(
        "/api/views",
        json={"name": "Habits", "cadence": "daily"},
    )
    view_id = view_res.json()["id"]

    task_res = client.post(
        f"/api/views/{view_id}/tasks",
        json={"title": "Meditate"},
    )
    task_id = task_res.json()["id"]

    # Mark done
    done_res = client.post(f"/api/tasks/{task_id}/done", json={"done": True})
    assert done_res.status_code == 200
    assert done_res.json()["done"] is True

    # Check task list
    list_res = client.get(f"/api/views/{view_id}/tasks")
    assert list_res.json()[0]["done"] is True

    # Toggle off (done: false)
    off_res = client.post(f"/api/tasks/{task_id}/done", json={"done": False})
    assert off_res.status_code == 200
    assert off_res.json()["done"] is False

    list_res2 = client.get(f"/api/views/{view_id}/tasks")
    assert list_res2.json()[0]["done"] is False


def test_malformed_completion_request(client):
    client.post(
        "/api/auth/register",
        json={"email": "compuser2@example.com", "password": "securepassword123"},
    )
    view_res = client.post(
        "/api/views",
        json={"name": "Habits", "cadence": "daily"},
    )
    view_id = view_res.json()["id"]

    task_res = client.post(
        f"/api/views/{view_id}/tasks",
        json={"title": "Meditate"},
    )
    task_id = task_res.json()["id"]

    # Non-boolean done
    res = client.post(f"/api/tasks/{task_id}/done", json={"done": "yes"})
    assert res.status_code == 400
