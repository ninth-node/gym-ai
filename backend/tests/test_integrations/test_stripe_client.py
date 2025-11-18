"""
Tests for Stripe integration.
"""

import pytest
from unittest.mock import Mock, patch
from app.core.integrations.stripe_client import StripeClient


def test_stripe_client_init():
    """Test Stripe client initialization."""
    client = StripeClient()
    assert client.api_key is not None


@patch('app.core.integrations.stripe_client.stripe.Customer.create')
def test_create_customer(mock_create):
    """Test creating a Stripe customer."""
    # Mock Stripe response
    mock_customer = Mock()
    mock_customer.id = "cus_test123"
    mock_create.return_value = mock_customer

    client = StripeClient()
    customer = client.create_customer(
        email="test@example.com",
        name="Test User"
    )

    assert customer is not None
    assert customer.id == "cus_test123"


@patch('app.core.integrations.stripe_client.stripe.PaymentIntent.create')
def test_create_payment_intent(mock_create):
    """Test creating a payment intent."""
    # Mock Stripe response
    mock_intent = Mock()
    mock_intent.id = "pi_test123"
    mock_create.return_value = mock_intent

    client = StripeClient()
    intent = client.create_payment_intent(
        amount=99.99,
        customer_id="cus_test123"
    )

    assert intent is not None
    assert intent.id == "pi_test123"
