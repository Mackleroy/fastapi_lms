from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from src.users.models import User


async def get_users(session: AsyncSession) -> Sequence[User]:
    """Get users, all at this very moment

    Args:
        session (AsyncSession): database session
    """
    return (await session.scalars(select(User).order_by(col(User.id)))).all()
