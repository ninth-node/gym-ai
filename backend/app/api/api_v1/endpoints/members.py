from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.member import (
    MemberCreate,
    MemberUpdate,
    MemberResponse,
    CheckInCreate,
    CheckInResponse,
    CheckOutUpdate,
)
from app.services.member_service import MemberService
from app.core.dependencies import get_current_user, require_role
from app.models.user import User, UserRole

router = APIRouter()


@router.post(
    "/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED
)
async def create_member(
    member_data: MemberCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.STAFF)),
):
    """Create a new member profile."""
    return await MemberService.create_member(db, member_data)


@router.get("/", response_model=List[MemberResponse])
async def list_members(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.STAFF)),
):
    """Get all members."""
    return await MemberService.get_members(db, skip=skip, limit=limit)


@router.get("/{member_id}", response_model=MemberResponse)
async def get_member(
    member_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get member by ID."""
    member = await MemberService.get_member(db, member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )

    # Members can only view their own profile, staff can view all
    if (
        current_user.role == UserRole.MEMBER
        and member.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this member",
        )

    return member


@router.get("/user/{user_id}", response_model=MemberResponse)
async def get_member_by_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get member by user ID."""
    member = await MemberService.get_member_by_user_id(db, user_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )

    # Members can only view their own profile
    if current_user.role == UserRole.MEMBER and user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this member",
        )

    return member


@router.put("/{member_id}", response_model=MemberResponse)
async def update_member(
    member_id: int,
    member_data: MemberUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update member profile."""
    member = await MemberService.get_member(db, member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )

    # Members can only update their own profile, except membership status
    if current_user.role == UserRole.MEMBER:
        if member.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this member",
            )
        # Members cannot change their membership status or plan
        if (
            member_data.membership_status is not None
            or member_data.membership_plan_id is not None
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to change membership details",
            )

    return await MemberService.update_member(db, member_id, member_data)


@router.post("/check-in", response_model=CheckInResponse)
async def check_in(
    check_in_data: CheckInCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.STAFF)),
):
    """Check in a member."""
    return await MemberService.check_in_member(db, check_in_data)


@router.put("/check-out/{check_in_id}", response_model=CheckInResponse)
async def check_out(
    check_in_id: int,
    check_out_data: CheckOutUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.STAFF)),
):
    """Check out a member."""
    check_in = await MemberService.check_out_member(
        db, check_in_id, check_out_data
    )
    if not check_in:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Check-in not found"
        )
    return check_in


@router.get("/dashboard/stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.STAFF)),
):
    """Get dashboard statistics."""
    return await MemberService.get_dashboard_stats(db)
