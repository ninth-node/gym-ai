"""
Facility configuration model for configurable gym settings.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from datetime import datetime

from app.db.base import Base


class FacilityConfig(Base):
    """
    Facility configuration model for customizable gym settings.

    Allows gym managers to configure capacity, hours, and other settings
    without code changes.
    """

    __tablename__ = "facility_configs"

    id = Column(Integer, primary_key=True, index=True)

    # Facility identification
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)

    # Capacity settings
    total_capacity = Column(Integer, nullable=False, default=100)
    equipment_capacity = Column(Integer, nullable=True)  # Max people on equipment at once
    class_capacity = Column(Integer, nullable=True)  # Max people in group classes

    # Peak hours capacity adjustments (JSON)
    # Format: {"morning": 80, "afternoon": 100, "evening": 120}
    peak_hours_capacity = Column(JSON, nullable=True)

    # Operating hours (JSON)
    # Format: {"monday": {"open": "06:00", "close": "22:00"}, ...}
    operating_hours = Column(JSON, nullable=True)

    # Facility metrics
    total_area_sqft = Column(Float, nullable=True)
    equipment_count = Column(Integer, nullable=True)
    training_rooms = Column(Integer, nullable=True)

    # Maintenance settings
    deep_cleaning_frequency_days = Column(Integer, default=30)
    equipment_inspection_frequency_days = Column(Integer, default=14)

    # Features and amenities (JSON)
    # Format: ["showers", "lockers", "parking", "wifi", "cafe"]
    amenities = Column(JSON, nullable=True)

    # HVAC and environmental settings
    target_temperature = Column(Float, nullable=True, default=72.0)  # Fahrenheit
    humidity_target = Column(Float, nullable=True, default=50.0)  # Percentage

    # Notifications and alerts
    occupancy_alert_threshold = Column(Float, default=0.9)  # 90% capacity
    enable_occupancy_alerts = Column(Boolean, default=True)
    enable_maintenance_alerts = Column(Boolean, default=True)

    # Active flag
    is_active = Column(Boolean, default=True, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<FacilityConfig(name='{self.name}', capacity={self.total_capacity})>"

    def get_current_capacity(self, hour: int = None) -> int:
        """
        Get the capacity for a specific hour, accounting for peak hours.

        Args:
            hour: Hour of day (0-23), if None uses default capacity

        Returns:
            Adjusted capacity
        """
        if hour is None or not self.peak_hours_capacity:
            return self.total_capacity

        # Determine time period
        if 5 <= hour < 12:
            period = "morning"
        elif 12 <= hour < 17:
            period = "afternoon"
        elif 17 <= hour < 22:
            period = "evening"
        else:
            period = "night"

        return self.peak_hours_capacity.get(period, self.total_capacity)

    def is_over_capacity(self, current_occupancy: int, hour: int = None) -> bool:
        """Check if facility is over capacity."""
        capacity = self.get_current_capacity(hour)
        return current_occupancy > capacity

    def get_occupancy_percentage(self, current_occupancy: int, hour: int = None) -> float:
        """Calculate occupancy percentage."""
        capacity = self.get_current_capacity(hour)
        return (current_occupancy / capacity * 100) if capacity > 0 else 0

    def should_send_occupancy_alert(self, current_occupancy: int, hour: int = None) -> bool:
        """Determine if occupancy alert should be sent."""
        if not self.enable_occupancy_alerts:
            return False

        occupancy_pct = self.get_occupancy_percentage(current_occupancy, hour) / 100
        return occupancy_pct >= self.occupancy_alert_threshold
