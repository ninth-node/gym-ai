from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.membership_plan import MembershipPlan
from app.schemas.member import MembershipPlanCreate, MembershipPlanUpdate


class MembershipPlanService:
    @staticmethod
    async def create_plan(
        db: AsyncSession, plan_data: MembershipPlanCreate
    ) -> MembershipPlan:
        """Create a new membership plan."""
        db_plan = MembershipPlan(**plan_data.model_dump())
        db.add(db_plan)
        await db.commit()
        await db.refresh(db_plan)
        return db_plan

    @staticmethod
    async def get_plan(
        db: AsyncSession, plan_id: int
    ) -> Optional[MembershipPlan]:
        """Get membership plan by ID."""
        result = await db.execute(
            select(MembershipPlan).where(MembershipPlan.id == plan_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_plans(
        db: AsyncSession, skip: int = 0, limit: int = 100, active_only: bool = True
    ) -> List[MembershipPlan]:
        """Get all membership plans."""
        query = select(MembershipPlan)
        if active_only:
            query = query.where(MembershipPlan.is_active == True)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update_plan(
        db: AsyncSession, plan_id: int, plan_data: MembershipPlanUpdate
    ) -> Optional[MembershipPlan]:
        """Update membership plan."""
        result = await db.execute(
            select(MembershipPlan).where(MembershipPlan.id == plan_id)
        )
        plan = result.scalar_one_or_none()

        if not plan:
            return None

        for field, value in plan_data.model_dump(exclude_unset=True).items():
            setattr(plan, field, value)

        await db.commit()
        await db.refresh(plan)
        return plan

    @staticmethod
    async def delete_plan(db: AsyncSession, plan_id: int) -> bool:
        """Soft delete membership plan."""
        result = await db.execute(
            select(MembershipPlan).where(MembershipPlan.id == plan_id)
        )
        plan = result.scalar_one_or_none()

        if not plan:
            return False

        plan.is_active = False
        await db.commit()
        return True
