"""
Stripe integration for payment processing.
"""

import stripe
from typing import Optional, Dict, Any
import logging
from decimal import Decimal

from app.core.config import settings

logger = logging.getLogger(__name__)

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeClient:
    """
    Stripe client for payment processing operations.
    """

    def __init__(self):
        self.api_key = settings.STRIPE_SECRET_KEY
        if not self.api_key:
            logger.warning("Stripe API key not configured - payment processing will not work")

    def create_customer(
        self,
        email: str,
        name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[stripe.Customer]:
        """
        Create a Stripe customer.

        Args:
            email: Customer email
            name: Customer name
            metadata: Additional metadata

        Returns:
            Stripe Customer object or None if failed
        """
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata=metadata or {}
            )
            logger.info(f"Stripe customer created: {customer.id}")
            return customer
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create Stripe customer: {e}")
            return None

    def get_customer(self, customer_id: str) -> Optional[stripe.Customer]:
        """Get a Stripe customer by ID."""
        try:
            return stripe.Customer.retrieve(customer_id)
        except stripe.error.StripeError as e:
            logger.error(f"Failed to retrieve Stripe customer {customer_id}: {e}")
            return None

    def update_customer(
        self,
        customer_id: str,
        **kwargs
    ) -> Optional[stripe.Customer]:
        """Update a Stripe customer."""
        try:
            customer = stripe.Customer.modify(customer_id, **kwargs)
            logger.info(f"Stripe customer updated: {customer_id}")
            return customer
        except stripe.error.StripeError as e:
            logger.error(f"Failed to update Stripe customer {customer_id}: {e}")
            return None

    def create_payment_intent(
        self,
        amount: Decimal,
        currency: str = "usd",
        customer_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None
    ) -> Optional[stripe.PaymentIntent]:
        """
        Create a payment intent.

        Args:
            amount: Amount in dollars (will be converted to cents)
            currency: Currency code (default: usd)
            customer_id: Stripe customer ID
            metadata: Additional metadata
            description: Payment description

        Returns:
            Stripe PaymentIntent object or None if failed
        """
        try:
            # Convert dollars to cents
            amount_cents = int(amount * 100)

            params = {
                "amount": amount_cents,
                "currency": currency,
                "metadata": metadata or {},
            }

            if customer_id:
                params["customer"] = customer_id
            if description:
                params["description"] = description

            payment_intent = stripe.PaymentIntent.create(**params)
            logger.info(f"Payment intent created: {payment_intent.id} for ${amount}")
            return payment_intent

        except stripe.error.StripeError as e:
            logger.error(f"Failed to create payment intent: {e}")
            return None

    def confirm_payment_intent(
        self,
        payment_intent_id: str,
        payment_method: Optional[str] = None
    ) -> Optional[stripe.PaymentIntent]:
        """Confirm a payment intent."""
        try:
            params = {}
            if payment_method:
                params["payment_method"] = payment_method

            payment_intent = stripe.PaymentIntent.confirm(payment_intent_id, **params)
            logger.info(f"Payment intent confirmed: {payment_intent_id}")
            return payment_intent

        except stripe.error.StripeError as e:
            logger.error(f"Failed to confirm payment intent {payment_intent_id}: {e}")
            return None

    def cancel_payment_intent(
        self,
        payment_intent_id: str
    ) -> Optional[stripe.PaymentIntent]:
        """Cancel a payment intent."""
        try:
            payment_intent = stripe.PaymentIntent.cancel(payment_intent_id)
            logger.info(f"Payment intent canceled: {payment_intent_id}")
            return payment_intent
        except stripe.error.StripeError as e:
            logger.error(f"Failed to cancel payment intent {payment_intent_id}: {e}")
            return None

    def create_subscription(
        self,
        customer_id: str,
        price_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[stripe.Subscription]:
        """
        Create a subscription for a customer.

        Args:
            customer_id: Stripe customer ID
            price_id: Stripe price ID
            metadata: Additional metadata

        Returns:
            Stripe Subscription object or None if failed
        """
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": price_id}],
                metadata=metadata or {}
            )
            logger.info(f"Subscription created: {subscription.id} for customer {customer_id}")
            return subscription
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create subscription: {e}")
            return None

    def cancel_subscription(
        self,
        subscription_id: str,
        at_period_end: bool = True
    ) -> Optional[stripe.Subscription]:
        """Cancel a subscription."""
        try:
            if at_period_end:
                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True
                )
            else:
                subscription = stripe.Subscription.delete(subscription_id)

            logger.info(f"Subscription canceled: {subscription_id}")
            return subscription
        except stripe.error.StripeError as e:
            logger.error(f"Failed to cancel subscription {subscription_id}: {e}")
            return None

    def create_refund(
        self,
        payment_intent_id: str,
        amount: Optional[int] = None,
        reason: Optional[str] = None
    ) -> Optional[stripe.Refund]:
        """
        Create a refund for a payment.

        Args:
            payment_intent_id: Payment intent ID to refund
            amount: Amount to refund in cents (None for full refund)
            reason: Reason for refund

        Returns:
            Stripe Refund object or None if failed
        """
        try:
            params = {"payment_intent": payment_intent_id}

            if amount:
                params["amount"] = amount
            if reason:
                params["reason"] = reason

            refund = stripe.Refund.create(**params)
            logger.info(f"Refund created: {refund.id} for payment {payment_intent_id}")
            return refund
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create refund for {payment_intent_id}: {e}")
            return None

    def construct_webhook_event(
        self,
        payload: bytes,
        sig_header: str,
        webhook_secret: str
    ) -> Optional[stripe.Event]:
        """
        Construct and verify a webhook event from Stripe.

        Args:
            payload: Request body
            sig_header: Stripe signature header
            webhook_secret: Webhook secret from Stripe dashboard

        Returns:
            Stripe Event object or None if verification fails
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
            return event
        except ValueError as e:
            logger.error(f"Invalid webhook payload: {e}")
            return None
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid webhook signature: {e}")
            return None


# Global Stripe client instance
stripe_client = StripeClient()
