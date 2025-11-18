from sqlalchemy import Boolean, Column, DateTime, Integer, String, Numeric, Text
from sqlalchemy.sql import func
from app.db.base import Base


class MembershipPlan(Base):
    __tablename__ = "membership_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    duration_days = Column(Integer, nullable=False)  # 30 for monthly, 365 for yearly
    is_active = Column(Boolean, default=True, nullable=False)
    features = Column(Text, nullable=True)  # JSON string of features
    max_classes_per_month = Column(Integer, nullable=True)  # null = unlimited
    has_personal_trainer = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<MembershipPlan {self.name}>"
