import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User


@pytest_asyncio.fixture
async def user(session: AsyncSession) -> User:
    """Create separate User for every test"""
    user = User(
        email="test@example.com",
        password="test",
        first_name="Test",
        last_name="User",
        hashed_password="hashed_pass",
        age=10,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    yield user

    await session.delete(user)
    await session.commit()
