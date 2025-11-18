from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Enum as SQLEnum,
    Text,
)
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class EquipmentStatus(str, enum.Enum):
    OPERATIONAL = "operational"
    MAINTENANCE_NEEDED = "maintenance_needed"
    UNDER_MAINTENANCE = "under_maintenance"
    OUT_OF_SERVICE = "out_of_service"


class EquipmentCategory(str, enum.Enum):
    CARDIO = "cardio"
    STRENGTH = "strength"
    FREE_WEIGHTS = "free_weights"
    FUNCTIONAL = "functional"
    OTHER = "other"


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(
        SQLEnum(EquipmentCategory, name="equipment_category"),
        nullable=False,
    )
    model = Column(String, nullable=True)
    serial_number = Column(String, unique=True, nullable=True)
    status = Column(
        SQLEnum(EquipmentStatus, name="equipment_status"),
        default=EquipmentStatus.OPERATIONAL,
        nullable=False,
    )

    # Usage tracking
    total_usage_count = Column(Integer, default=0, nullable=False)
    total_usage_hours = Column(Integer, default=0, nullable=False)  # In hours
    last_used_at = Column(DateTime(timezone=True), nullable=True)

    # Maintenance tracking
    last_maintenance_date = Column(DateTime(timezone=True), nullable=True)
    next_maintenance_due = Column(DateTime(timezone=True), nullable=True)
    maintenance_notes = Column(Text, nullable=True)

    # Purchase information
    purchase_date = Column(DateTime(timezone=True), nullable=True)
    warranty_expiry = Column(DateTime(timezone=True), nullable=True)

    # IoT integration
    # TODO: Add IoT sensor integration fields
    iot_device_id = Column(String, unique=True, nullable=True)
    iot_last_sync = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<Equipment {self.name}>"
