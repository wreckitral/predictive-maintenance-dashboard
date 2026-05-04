from datetime import datetime
from sqlalchemy import func

from database.connection import SessionLocal
from database.models import SensorReading


def append_reading(reading):
    if isinstance(reading.get("timestamp"), str):
        reading["timestamp"] = datetime.fromisoformat(reading["timestamp"])

    sensor_reading = SensorReading(
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
        readings = db.query(SensorReading).all()
        return readings


def get_latest_by_machine():
    with SessionLocal() as db:
        subq = db.query(
            SensorReading.machine_id,
            SensorReading.sensor_type,
            func.max(SensorReading.timestamp).label('max_timestamp')
        ).group_by(SensorReading.machine_id, SensorReading.sensor_type).subquery()

        latest_readings = db.query(SensorReading).join(
            subq,
            (SensorReading.machine_id == subq.c.machine_id) &
            (SensorReading.sensor_type == subq.c.sensor_type) &
            (SensorReading.timestamp == subq.c.max_timestamp)
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
                "timestamp": reading.timestamp.isoformat() if reading.timestamp else None
            }

        return list(machines.values())