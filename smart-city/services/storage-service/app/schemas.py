from datetime import datetime

from pydantic import BaseModel


class LocationCreate(BaseModel):
    id: str
    name: str
    city: str


class SensorCreate(BaseModel):
    id: str
    type: str
    location_id: str
    status: str = "active"


class SensorRead(BaseModel):
    id: str
    type: str
    location_id: str
    status: str

    class Config:
        from_attributes = True


class SensorDataRead(BaseModel):
    sensor_id: str
    type: str
    value: float
    rolling_avg: float | None
    is_valid: bool
    recorded_at: datetime

    class Config:
        from_attributes = True
