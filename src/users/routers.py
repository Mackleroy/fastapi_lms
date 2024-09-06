from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.users.schemas import UserList
from src.users.selectors import get_users

router = APIRouter()


@router.get("/users", name="user-list")
async def get_users_router(
    session: AsyncSession = Depends(get_session),
) -> list[UserList]:
    """Get all users."""
    users = await get_users(session)
    return [UserList.from_orm(user) for user in users]
