import uuid
from datetime import datetime, timedelta, date
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status
from app.models.member import Member, MembershipStatus
from app.models.membership_plan import MembershipPlan
from app.models.check_in import CheckIn
from app.models.user import User
from app.schemas.member import (
    MemberCreate,
    MemberUpdate,
    CheckInCreate,
    CheckOutUpdate,
)


class MemberService:
    @staticmethod
    async def create_member(
        db: AsyncSession, member_data: MemberCreate
    ) -> Member:
        """Create a new member profile."""
        # Check if user exists
        result = await db.execute(
            select(User).where(User.id == member_data.user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # Check if member profile already exists
        result = await db.execute(
            select(Member).where(Member.user_id == member_data.user_id)
        )
        existing_member = result.scalar_one_or_none()
        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member profile already exists for this user",
            )

        # Generate QR code
        qr_code = str(uuid.uuid4())

        # Create member
        db_member = Member(
            **member_data.model_dump(),
            qr_code=qr_code,
        )

        # If membership plan is provided, set dates
        if member_data.membership_plan_id:
            result = await db.execute(
                select(MembershipPlan).where(
                    MembershipPlan.id == member_data.membership_plan_id
                )
            )
            plan = result.scalar_one_or_none()
            if plan:
                db_member.membership_start_date = date.today()
                db_member.membership_end_date = date.today() + timedelta(
                    days=plan.duration_days
                )

        db.add(db_member)
        await db.commit()
        await db.refresh(db_member)

        return db_member

    @staticmethod
    async def get_member(db: AsyncSession, member_id: int) -> Optional[Member]:
        """Get member by ID."""
        result = await db.execute(
            select(Member).where(Member.id == member_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_member_by_user_id(
        db: AsyncSession, user_id: int
    ) -> Optional[Member]:
        """Get member by user ID."""
        result = await db.execute(
            select(Member).where(Member.user_id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_members(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Member]:
        """Get all members."""
        result = await db.execute(select(Member).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def update_member(
        db: AsyncSession, member_id: int, member_data: MemberUpdate
    ) -> Optional[Member]:
        """Update member profile."""
        result = await db.execute(
            select(Member).where(Member.id == member_id)
        )
        member = result.scalar_one_or_none()

        if not member:
            return None

        # Update fields
        for field, value in member_data.model_dump(exclude_unset=True).items():
            setattr(member, field, value)

        # Update membership dates if plan changed
        if member_data.membership_plan_id:
            result = await db.execute(
                select(MembershipPlan).where(
                    MembershipPlan.id == member_data.membership_plan_id
                )
            )
            plan = result.scalar_one_or_none()
            if plan:
                member.membership_start_date = date.today()
                member.membership_end_date = date.today() + timedelta(
                    days=plan.duration_days
                )

        await db.commit()
        await db.refresh(member)

        return member

    @staticmethod
    async def check_in_member(
        db: AsyncSession, check_in_data: CheckInCreate
    ) -> CheckIn:
        """Check in a member."""
        # Verify member exists
        result = await db.execute(
            select(Member).where(Member.id == check_in_data.member_id)
        )
        member = result.scalar_one_or_none()

        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found",
            )

        # Create check-in
        check_in = CheckIn(**check_in_data.model_dump())
        db.add(check_in)

        # Update member stats
        member.total_check_ins += 1
        member.last_check_in = datetime.utcnow()

        await db.commit()
        await db.refresh(check_in)

        return check_in

    @staticmethod
    async def check_out_member(
        db: AsyncSession, check_in_id: int, check_out_data: CheckOutUpdate
    ) -> Optional[CheckIn]:
        """Check out a member."""
        result = await db.execute(
            select(CheckIn).where(CheckIn.id == check_in_id)
        )
        check_in = result.scalar_one_or_none()

        if not check_in:
            return None

        check_in.check_out_time = datetime.utcnow()
        if check_out_data.notes:
            check_in.notes = check_out_data.notes

        await db.commit()
        await db.refresh(check_in)

        return check_in

    @staticmethod
    async def get_dashboard_stats(db: AsyncSession) -> dict:
        """Get dashboard statistics."""
        # Total members
        total_members = await db.execute(select(func.count(Member.id)))
        total_members = total_members.scalar()

        # Active members
        active_members = await db.execute(
            select(func.count(Member.id)).where(
                Member.membership_status == MembershipStatus.ACTIVE
            )
        )
        active_members = active_members.scalar()

        # Today's check-ins
        today = datetime.utcnow().date()
        today_check_ins = await db.execute(
            select(func.count(CheckIn.id)).where(
                func.date(CheckIn.check_in_time) == today
            )
        )
        today_check_ins = today_check_ins.scalar()

        # Active check-ins (not checked out)
        active_check_ins = await db.execute(
            select(func.count(CheckIn.id)).where(CheckIn.check_out_time.is_(None))
        )
        active_check_ins = active_check_ins.scalar()

        return {
            "total_members": total_members,
            "active_members": active_members,
            "today_check_ins": today_check_ins,
            "active_check_ins": active_check_ins,
        }
