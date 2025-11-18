from sqlalchemy import Boolean, Column, DateTime, Integer, String, Enum as SQLEnum
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    STAFF = "staff"
    MEMBER = "member"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(
        SQLEnum(UserRole, name="user_role"),
        default=UserRole.MEMBER,
        nullable=False,
    )
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    phone_number = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    last_login = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<User {self.email}>"
