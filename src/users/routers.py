from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.users.schemas import UserList, UserDetail
from src.users.selectors import get_users, get_user_by_id

router = APIRouter()


@router.get("/users", name="user-list")
async def get_users_router(
    session: AsyncSession = Depends(get_session),
) -> list[UserList]:
    """Get all users."""
    users = await get_users(session)
    return [UserList.from_orm(user) for user in users]


@router.get("/users/{user_id}", name="user-detail")
async def get_user_by_id_router(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> UserDetail:
    """Get detail information about user."""
    user = await get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserDetail.from_orm(user)
