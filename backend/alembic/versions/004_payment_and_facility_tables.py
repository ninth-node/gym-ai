"""add payment and facility config tables

Revision ID: 004
Revises: 003
Create Date: 2025-11-18 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create facility_configs table
    op.create_table(
        'facility_configs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('total_capacity', sa.Integer(), nullable=False, server_default='100'),
        sa.Column('equipment_capacity', sa.Integer(), nullable=True),
        sa.Column('class_capacity', sa.Integer(), nullable=True),
        sa.Column('peak_hours_capacity', sa.JSON(), nullable=True),
        sa.Column('operating_hours', sa.JSON(), nullable=True),
        sa.Column('total_area_sqft', sa.Float(), nullable=True),
        sa.Column('equipment_count', sa.Integer(), nullable=True),
        sa.Column('training_rooms', sa.Integer(), nullable=True),
        sa.Column('deep_cleaning_frequency_days', sa.Integer(), server_default='30'),
        sa.Column('equipment_inspection_frequency_days', sa.Integer(), server_default='14'),
        sa.Column('amenities', sa.JSON(), nullable=True),
        sa.Column('target_temperature', sa.Float(), nullable=True, server_default='72.0'),
        sa.Column('humidity_target', sa.Float(), nullable=True, server_default='50.0'),
        sa.Column('occupancy_alert_threshold', sa.Float(), server_default='0.9'),
        sa.Column('enable_occupancy_alerts', sa.Boolean(), server_default='true'),
        sa.Column('enable_maintenance_alerts', sa.Boolean(), server_default='true'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )

    # Add stripe_customer_id to members table
    op.add_column('members', sa.Column('stripe_customer_id', sa.String(), nullable=True))
    op.create_index('ix_members_stripe_customer_id', 'members', ['stripe_customer_id'], unique=True)

    # Create payments table
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('member_id', sa.Integer(), nullable=False),
        sa.Column('stripe_payment_intent_id', sa.String(), nullable=True),
        sa.Column('stripe_customer_id', sa.String(), nullable=True),
        sa.Column('stripe_charge_id', sa.String(), nullable=True),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(), nullable=False, server_default='usd'),
        sa.Column('status', sa.Enum('PENDING', 'PROCESSING', 'SUCCEEDED', 'FAILED', 'REFUNDED', 'CANCELED', name='paymentstatus'), nullable=False),
        sa.Column('payment_method', sa.Enum('CARD', 'BANK_TRANSFER', 'CASH', 'CHECK', 'OTHER', name='paymentmethod'), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('invoice_number', sa.String(), nullable=True),
        sa.Column('membership_plan_id', sa.Integer(), nullable=True),
        sa.Column('failure_reason', sa.String(), nullable=True),
        sa.Column('failure_code', sa.String(), nullable=True),
        sa.Column('retry_count', sa.Integer(), server_default='0'),
        sa.Column('next_retry_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, onupdate=sa.text('now()')),
        sa.Column('paid_at', sa.DateTime(), nullable=True),
        sa.Column('refunded_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['member_id'], ['members.id'], ),
        sa.ForeignKeyConstraint(['membership_plan_id'], ['membership_plans.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_payments_member_id', 'payments', ['member_id'])
    op.create_index('ix_payments_stripe_payment_intent_id', 'payments', ['stripe_payment_intent_id'], unique=True)
    op.create_index('ix_payments_stripe_customer_id', 'payments', ['stripe_customer_id'])
    op.create_index('ix_payments_stripe_charge_id', 'payments', ['stripe_charge_id'], unique=True)
    op.create_index('ix_payments_invoice_number', 'payments', ['invoice_number'], unique=True)

    # Create payment_history table
    op.create_table(
        'payment_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('payment_id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.String(), nullable=False),
        sa.Column('previous_status', sa.String(), nullable=True),
        sa.Column('new_status', sa.String(), nullable=True),
        sa.Column('metadata', sa.String(), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['payment_id'], ['payments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_payment_history_payment_id', 'payment_history', ['payment_id'])


def downgrade() -> None:
    # Drop payment_history table
    op.drop_index('ix_payment_history_payment_id', table_name='payment_history')
    op.drop_table('payment_history')

    # Drop payments table
    op.drop_index('ix_payments_invoice_number', table_name='payments')
    op.drop_index('ix_payments_stripe_charge_id', table_name='payments')
    op.drop_index('ix_payments_stripe_customer_id', table_name='payments')
    op.drop_index('ix_payments_stripe_payment_intent_id', table_name='payments')
    op.drop_index('ix_payments_member_id', table_name='payments')
    op.drop_table('payments')

    # Drop enums
    op.execute('DROP TYPE paymentmethod')
    op.execute('DROP TYPE paymentstatus')

    # Remove stripe_customer_id from members table
    op.drop_index('ix_members_stripe_customer_id', table_name='members')
    op.drop_column('members', 'stripe_customer_id')

    # Drop facility_configs table
    op.drop_table('facility_configs')
