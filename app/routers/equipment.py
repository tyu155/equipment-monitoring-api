from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Equipment, Measurement
from app.schemas import (
    EquipmentCreate, EquipmentRead, EquipmentUpdate,
    MeasurementCreate, MeasurementRead,
)

router = APIRouter(prefix="/api/v1/equipment", tags=["equipment"])


@router.post("", response_model=EquipmentRead, status_code=status.HTTP_201_CREATED)
def create_equipment(payload: EquipmentCreate, db: Session = Depends(get_db)):
    equipment = Equipment(**payload.model_dump())
    db.add(equipment)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Equipment with this serial_number already exists",
        ) from exc
    db.refresh(equipment)
    return equipment


@router.get("", response_model=list[EquipmentRead])
def list_equipment(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if skip < 0 or not 1 <= limit <= 100:
        raise HTTPException(status_code=400, detail="Invalid pagination parameters")
    statement = select(Equipment).order_by(Equipment.id).offset(skip).limit(limit)
    return db.scalars(statement).all()


@router.get("/{equipment_id}", response_model=EquipmentRead)
def get_equipment(equipment_id: int, db: Session = Depends(get_db)):
    equipment = db.get(Equipment, equipment_id)
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment


@router.patch("/{equipment_id}", response_model=EquipmentRead)
def update_equipment(
    equipment_id: int, payload: EquipmentUpdate, db: Session = Depends(get_db)
):
    equipment = db.get(Equipment, equipment_id)
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(equipment, field, value)
    db.commit()
    db.refresh(equipment)
    return equipment


@router.delete("/{equipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    equipment = db.get(Equipment, equipment_id)
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    db.delete(equipment)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{equipment_id}/measurements",
    response_model=MeasurementRead,
    status_code=status.HTTP_201_CREATED,
)
def create_measurement(
    equipment_id: int, payload: MeasurementCreate, db: Session = Depends(get_db)
):
    if db.get(Equipment, equipment_id) is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    measurement = Measurement(equipment_id=equipment_id, **payload.model_dump())
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    return measurement


@router.get(
    "/{equipment_id}/measurements",
    response_model=list[MeasurementRead],
)
def list_measurements(equipment_id: int, db: Session = Depends(get_db)):
    if db.get(Equipment, equipment_id) is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    statement = (
        select(Measurement)
        .where(Measurement.equipment_id == equipment_id)
        .order_by(Measurement.recorded_at.desc())
    )
    return db.scalars(statement).all()
