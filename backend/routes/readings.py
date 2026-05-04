from fastapi import APIRouter, HTTPException
from models.schemas import SensorReading
from data.store import append_reading, get_all_reading, get_latest_by_machine, get_reading_by_machine
from services.ai import analyze_machine

router = APIRouter()

@router.post("/readings")
def create_reading(payload: SensorReading):
    append_reading(payload.dict())
    return {"status": "ok"}

@router.get("/readings")
def get_readings():
    return get_all_reading()

@router.get("/readings/{machine_id}")
def get_readings_by_machine(machine_id: str):
    return get_reading_by_machine(machine_id)

@router.post("/analyze/{machine_id}")
def analyze_readings(machine_id: str):
    latest_by_machine = get_latest_by_machine()
    machine_summary = next(
        (machine for machine in latest_by_machine if machine.get("machine_id") == machine_id),
        None,
    )

    if machine_summary is None:
        raise HTTPException(status_code=404, detail="Machine not found")

    return analyze_machine(machine_summary)
