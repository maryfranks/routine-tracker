from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal

router = APIRouter(prefix="/api/clock", tags=["Clock Simulation"])


class ClockOffset(BaseModel):
    days: int = 0
    weeks: int = 0
    months: int = 0


class ClockState(BaseModel):
    now: str
    simulated: bool
    offset: ClockOffset


class AdvanceRequest(BaseModel):
    unit: Literal["day", "week", "month"]


@router.get("", response_model=ClockState)
def get_clock():
    return {
        "now": "2025-01-01T00:00:00Z",
        "simulated": False,
        "offset": {"days": 0, "weeks": 0, "months": 0},
    }


@router.post("/advance", response_model=ClockState)
def advance_clock(body: AdvanceRequest):
    days = 1 if body.unit == "day" else (7 if body.unit == "week" else 30)
    return {
        "now": "2025-01-02T00:00:00Z",
        "simulated": True,
        "offset": {"days": days, "weeks": 0, "months": 0},
    }


@router.post("/reset", response_model=ClockState)
def reset_clock():
    return {
        "now": "2025-01-01T00:00:00Z",
        "simulated": False,
        "offset": {"days": 0, "weeks": 0, "months": 0},
    }
