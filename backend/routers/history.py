from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from backend.database import get_db
from backend.models.user import User
from backend.models.view import View
from backend.models.task import Task
from backend.models.completion_log import CompletionLog
from backend.security import get_current_user

router = APIRouter(prefix="/api/history", tags=["History"])


class HistoryTaskResponse(BaseModel):
    id: str
    title: str
    done: bool

    class Config:
        from_attributes = True


class HistoryPeriodResponse(BaseModel):
    key: str
    start: str
    tasks: List[HistoryTaskResponse]


class ViewResponse(BaseModel):
    id: str
    name: str
    cadence: str
    createdAt: str

    class Config:
        from_attributes = True


class ViewHistoryResponse(BaseModel):
    view: ViewResponse
    periods: List[HistoryPeriodResponse]


def period_key_to_start_datetime(period_key: str) -> str:
    try:
        # Format examples: d:2026-10-27, w:2026-10-26, m:2026-10
        parts = period_key.split(":")
        if len(parts) == 2:
            date_str = parts[1]
            if len(date_str) == 7:  # monthly m:YYYY-MM
                date_str += "-01"
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.isoformat() + "Z"
    except Exception:
        pass
    return datetime.utcnow().isoformat() + "Z"


@router.get("", response_model=List[ViewHistoryResponse])
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    views = db.query(View).filter(View.user_id == current_user.id).all()
    result = []

    for view in views:
        tasks = db.query(Task).filter(Task.view_id == view.id).all()
        task_ids = [t.id for t in tasks]

        periods_data = []
        if task_ids:
            # Find distinct period keys for these tasks
            log_rows = (
                db.query(CompletionLog.period_key)
                .filter(CompletionLog.task_id.in_(task_ids))
                .distinct()
                .all()
            )
            period_keys = sorted(list({row[0] for row in log_rows}), reverse=True)

            for p_key in period_keys:
                period_tasks = []
                for task in tasks:
                    log = (
                        db.query(CompletionLog)
                        .filter(
                            CompletionLog.task_id == task.id,
                            CompletionLog.period_key == p_key,
                        )
                        .first()
                    )
                    done_status = log.done if log else False
                    period_tasks.append(
                        {
                            "id": task.id,
                            "title": task.title,
                            "done": done_status,
                        }
                    )
                periods_data.append(
                    {
                        "key": p_key,
                        "start": period_key_to_start_datetime(p_key),
                        "tasks": period_tasks,
                    }
                )

        result.append(
            {
                "view": {
                    "id": view.id,
                    "name": view.name,
                    "cadence": view.cadence,
                    "createdAt": view.created_at.isoformat() if view.created_at else datetime.utcnow().isoformat(),
                },
                "periods": periods_data,
            }
        )

    return result
