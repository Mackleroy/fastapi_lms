import pytest
from httpx import AsyncClient

from src.users.models import User


@pytest.mark.asyncio
async def test_get_users_router(user: User, client: AsyncClient):
    """Test list of users"""
    response = await client.get("/api/v1/users")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["email"] == user.email


@pytest.mark.asyncio
async def test_get_user_by_id_router(user: User, client: AsyncClient):
    """Test detail of users"""
    response = await client.get(f"/api/v1/users/{user.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user.email
