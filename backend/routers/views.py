from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/views", tags=["Views"])


class ViewResponse(BaseModel):
    id: str
    name: str
    cadence: str
    createdAt: str


class CreateViewRequest(BaseModel):
    name: str
    cadence: str


class TaskResponse(BaseModel):
    id: str
    viewId: str
    title: str
    createdAt: str


class CreateTaskRequest(BaseModel):
    title: str


@router.get("", response_model=List[ViewResponse])
def list_views():
    return []


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ViewResponse)
def create_view(body: CreateViewRequest):
    return {
        "id": "view-1",
        "name": body.name,
        "cadence": body.cadence,
        "createdAt": "2025-01-01T00:00:00Z",
    }


@router.get("/{id}", response_model=ViewResponse)
def get_view(id: str):
    return {
        "id": id,
        "name": "Default View",
        "cadence": "daily",
        "createdAt": "2025-01-01T00:00:00Z",
    }


@router.put("/{id}", response_model=ViewResponse)
def update_view(id: str, body: CreateViewRequest):
    return {
        "id": id,
        "name": body.name,
        "cadence": body.cadence,
        "createdAt": "2025-01-01T00:00:00Z",
    }


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_view(id: str):
    return None


@router.post("/{viewId}/tasks", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_task_for_view(viewId: str, body: CreateTaskRequest):
    return {
        "id": "task-1",
        "viewId": viewId,
        "title": body.title,
        "createdAt": "2025-01-01T00:00:00Z",
    }
