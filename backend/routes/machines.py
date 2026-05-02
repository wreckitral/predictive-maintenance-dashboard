from fastapi import APIRouter
from models.schemas import SensorReading, MachineSummary
from data.store import get_latest_by_machine
from typing import List

router = APIRouter()

@router.get("/machines", response_model=List[MachineSummary])
def get_machines():
    return get_latest_by_machine()