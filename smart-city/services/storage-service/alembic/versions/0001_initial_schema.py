"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-04-15 15:30:00
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "locations",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("city", sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "sensors",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("location_id", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False),
        sa.ForeignKeyConstraint(["location_id"], ["locations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "sensor_data",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sensor_id", sa.String(length=64), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("rolling_avg", sa.Float(), nullable=True),
        sa.Column("is_valid", sa.Boolean(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["sensor_id"], ["sensors.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sensor_data_sensor_id", "sensor_data", ["sensor_id"], unique=False)
    op.create_index("ix_sensor_data_type", "sensor_data", ["type"], unique=False)
    op.create_index("ix_sensor_data_recorded_at", "sensor_data", ["recorded_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_sensor_data_recorded_at", table_name="sensor_data")
    op.drop_index("ix_sensor_data_type", table_name="sensor_data")
    op.drop_index("ix_sensor_data_sensor_id", table_name="sensor_data")
    op.drop_table("sensor_data")
    op.drop_table("sensors")
    op.drop_table("locations")
