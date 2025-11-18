from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from app.models.member import MembershipStatus


# Membership Plan Schemas
class MembershipPlanBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    duration_days: int
    features: Optional[str] = None
    max_classes_per_month: Optional[int] = None
    has_personal_trainer: bool = False


class MembershipPlanCreate(MembershipPlanBase):
    pass


class MembershipPlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    duration_days: Optional[int] = None
    features: Optional[str] = None
    max_classes_per_month: Optional[int] = None
    has_personal_trainer: Optional[bool] = None
    is_active: Optional[bool] = None


class MembershipPlanResponse(MembershipPlanBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Member Schemas
class MemberBase(BaseModel):
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    fitness_goals: Optional[str] = None
    medical_conditions: Optional[str] = None
    preferred_workout_time: Optional[str] = None


class MemberCreate(MemberBase):
    user_id: int
    membership_plan_id: Optional[int] = None


class MemberUpdate(MemberBase):
    membership_plan_id: Optional[int] = None
    membership_status: Optional[MembershipStatus] = None


class MemberResponse(MemberBase):
    id: int
    user_id: int
    membership_plan_id: Optional[int] = None
    membership_status: MembershipStatus
    membership_start_date: Optional[date] = None
    membership_end_date: Optional[date] = None
    qr_code: Optional[str] = None
    total_check_ins: int
    last_check_in: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Check-in Schemas
class CheckInCreate(BaseModel):
    member_id: int
    method: Optional[str] = "manual"
    notes: Optional[str] = None


class CheckOutUpdate(BaseModel):
    notes: Optional[str] = None


class CheckInResponse(BaseModel):
    id: int
    member_id: int
    check_in_time: datetime
    check_out_time: Optional[datetime] = None
    method: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
