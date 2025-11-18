from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    ForeignKey,
    Date,
    Text,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class MembershipStatus(str, enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    SUSPENDED = "suspended"


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    membership_plan_id = Column(
        Integer, ForeignKey("membership_plans.id"), nullable=True
    )
    membership_status = Column(
        SQLEnum(MembershipStatus, name="membership_status"),
        default=MembershipStatus.ACTIVE,
        nullable=False,
    )
    membership_start_date = Column(Date, nullable=True)
    membership_end_date = Column(Date, nullable=True)

    # Personal Information
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    emergency_contact_name = Column(String, nullable=True)
    emergency_contact_phone = Column(String, nullable=True)

    # Fitness Information
    fitness_goals = Column(Text, nullable=True)
    medical_conditions = Column(Text, nullable=True)
    preferred_workout_time = Column(String, nullable=True)

    # QR Code for Check-in
    qr_code = Column(String, unique=True, nullable=True)

    # Tracking
    total_check_ins = Column(Integer, default=0, nullable=False)
    last_check_in = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user = relationship("User", backref="member_profile")
    membership_plan = relationship("MembershipPlan")

    def __repr__(self):
        return f"<Member {self.user_id}>"
