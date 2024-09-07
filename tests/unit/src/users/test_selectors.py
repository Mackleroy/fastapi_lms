from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User
from src.users.selectors import get_users, get_user_by_id


async def test_get_users(user: User, session: AsyncSession):
    """Test selector returns all users"""
    second_user = User(
        email="test_1@example.com",
        password="test_1",
        first_name="Test_1",
        last_name="User_1",
        hashed_password="hashed_pass_1",
        age=11,
    )
    session.add(second_user)
    await session.commit()

    result = await get_users(session)

    assert len(result) == 2  # first from fixture


async def test_get_user_by_id(user: User, session: AsyncSession):
    """Test selector returns user by id"""
    assert user.id is not None

    result = await get_user_by_id(session, user_id=user.id)

    assert isinstance(result, User)
    assert result.id == user.id
