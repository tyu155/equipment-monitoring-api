from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Equipment(Base):
    __tablename__ = "equipment"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'inactive', 'maintenance')",
            name="ck_equipment_status",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    location: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
    serial_number: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    measurements: Mapped[list["Measurement"]] = relationship(
        back_populates="equipment",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Measurement(Base):
    __tablename__ = "measurements"
    __table_args__ = (
        CheckConstraint(
            "temperature >= -100 AND temperature <= 1000",
            name="ck_measurement_temperature_range",
        ),
        CheckConstraint(
            "pressure >= 0 AND pressure <= 1000",
            name="ck_measurement_pressure_range",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.id", ondelete="CASCADE"), nullable=False, index=True
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    pressure: Mapped[float] = mapped_column(Float, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    equipment: Mapped[Equipment] = relationship(back_populates="measurements")
