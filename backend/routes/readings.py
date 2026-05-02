from fastapi import APIRouter
from models.schemas import SensorReading
from data.store import append_reading, get_all_reading

router = APIRouter()

@router.post("/readings")
def create_reading(payload: SensorReading):
    append_reading(payload.dict())

    return {"status": "ok"}

@router.get("/readings")
def get_reading():
    return get_all_reading()