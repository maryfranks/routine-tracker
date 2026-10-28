from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal
from datetime import datetime, timedelta

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


_simulated_days = 0
_simulated_weeks = 0
_simulated_months = 0

BASE_DATE = datetime(2025, 1, 1, 0, 0, 0)


def get_simulated_now() -> datetime:
    total_days = _simulated_days + (_simulated_weeks * 7) + (_simulated_months * 30)
    return BASE_DATE + timedelta(days=total_days)


@router.get("", response_model=ClockState)
def get_clock():
    total_days = _simulated_days + (_simulated_weeks * 7) + (_simulated_months * 30)
    current_time = BASE_DATE + timedelta(days=total_days)
    simulated = total_days > 0
    return {
        "now": current_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "simulated": simulated,
        "offset": {
            "days": _simulated_days,
            "weeks": _simulated_weeks,
            "months": _simulated_months,
        },
    }


@router.post("/advance", response_model=ClockState)
def advance_clock(body: AdvanceRequest):
    global _simulated_days, _simulated_weeks, _simulated_months
    if body.unit == "day":
        _simulated_days += 1
    elif body.unit == "week":
        _simulated_weeks += 1
    elif body.unit == "month":
        _simulated_months += 1

    total_days = _simulated_days + (_simulated_weeks * 7) + (_simulated_months * 30)
    current_time = BASE_DATE + timedelta(days=total_days)
    return {
        "now": current_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "simulated": True,
        "offset": {
            "days": _simulated_days,
            "weeks": _simulated_weeks,
            "months": _simulated_months,
        },
    }


@router.post("/reset", response_model=ClockState)
def reset_clock():
    global _simulated_days, _simulated_weeks, _simulated_months
    _simulated_days = 0
    _simulated_weeks = 0
    _simulated_months = 0
    return {
        "now": BASE_DATE.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "simulated": False,
        "offset": {
            "days": 0,
            "weeks": 0,
            "months": 0,
        },
    }
