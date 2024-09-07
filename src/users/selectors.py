from typing import Sequence, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select

from src.users.models import User


async def get_users(session: AsyncSession) -> Sequence[User]:
    """Get users, all at this very moment

    Args:
        session (AsyncSession): database session
    """
    return (await session.scalars(select(User).order_by(col(User.id)))).all()


async def get_user_by_id(
    session: AsyncSession,
    user_id: int,
) -> Optional[User]:
    """Get user by id if exists.

    Args:
        session (AsyncSession): database session
        user_id (int): user identifier
    """
    return await session.get(User, user_id)
