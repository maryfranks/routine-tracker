from fastapi import APIRouter, Response, status
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    createdAt: str


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register_user(body: RegisterRequest, response: Response):
    # Stub registration and cookie setting
    response.set_cookie(key="session", value="mock-session-token", httponly=True)
    return {
        "id": "user-1",
        "email": body.email,
        "createdAt": "2025-01-01T00:00:00Z",
    }


@router.post("/login", response_model=UserResponse)
def login_user(body: LoginRequest, response: Response):
    # Stub login and cookie setting
    response.set_cookie(key="session", value="mock-session-token", httponly=True)
    return {
        "id": "user-1",
        "email": body.email,
        "createdAt": "2025-01-01T00:00:00Z",
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_user(response: Response):
    response.delete_cookie(key="session")
    return None


@router.get("/me", response_model=UserResponse)
def get_current_user():
    return {
        "id": "user-1",
        "email": "user@example.com",
        "createdAt": "2025-01-01T00:00:00Z",
    }
