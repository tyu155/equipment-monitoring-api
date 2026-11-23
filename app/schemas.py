from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


EquipmentStatus = Literal["active", "inactive", "maintenance"]


class EquipmentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    location: str = Field(min_length=1, max_length=160)
    status: EquipmentStatus = "active"
    serial_number: str = Field(min_length=1, max_length=80)


class EquipmentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    location: str | None = Field(default=None, min_length=1, max_length=160)
    status: EquipmentStatus | None = None


class EquipmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    location: str
    status: EquipmentStatus
    serial_number: str


class MeasurementCreate(BaseModel):
    temperature: float = Field(ge=-100, le=1000)
    pressure: float = Field(ge=0, le=1000)


class MeasurementRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    equipment_id: int
    temperature: float
    pressure: float
    recorded_at: datetime
