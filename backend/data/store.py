from datetime import datetime
from sqlalchemy import func

from database.connection import SessionLocal
from database.models import SensorReadingModel


def append_reading(reading):
    if isinstance(reading.get("timestamp"), str):
        reading["timestamp"] = datetime.fromisoformat(reading["timestamp"])

    sensor_reading = SensorReadingModel(
        machine_id=reading["machine_id"],
        machine_name=reading["machine_name"],
        sensor_type=reading["sensor_type"],
        value=reading["value"],
        unit=reading["unit"],
        timestamp=reading["timestamp"],
        is_anomaly=reading.get("is_anomaly", False),
        drift_status=reading.get("drift_status"),
    )

    with SessionLocal() as db:
        db.add(sensor_reading)
        db.commit()
        db.refresh(sensor_reading)

    return sensor_reading


def get_all_reading():
    with SessionLocal() as db:
        readings = db.query(SensorReadingModel).all()
        return [
            {
                "machine_id": r.machine_id,
                "machine_name": r.machine_name,
                "sensor_type": r.sensor_type,
                "value": r.value,
                "unit": r.unit,
                "timestamp": r.timestamp.isoformat() if r.timestamp else None,
                "is_anomaly": r.is_anomaly,
                "drift_status": r.drift_status,
            }
            for r in readings
        ]
    
def get_reading_by_machine(machine_id):
    with SessionLocal() as db:
        readings = db.query(SensorReadingModel).filter(
            SensorReadingModel.machine_id == machine_id
        ).all()
        return [
            {
                "machine_id": r.machine_id,
                "machine_name": r.machine_name,
                "sensor_type": r.sensor_type,
                "value": r.value,
                "unit": r.unit,
                "timestamp": r.timestamp.isoformat() if r.timestamp else None,
                "is_anomaly": r.is_anomaly,
                "drift_status": r.drift_status,
            }
            for r in readings
        ]

def get_latest_by_machine():
    with SessionLocal() as db:
        subq = db.query(
            SensorReadingModel.machine_id,
            SensorReadingModel.sensor_type,
            func.max(SensorReadingModel.timestamp).label('max_timestamp')
        ).group_by(SensorReadingModel.machine_id, SensorReadingModel.sensor_type).subquery()

        latest_readings = db.query(SensorReadingModel).join(
            subq,
            (SensorReadingModel.machine_id == subq.c.machine_id) &
            (SensorReadingModel.sensor_type == subq.c.sensor_type) &
            (SensorReadingModel.timestamp == subq.c.max_timestamp)
        ).all()

        machines = {}
        for reading in latest_readings:
            machine_id = reading.machine_id
            if machine_id not in machines:
                machines[machine_id] = {
                    "machine_id": machine_id,
                    "machine_name": reading.machine_name,
                    "sensors": {}
                }
            machines[machine_id]["sensors"][reading.sensor_type] = {
                "value": reading.value,
                "unit": reading.unit,
                "is_anomaly": reading.is_anomaly,
                "drift_status": reading.drift_status,
                "timestamp": reading.timestamp.isoformat() if reading.timestamp else None
            }

        return list(machines.values())