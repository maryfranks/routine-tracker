from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import re

from backend.database import get_db
from backend.models.user import User
from backend.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(..., min_length=8)


class LoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    createdAt: str

    class Config:
        from_attributes = True


def validate_email_format(email: str):
    if not re.match(EMAIL_REGEX, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format",
        )


def set_auth_cookie(response: Response, token: str):
    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
    )


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register_user(body: RegisterRequest, response: Response, db: Session = Depends(get_db)):
    validate_email_format(body.email)

    existing_user = db.query(User).filter(User.email == body.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = get_password_hash(body.password)
    new_user = User(
        email=body.email,
        password_hash=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(data={"sub": new_user.id})
    set_auth_cookie(response, token)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "createdAt": new_user.created_at.isoformat() if new_user.created_at else datetime.utcnow().isoformat(),
    }


@router.post("/login", response_model=UserResponse)
def login_user(body: LoginRequest, response: Response, db: Session = Depends(get_db)):
    validate_email_format(body.email)

    user = db.query(User).filter(User.email == body.email).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token(data={"sub": user.id})
    set_auth_cookie(response, token)

    return {
        "id": user.id,
        "email": user.email,
        "createdAt": user.created_at.isoformat() if user.created_at else datetime.utcnow().isoformat(),
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_user(response: Response, current_user: User = Depends(get_current_user)):
    response.delete_cookie(key="session")
    return None


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "createdAt": current_user.created_at.isoformat() if current_user.created_at else datetime.utcnow().isoformat(),
    }
