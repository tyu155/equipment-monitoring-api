"""Create equipment and measurements tables."""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "equipment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("location", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("serial_number", sa.String(length=80), nullable=False),
        sa.CheckConstraint(
            "status IN ('active', 'inactive', 'maintenance')",
            name="ck_equipment_status",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("serial_number"),
    )
    op.create_index("ix_equipment_id", "equipment", ["id"], unique=False)

    op.create_table(
        "measurements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("equipment_id", sa.Integer(), nullable=False),
        sa.Column("temperature", sa.Float(), nullable=False),
        sa.Column("pressure", sa.Float(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "temperature >= -100 AND temperature <= 1000",
            name="ck_measurement_temperature_range",
        ),
        sa.CheckConstraint(
            "pressure >= 0 AND pressure <= 1000",
            name="ck_measurement_pressure_range",
        ),
        sa.ForeignKeyConstraint(
            ["equipment_id"], ["equipment.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_measurements_id", "measurements", ["id"], unique=False)
    op.create_index(
        "ix_measurements_equipment_id",
        "measurements",
        ["equipment_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_measurements_equipment_id", table_name="measurements")
    op.drop_index("ix_measurements_id", table_name="measurements")
    op.drop_table("measurements")
    op.drop_index("ix_equipment_id", table_name="equipment")
    op.drop_table("equipment")
