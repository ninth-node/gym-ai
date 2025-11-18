"""
Tests for FacilityConfig model.
"""

import pytest
from app.models.facility_config import FacilityConfig


def test_facility_config_creation():
    """Test creating a facility config."""
    config = FacilityConfig(
        name="Test Gym",
        location="123 Main St",
        total_capacity=100
    )

    assert config.name == "Test Gym"
    assert config.total_capacity == 100
    assert config.is_active is True


def test_get_current_capacity():
    """Test getting capacity for different hours."""
    config = FacilityConfig(
        name="Test Gym",
        total_capacity=100,
        peak_hours_capacity={
            "morning": 80,
            "afternoon": 100,
            "evening": 120,
            "night": 50
        }
    )

    # Morning hours (5-11)
    assert config.get_current_capacity(8) == 80

    # Afternoon hours (12-16)
    assert config.get_current_capacity(14) == 100

    # Evening hours (17-21)
    assert config.get_current_capacity(19) == 120

    # Night hours
    assert config.get_current_capacity(2) == 50

    # No hour specified
    assert config.get_current_capacity() == 100


def test_is_over_capacity():
    """Test checking if facility is over capacity."""
    config = FacilityConfig(
        name="Test Gym",
        total_capacity=100
    )

    assert config.is_over_capacity(90) is False
    assert config.is_over_capacity(100) is False
    assert config.is_over_capacity(110) is True


def test_get_occupancy_percentage():
    """Test calculating occupancy percentage."""
    config = FacilityConfig(
        name="Test Gym",
        total_capacity=100
    )

    assert config.get_occupancy_percentage(50) == 50.0
    assert config.get_occupancy_percentage(100) == 100.0
    assert config.get_occupancy_percentage(0) == 0.0


def test_should_send_occupancy_alert():
    """Test determining if occupancy alert should be sent."""
    config = FacilityConfig(
        name="Test Gym",
        total_capacity=100,
        occupancy_alert_threshold=0.9,
        enable_occupancy_alerts=True
    )

    # Below threshold
    assert config.should_send_occupancy_alert(80) is False

    # At threshold
    assert config.should_send_occupancy_alert(90) is True

    # Above threshold
    assert config.should_send_occupancy_alert(95) is True

    # Alerts disabled
    config.enable_occupancy_alerts = False
    assert config.should_send_occupancy_alert(95) is False
