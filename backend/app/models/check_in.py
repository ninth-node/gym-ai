from sqlalchemy import Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class CheckIn(Base):
    __tablename__ = "check_ins"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    check_in_time = Column(DateTime(timezone=True), server_default=func.now())
    check_out_time = Column(DateTime(timezone=True), nullable=True)
    method = Column(String, nullable=True)  # qr_code, manual, biometric
    notes = Column(String, nullable=True)

    # Relationship
    member = relationship("Member", backref="check_ins")

    def __repr__(self):
        return f"<CheckIn {self.member_id} at {self.check_in_time}>"
