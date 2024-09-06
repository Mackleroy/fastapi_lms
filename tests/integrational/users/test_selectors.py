import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.settings import Settings
from src.users.models import User


@pytest.mark.asyncio
async def test_get_users(client: AsyncClient, session: AsyncSession, settings: Settings):
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

    response = await client.get(f"/api/v1/users")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["email"] == "test@example.com"



