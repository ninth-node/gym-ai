from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.member import (
    MembershipPlanCreate,
    MembershipPlanUpdate,
    MembershipPlanResponse,
)
from app.services.membership_plan_service import MembershipPlanService
from app.core.dependencies import get_current_user, require_role
from app.models.user import User, UserRole

router = APIRouter()


@router.post(
    "/",
    response_model=MembershipPlanResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_plan(
    plan_data: MembershipPlanCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    """Create a new membership plan."""
    return await MembershipPlanService.create_plan(db, plan_data)


@router.get("/", response_model=List[MembershipPlanResponse])
async def list_plans(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all membership plans."""
    return await MembershipPlanService.get_plans(
        db, skip=skip, limit=limit, active_only=active_only
    )


@router.get("/{plan_id}", response_model=MembershipPlanResponse)
async def get_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get membership plan by ID."""
    plan = await MembershipPlanService.get_plan(db, plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership plan not found",
        )
    return plan


@router.put("/{plan_id}", response_model=MembershipPlanResponse)
async def update_plan(
    plan_id: int,
    plan_data: MembershipPlanUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    """Update membership plan."""
    plan = await MembershipPlanService.update_plan(db, plan_id, plan_data)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership plan not found",
        )
    return plan


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    """Delete (deactivate) membership plan."""
    success = await MembershipPlanService.delete_plan(db, plan_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership plan not found",
        )
    return None
