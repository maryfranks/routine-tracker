from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from backend.database import get_db
from backend.models.user import User
from backend.models.view import View
from backend.models.task import Task
from backend.models.completion_log import CompletionLog
from backend.security import get_current_user
from backend.routers.clock import get_simulated_now

router = APIRouter(prefix="/api", tags=["Tasks"])


class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=80)


class UpdateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=80)


class TaskResponse(BaseModel):
    id: str
    viewId: str
    title: str
    createdAt: str

    class Config:
        from_attributes = True


class TaskWithStatusResponse(TaskResponse):
    done: bool


class TaskDoneRequest(BaseModel):
    done: bool = Field(..., strict=True)


class TaskDoneResponse(BaseModel):
    id: str
    done: bool


def get_current_period_key(cadence: str, dt: datetime = None) -> str:
    if dt is None:
        dt = get_simulated_now()
    if cadence == "daily":
        return f"d:{dt.strftime('%Y-%m-%d')}"
    elif cadence == "weekly":
        monday = dt - timedelta(days=dt.weekday())
        return f"w:{monday.strftime('%Y-%m-%d')}"
    elif cadence == "monthly":
        return f"m:{dt.strftime('%Y-%m-%d')[:7]}"
    return f"d:{dt.strftime('%Y-%m-%d')}"


@router.get("/views/{viewId}/tasks", response_model=List[TaskWithStatusResponse])
def list_tasks(
    viewId: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    view = db.query(View).filter(View.id == viewId, View.user_id == current_user.id).first()
    if not view:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="View not found",
        )

    period_key = get_current_period_key(view.cadence)
    tasks = db.query(Task).filter(Task.view_id == viewId).all()

    result = []
    for task in tasks:
        log = (
            db.query(CompletionLog)
            .filter(
                CompletionLog.task_id == task.id,
                CompletionLog.period_key == period_key,
            )
            .first()
        )
        done_status = log.done if log else False
        result.append(
            {
                "id": task.id,
                "viewId": task.view_id,
                "title": task.title,
                "createdAt": task.created_at.isoformat() if task.created_at else datetime.utcnow().isoformat(),
                "done": done_status,
            }
        )
    return result


@router.post("/views/{viewId}/tasks", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_task(
    viewId: str,
    body: CreateTaskRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not body.title or not body.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty",
        )

    view = db.query(View).filter(View.id == viewId, View.user_id == current_user.id).first()
    if not view:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="View not found",
        )

    new_task = Task(
        view_id=viewId,
        title=body.title.strip(),
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "id": new_task.id,
        "viewId": new_task.view_id,
        "title": new_task.title,
        "createdAt": new_task.created_at.isoformat() if new_task.created_at else datetime.utcnow().isoformat(),
    }


@router.put("/tasks/{id}", response_model=TaskResponse)
def update_task(
    id: str,
    body: UpdateTaskRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not body.title or not body.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty",
        )

    task = db.query(Task).join(View).filter(Task.id == id, View.user_id == current_user.id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task.title = body.title.strip()
    db.commit()
    db.refresh(task)

    return {
        "id": task.id,
        "viewId": task.view_id,
        "title": task.title,
        "createdAt": task.created_at.isoformat() if task.created_at else datetime.utcnow().isoformat(),
    }


@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).join(View).filter(Task.id == id, View.user_id == current_user.id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    db.delete(task)
    db.commit()
    return None


@router.post("/tasks/{id}/done", response_model=TaskDoneResponse)
def set_task_done(
    id: str,
    body: TaskDoneRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).join(View).filter(Task.id == id, View.user_id == current_user.id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    period_key = get_current_period_key(task.view.cadence)
    log = (
        db.query(CompletionLog)
        .filter(
            CompletionLog.task_id == task.id,
            CompletionLog.period_key == period_key,
        )
        .first()
    )

    if log:
        log.done = body.done
    else:
        log = CompletionLog(
            task_id=task.id,
            period_key=period_key,
            done=body.done,
        )
        db.add(log)

    db.commit()
    return {
        "id": task.id,
        "done": body.done,
    }
