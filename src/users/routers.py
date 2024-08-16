from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.users.schemas import UserList

router = APIRouter()


@router.get("/users")
async def get_users(
    session: AsyncSession = Depends(get_session),
) -> list[UserList]:
    """Get all users."""
    users = await get_users(session)
    return [UserList.from_orm(user) for user in users]
