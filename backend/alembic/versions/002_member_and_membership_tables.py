"""Member and membership tables

Revision ID: 002
Revises: 001
Create Date: 2024-11-18 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create membership_status enum type
    op.execute("""
        CREATE TYPE membership_status AS ENUM (
            'active',
            'expired',
            'cancelled',
            'suspended'
        )
    """)

    # Create membership_plans table
    op.create_table(
        'membership_plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('duration_days', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('features', sa.Text(), nullable=True),
        sa.Column('max_classes_per_month', sa.Integer(), nullable=True),
        sa.Column('has_personal_trainer', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_membership_plans_id'), 'membership_plans', ['id'], unique=False)

    # Create members table
    op.create_table(
        'members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('membership_plan_id', sa.Integer(), nullable=True),
        sa.Column('membership_status', sa.Enum('active', 'expired', 'cancelled', 'suspended', name='membership_status'), nullable=False, server_default='active'),
        sa.Column('membership_start_date', sa.Date(), nullable=True),
        sa.Column('membership_end_date', sa.Date(), nullable=True),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('gender', sa.String(), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('emergency_contact_name', sa.String(), nullable=True),
        sa.Column('emergency_contact_phone', sa.String(), nullable=True),
        sa.Column('fitness_goals', sa.Text(), nullable=True),
        sa.Column('medical_conditions', sa.Text(), nullable=True),
        sa.Column('preferred_workout_time', sa.String(), nullable=True),
        sa.Column('qr_code', sa.String(), nullable=True),
        sa.Column('total_check_ins', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_check_in', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['membership_plan_id'], ['membership_plans.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_members_id'), 'members', ['id'], unique=False)
    op.create_index(op.f('ix_members_user_id'), 'members', ['user_id'], unique=True)
    op.create_index(op.f('ix_members_qr_code'), 'members', ['qr_code'], unique=True)

    # Create check_ins table
    op.create_table(
        'check_ins',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('member_id', sa.Integer(), nullable=False),
        sa.Column('check_in_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('check_out_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('method', sa.String(), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['member_id'], ['members.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_check_ins_id'), 'check_ins', ['id'], unique=False)
    op.create_index(op.f('ix_check_ins_member_id'), 'check_ins', ['member_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_check_ins_member_id'), table_name='check_ins')
    op.drop_index(op.f('ix_check_ins_id'), table_name='check_ins')
    op.drop_table('check_ins')

    op.drop_index(op.f('ix_members_qr_code'), table_name='members')
    op.drop_index(op.f('ix_members_user_id'), table_name='members')
    op.drop_index(op.f('ix_members_id'), table_name='members')
    op.drop_table('members')

    op.drop_index(op.f('ix_membership_plans_id'), table_name='membership_plans')
    op.drop_table('membership_plans')

    op.execute('DROP TYPE membership_status')
