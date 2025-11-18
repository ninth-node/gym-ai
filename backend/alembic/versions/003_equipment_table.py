"""Equipment table

Revision ID: 003
Revises: 002
Create Date: 2024-11-18 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create equipment_status enum type
    op.execute("""
        CREATE TYPE equipment_status AS ENUM (
            'operational',
            'maintenance_needed',
            'under_maintenance',
            'out_of_service'
        )
    """)

    # Create equipment_category enum type
    op.execute("""
        CREATE TYPE equipment_category AS ENUM (
            'cardio',
            'strength',
            'free_weights',
            'functional',
            'other'
        )
    """)

    # Create equipment table
    op.create_table(
        'equipment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('category', sa.Enum('cardio', 'strength', 'free_weights', 'functional', 'other', name='equipment_category'), nullable=False),
        sa.Column('model', sa.String(), nullable=True),
        sa.Column('serial_number', sa.String(), nullable=True),
        sa.Column('status', sa.Enum('operational', 'maintenance_needed', 'under_maintenance', 'out_of_service', name='equipment_status'), nullable=False, server_default='operational'),
        sa.Column('total_usage_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_usage_hours', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_maintenance_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('next_maintenance_due', sa.DateTime(timezone=True), nullable=True),
        sa.Column('maintenance_notes', sa.Text(), nullable=True),
        sa.Column('purchase_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('warranty_expiry', sa.DateTime(timezone=True), nullable=True),
        sa.Column('iot_device_id', sa.String(), nullable=True),
        sa.Column('iot_last_sync', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_equipment_id'), 'equipment', ['id'], unique=False)
    op.create_index(op.f('ix_equipment_serial_number'), 'equipment', ['serial_number'], unique=True)
    op.create_index(op.f('ix_equipment_iot_device_id'), 'equipment', ['iot_device_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_equipment_iot_device_id'), table_name='equipment')
    op.drop_index(op.f('ix_equipment_serial_number'), table_name='equipment')
    op.drop_index(op.f('ix_equipment_id'), table_name='equipment')
    op.drop_table('equipment')
    op.execute('DROP TYPE equipment_category')
    op.execute('DROP TYPE equipment_status')
