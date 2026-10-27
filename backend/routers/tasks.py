from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


class TaskResponse(BaseModel):
    id: str
    viewId: str
    title: str
    createdAt: str


class UpdateTaskRequest(BaseModel):
    title: str


class TaskDoneResponse(BaseModel):
    id: str
    done: bool


class TaskDoneRequest(BaseModel):
    done: bool


@router.put("/{id}", response_model=TaskResponse)
def update_task(id: str, body: UpdateTaskRequest):
    return {
        "id": id,
        "viewId": "view-1",
        "title": body.title,
        "createdAt": "2025-01-01T00:00:00Z",
    }


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: str):
    return None


@router.post("/{id}/done", response_model=TaskDoneResponse)
def set_task_done(id: str, body: TaskDoneRequest):
    return {
        "id": id,
        "done": body.done,
    }
