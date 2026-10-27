from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Literal, Optional
from datetime import datetime, timedelta

from backend.database import get_db
from backend.models.user import User
from backend.models.view import View
from backend.models.task import Task
from backend.models.completion_log import CompletionLog
from backend.security import get_current_user

router = APIRouter(prefix="/api/views", tags=["Views"])

CadenceType = Literal["daily", "weekly", "monthly"]


class CreateViewRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    cadence: CadenceType


class UpdateViewRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    cadence: CadenceType


class ViewResponse(BaseModel):
    id: str
    name: str
    cadence: str
    createdAt: str

    class Config:
        from_attributes = True


class ViewSummaryResponse(ViewResponse):
    taskCount: int
    doneCount: int


def get_current_period_key(cadence: str, dt: datetime = None) -> str:
    if dt is None:
        dt = datetime.utcnow()
    if cadence == "daily":
        return f"d:{dt.strftime('%Y-%m-%d')}"
    elif cadence == "weekly":
        monday = dt - timedelta(days=dt.weekday())
        return f"w:{monday.strftime('%Y-%m-%d')}"
    elif cadence == "monthly":
        return f"m:{dt.strftime('%Y-%m')}"
    return f"d:{dt.strftime('%Y-%m-%d')}"


@router.get("", response_model=List[ViewSummaryResponse])
def list_views(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    views = db.query(View).filter(View.user_id == current_user.id).all()
    result = []
    for view in views:
        task_count = len(view.tasks)
        period_key = get_current_period_key(view.cadence)
        task_ids = [t.id for t in view.tasks]
        done_count = 0
        if task_ids:
            done_count = (
                db.query(CompletionLog)
                .filter(
                    CompletionLog.task_id.in_(task_ids),
                    CompletionLog.period_key == period_key,
                    CompletionLog.done == True,
                )
                .count()
            )
        result.append(
            {
                "id": view.id,
                "name": view.name,
                "cadence": view.cadence,
                "createdAt": view.created_at.isoformat() if view.created_at else datetime.utcnow().isoformat(),
                "taskCount": task_count,
                "doneCount": done_count,
            }
        )
    return result


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ViewResponse)
def create_view(
    body: CreateViewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not body.name or not body.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="View name cannot be empty",
        )
    if body.cadence not in ["daily", "weekly", "monthly"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid cadence",
        )

    new_view = View(
        user_id=current_user.id,
        name=body.name.strip(),
        cadence=body.cadence,
    )
    db.add(new_view)
    db.commit()
    db.refresh(new_view)

    return {
        "id": new_view.id,
        "name": new_view.name,
        "cadence": new_view.cadence,
        "createdAt": new_view.created_at.isoformat() if new_view.created_at else datetime.utcnow().isoformat(),
    }


@router.put("/{id}", response_model=ViewResponse)
def update_view(
    id: str,
    body: UpdateViewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not body.name or not body.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="View name cannot be empty",
        )
    if body.cadence not in ["daily", "weekly", "monthly"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid cadence",
        )

    view = db.query(View).filter(View.id == id, View.user_id == current_user.id).first()
    if not view:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="View not found",
        )

    view.name = body.name.strip()
    view.cadence = body.cadence
    db.commit()
    db.refresh(view)

    return {
        "id": view.id,
        "name": view.name,
        "cadence": view.cadence,
        "createdAt": view.created_at.isoformat() if view.created_at else datetime.utcnow().isoformat(),
    }


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_view(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    view = db.query(View).filter(View.id == id, View.user_id == current_user.id).first()
    if not view:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="View not found",
        )

    db.delete(view)
    db.commit()
    return None
