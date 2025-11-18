"""
Payment model for tracking member payments and transactions.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base


class PaymentStatus(str, enum.Enum):
    """Payment status enumeration."""

    PENDING = "pending"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELED = "canceled"


class PaymentMethod(str, enum.Enum):
    """Payment method enumeration."""

    CARD = "card"
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"
    CHECK = "check"
    OTHER = "other"


class Payment(Base):
    """
    Payment model for tracking member payments.

    Integrates with Stripe for online payments.
    """

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    # Member relationship
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    member = relationship("Member", back_populates="payments")

    # Stripe integration
    stripe_payment_intent_id = Column(String, unique=True, nullable=True, index=True)
    stripe_customer_id = Column(String, nullable=True, index=True)
    stripe_charge_id = Column(String, unique=True, nullable=True)

    # Payment details
    amount = Column(Float, nullable=False)  # Amount in USD
    currency = Column(String, default="usd", nullable=False)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)

    # Payment metadata
    description = Column(String, nullable=True)
    invoice_number = Column(String, unique=True, nullable=True, index=True)

    # Related subscription/plan
    membership_plan_id = Column(Integer, ForeignKey("membership_plans.id"), nullable=True)
    membership_plan = relationship("MembershipPlan")

    # Failure tracking
    failure_reason = Column(String, nullable=True)
    failure_code = Column(String, nullable=True)
    retry_count = Column(Integer, default=0)
    next_retry_at = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)
    refunded_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Payment(id={self.id}, member_id={self.member_id}, amount=${self.amount}, status={self.status})>"


class PaymentHistory(Base):
    """
    Payment history for tracking all payment events and state changes.
    """

    __tablename__ = "payment_history"

    id = Column(Integer, primary_key=True, index=True)

    # Payment relationship
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False)
    payment = relationship("Payment", backref="history")

    # Event details
    event_type = Column(String, nullable=False)  # e.g., "created", "succeeded", "failed", "refunded"
    previous_status = Column(String, nullable=True)
    new_status = Column(String, nullable=True)

    # Event metadata
    metadata = Column(String, nullable=True)  # JSON string for additional data
    notes = Column(String, nullable=True)

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<PaymentHistory(id={self.id}, payment_id={self.payment_id}, event={self.event_type})>"
