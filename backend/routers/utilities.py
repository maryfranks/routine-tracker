from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(tags=["Utilities"])


class MessageResponse(BaseModel):
    message: str


@router.post("/api/demo", response_model=MessageResponse)
def load_demo():
    return {"message": "Demo data loaded"}


@router.post("/api/reset", response_model=MessageResponse)
def reset_data():
    return {"message": "Data reset"}
