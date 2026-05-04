from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String

from .connection import Base

class SensorReadingModel(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    machine_id = Column(String, nullable=False)
    machine_name = Column(String, nullable=False)
    sensor_type = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    is_anomaly = Column(Boolean, nullable=False, default=False)
    drift_status = Column(String, nullable=True)
