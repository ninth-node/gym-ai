from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user."""
    user = await AuthService.register_user(db, user_data)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    """Login user and return JWT tokens."""
    user = await AuthService.authenticate_user(db, credentials)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return AuthService.create_tokens(user)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """Get current user information."""
    return current_user


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    current_user: User = Depends(get_current_user),
):
    """Refresh access token."""
    return AuthService.create_tokens(current_user)
