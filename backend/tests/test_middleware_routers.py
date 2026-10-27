from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_cors_headers():
    response = client.options(
        "/api/auth/login",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        },
    )
    # FastAPI CORSMiddleware responds to OPTIONS preflight
    assert response.status_code in (200, 204)
    assert "access-control-allow-origin" in response.headers


def test_routers_registered():
    # Health check
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

    # Auth router - unauthenticated should return 401
    response = client.get("/api/auth/me")
    assert response.status_code == 401

    # Clock router
    response = client.get("/api/clock")
    assert response.status_code == 200

    # Views router
    response = client.get("/api/views")
    assert response.status_code == 200

    # History router
    response = client.get("/api/history")
    assert response.status_code == 200

    # Utilities router
    response = client.post("/api/demo")
    assert response.status_code == 200
    assert response.json() == {"message": "Demo data loaded"}
