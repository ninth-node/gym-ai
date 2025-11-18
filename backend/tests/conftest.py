"""
Pytest configuration and fixtures for test suite.
"""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.db.base import Base
from app.core.config import settings


# Test database URL (use separate test database)
TEST_DATABASE_URL = settings.DATABASE_URL.replace("/gym_ai", "/gym_ai_test")


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_db():
    """
    Create a fresh database for each test.
    """
    # Create async engine
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
        echo=False
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    # Cleanup
    await engine.dispose()


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "full_name": "Test User",
        "role": "member"
    }


@pytest.fixture
def sample_member_data():
    """Sample member data for testing."""
    return {
        "date_of_birth": "1990-01-01",
        "gender": "male",
        "fitness_goals": "Build muscle and improve endurance",
        "membership_plan_id": 1
    }


@pytest.fixture
def sample_payment_data():
    """Sample payment data for testing."""
    return {
        "amount": 99.99,
        "payment_method": "CARD",
        "description": "Monthly membership fee"
    }
