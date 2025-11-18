"""
Payment service for handling payment operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import logging
import json

from app.models.payment import Payment, PaymentHistory, PaymentStatus, PaymentMethod
from app.models.member import Member
from app.core.integrations.stripe_client import stripe_client

logger = logging.getLogger(__name__)


class PaymentService:
    """Service for payment operations."""

    @staticmethod
    async def create_payment(
        db: AsyncSession,
        member_id: int,
        amount: float,
        payment_method: PaymentMethod,
        membership_plan_id: Optional[int] = None,
        description: Optional[str] = None,
        auto_process: bool = False
    ) -> Optional[Payment]:
        """
        Create a new payment record.

        Args:
            db: Database session
            member_id: Member ID
            amount: Payment amount
            payment_method: Payment method
            membership_plan_id: Optional membership plan ID
            description: Payment description
            auto_process: Automatically process payment via Stripe

        Returns:
            Created Payment object
        """
        try:
            # Get member
            result = await db.execute(
                select(Member).where(Member.id == member_id)
            )
            member = result.scalar_one_or_none()

            if not member:
                logger.error(f"Member {member_id} not found")
                return None

            # Create payment record
            payment = Payment(
                member_id=member_id,
                amount=amount,
                currency="usd",
                status=PaymentStatus.PENDING,
                payment_method=payment_method,
                description=description,
                membership_plan_id=membership_plan_id
            )

            # If payment method is card and auto_process is True, create Stripe payment intent
            if payment_method == PaymentMethod.CARD and auto_process:
                # Ensure member has Stripe customer ID
                if not member.stripe_customer_id:
                    user = member.user
                    customer = stripe_client.create_customer(
                        email=user.email,
                        name=user.full_name,
                        metadata={
                            "member_id": member.id,
                            "user_id": user.id
                        }
                    )

                    if customer:
                        member.stripe_customer_id = customer.id
                        await db.commit()
                    else:
                        logger.error(f"Failed to create Stripe customer for member {member_id}")

                # Create payment intent
                if member.stripe_customer_id:
                    payment_intent = stripe_client.create_payment_intent(
                        amount=amount,
                        customer_id=member.stripe_customer_id,
                        metadata={
                            "member_id": member_id,
                            "payment_id": "pending"  # Will be updated after insert
                        },
                        description=description
                    )

                    if payment_intent:
                        payment.stripe_payment_intent_id = payment_intent.id
                        payment.status = PaymentStatus.PROCESSING

            db.add(payment)
            await db.commit()
            await db.refresh(payment)

            # Create payment history entry
            await PaymentService.add_payment_history(
                db,
                payment.id,
                "created",
                None,
                PaymentStatus.PENDING.value
            )

            logger.info(f"Payment created: {payment.id} for member {member_id}, amount ${amount}")
            return payment

        except Exception as e:
            logger.error(f"Error creating payment: {e}")
            await db.rollback()
            return None

    @staticmethod
    async def get_payment(db: AsyncSession, payment_id: int) -> Optional[Payment]:
        """Get a payment by ID."""
        result = await db.execute(
            select(Payment).where(Payment.id == payment_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_member_payments(
        db: AsyncSession,
        member_id: int,
        limit: int = 50
    ) -> List[Payment]:
        """Get all payments for a member."""
        result = await db.execute(
            select(Payment)
            .where(Payment.member_id == member_id)
            .order_by(Payment.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    @staticmethod
    async def update_payment_status(
        db: AsyncSession,
        payment_id: int,
        new_status: PaymentStatus,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Payment]:
        """Update payment status."""
        payment = await PaymentService.get_payment(db, payment_id)

        if not payment:
            logger.error(f"Payment {payment_id} not found")
            return None

        old_status = payment.status
        payment.status = new_status
        payment.updated_at = datetime.utcnow()

        if new_status == PaymentStatus.SUCCEEDED:
            payment.paid_at = datetime.utcnow()
        elif new_status == PaymentStatus.REFUNDED:
            payment.refunded_at = datetime.utcnow()

        await db.commit()
        await db.refresh(payment)

        # Add to payment history
        await PaymentService.add_payment_history(
            db,
            payment_id,
            f"status_changed_to_{new_status.value}",
            old_status.value,
            new_status.value,
            metadata
        )

        logger.info(f"Payment {payment_id} status updated: {old_status} -> {new_status}")
        return payment

    @staticmethod
    async def process_failed_payment(
        db: AsyncSession,
        payment_id: int,
        failure_reason: str,
        failure_code: Optional[str] = None
    ) -> Optional[Payment]:
        """Process a failed payment."""
        payment = await PaymentService.get_payment(db, payment_id)

        if not payment:
            return None

        payment.status = PaymentStatus.FAILED
        payment.failure_reason = failure_reason
        payment.failure_code = failure_code
        payment.retry_count += 1

        # Schedule next retry (exponential backoff)
        retry_delay_hours = 2 ** payment.retry_count  # 2, 4, 8, 16 hours
        payment.next_retry_at = datetime.utcnow() + timedelta(hours=retry_delay_hours)

        await db.commit()
        await db.refresh(payment)

        # Add to payment history
        await PaymentService.add_payment_history(
            db,
            payment_id,
            "payment_failed",
            None,
            PaymentStatus.FAILED.value,
            {"failure_reason": failure_reason, "failure_code": failure_code}
        )

        logger.warning(
            f"Payment {payment_id} failed (attempt {payment.retry_count}): {failure_reason}"
        )
        return payment

    @staticmethod
    async def add_payment_history(
        db: AsyncSession,
        payment_id: int,
        event_type: str,
        previous_status: Optional[str] = None,
        new_status: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Add an entry to payment history."""
        history_entry = PaymentHistory(
            payment_id=payment_id,
            event_type=event_type,
            previous_status=previous_status,
            new_status=new_status,
            metadata=json.dumps(metadata) if metadata else None
        )

        db.add(history_entry)
        await db.commit()

    @staticmethod
    async def get_failed_payments_for_retry(
        db: AsyncSession
    ) -> List[Payment]:
        """Get failed payments that are ready for retry."""
        now = datetime.utcnow()
        result = await db.execute(
            select(Payment)
            .where(
                Payment.status == PaymentStatus.FAILED,
                Payment.retry_count < 5,  # Max 5 retry attempts
                Payment.next_retry_at <= now
            )
            .order_by(Payment.next_retry_at)
        )
        return list(result.scalars().all())

    @staticmethod
    async def calculate_member_revenue(
        db: AsyncSession,
        member_id: int
    ) -> Dict[str, float]:
        """Calculate total revenue from a member."""
        result = await db.execute(
            select(Payment)
            .where(
                Payment.member_id == member_id,
                Payment.status == PaymentStatus.SUCCEEDED
            )
        )
        payments = result.scalars().all()

        total = sum(p.amount for p in payments)
        count = len(payments)

        return {
            "total_revenue": total,
            "payment_count": count,
            "average_payment": total / count if count > 0 else 0
        }
