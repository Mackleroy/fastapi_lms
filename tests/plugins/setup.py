import asyncio
import os
from copy import deepcopy
from typing import AsyncIterator

import httpx
import pytest
import pytest_asyncio
from alembic.command import upgrade, downgrade
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from alembic.config import Config

from src import app
from src.db import get_session
from src.settings import Settings, get_settings, settings


engine = create_async_engine(settings.database.database_url, echo=True)
async_session_maker = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database(event_loop):
    """Fixture to setup database with teardown logic

    Args:
        event_loop: was imported for proper ordering of fixtures setup
            and teardown
    """
    parent = os.path.dirname
    project_root = parent(parent(parent(os.path.abspath(__file__))))
    config = Config(project_root + "/alembic.ini")
    config.set_main_option('script_location', project_root + '/alembic')

    async with engine.connect() as c:
        await c.run_sync(lambda _: downgrade(config, "base"))
        await c.run_sync(lambda _: upgrade(config, "head"))

    yield

    async with engine.connect() as c:
        await c.run_sync(lambda _: downgrade(config, "base"))


async def manage_test_session() -> AsyncIterator[AsyncSession]:
    """
    Common function to manage the session lifecycle for testing.
    Handles session creation, rollback, and closure.
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


async def get_test_session() -> AsyncIterator[AsyncSession]:
    """
    Reuse the session management logic for overwrite dependency.
    """
    async for session in manage_test_session():
        yield session


@pytest_asyncio.fixture
async def session() -> AsyncIterator[AsyncSession]:
    """
    Fixture to provide a session for tests, using the common session management logic.
    """
    async for session in manage_test_session():
        yield session


@pytest.fixture(scope="session")
def settings_base() -> Settings:
    """Settings object as is"""
    return get_settings()


@pytest.fixture
def settings(settings_base) -> AsyncIterator[Settings]:
    """Current settings for app

    Teardown logic was implemented to restore original settings
    so one test will not affect other tests

    Args:
        settings_base:  base settings object as is
    """
    params_back_up = {}
    for field in Settings.model_fields.keys():
        params_back_up[field] = deepcopy(getattr(settings_base, field))

    yield settings_base

    for field, value in params_back_up.items():
        setattr(settings_base, field, value)


@pytest_asyncio.fixture()
async def client() -> AsyncIterator[httpx.AsyncClient]:
    """Asynchronous client for testing purposes"""
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as c:
        yield c


@pytest.fixture(autouse=True)
def override_settings():
    """Override settings or dependencies for tests"""
    app.dependency_overrides[get_session] = get_test_session
    yield
    app.dependency_overrides.clear()