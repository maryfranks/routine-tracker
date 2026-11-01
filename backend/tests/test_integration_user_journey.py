import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.main import app
from backend.database import Base, get_db


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


def test_end_to_end_user_journey(client):
    # 1. Register a new user
    reg_response = client.post(
        "/api/auth/register",
        json={"email": "journey@example.com", "password": "securepassword123"},
    )
    assert reg_response.status_code == 201
    assert reg_response.json()["email"] == "journey@example.com"

    # 2. Login to obtain session cookie
    login_response = client.post(
        "/api/auth/login",
        json={"email": "journey@example.com", "password": "securepassword123"},
    )
    assert login_response.status_code == 200
    assert login_response.json()["email"] == "journey@example.com"

    # 3. Create Daily and Weekly Views
    daily_view_res = client.post(
        "/api/views",
        json={"name": "Daily Habits", "cadence": "daily"},
    )
    assert daily_view_res.status_code == 201
    daily_view_id = daily_view_res.json()["id"]

    weekly_view_res = client.post(
        "/api/views",
        json={"name": "Weekly Goals", "cadence": "weekly"},
    )
    assert weekly_view_res.status_code == 201
    weekly_view_id = weekly_view_res.json()["id"]

    # 4. Add Tasks to Views
    task1_res = client.post(
        f"/api/views/{daily_view_id}/tasks",
        json={"title": "Morning Exercise"},
    )
    assert task1_res.status_code == 201
    task1_id = task1_res.json()["id"]

    task2_res = client.post(
        f"/api/views/{weekly_view_id}/tasks",
        json={"title": "Weekly Architecture Review"},
    )
    assert task2_res.status_code == 201
    task2_id = task2_res.json()["id"]

    # 5. Mark tasks as done
    done1_res = client.post(f"/api/tasks/{task1_id}/done", json={"done": True})
    assert done1_res.status_code == 200
    assert done1_res.json()["done"] is True

    done2_res = client.post(f"/api/tasks/{task2_id}/done", json={"done": True})
    assert done2_res.status_code == 200
    assert done2_res.json()["done"] is True

    # 6. Test Clock Simulation API
    clock_res = client.get("/api/clock")
    assert clock_res.status_code == 200
    assert clock_res.json()["simulated"] is False

    advance_res = client.post("/api/clock/advance", json={"unit": "day"})
    assert advance_res.status_code == 200
    assert advance_res.json()["simulated"] is True
    assert advance_res.json()["offset"]["days"] == 1

    reset_res = client.post("/api/clock/reset")
    assert reset_res.status_code == 200
    assert reset_res.json()["simulated"] is False

    # 7. Fetch History and Verify Records
    history_res = client.get("/api/history")
    assert history_res.status_code == 200
    history_data = history_res.json()
    assert isinstance(history_data, list)
    assert len(history_data) == 2

    # 8. Clean up / Delete a task and view
    delete_task_res = client.delete(f"/api/tasks/{task1_id}")
    assert delete_task_res.status_code == 204

    delete_view_res = client.delete(f"/api/views/{daily_view_id}")
    assert delete_view_res.status_code == 204
