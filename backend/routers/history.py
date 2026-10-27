from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/history", tags=["History"])


class HistoryPeriodResponse(BaseModel):
    key: str
    start: str
    tasks: List[dict]


@router.get("", response_model=List[HistoryPeriodResponse])
def get_history():
    return []
