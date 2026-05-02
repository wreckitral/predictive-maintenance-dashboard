from pydantic import BaseModel
from typing import Dict

class SensorReading(BaseModel):
    machine_id: str
    machine_name: str
    sensor_type: str
    value: float
    unit: str
    timestamp: str
    is_anomaly: bool

class SensorLatest(BaseModel):
    value: float
    unit: str
    is_anomaly: bool
    timestamp: str

class MachineSummary(BaseModel):
    machine_id: str
    machine_name: str
    sensors: Dict[str, SensorLatest]