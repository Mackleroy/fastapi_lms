from asyncio import current_task
from typing import AsyncIterator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from src.settings import settings


class DatabaseSessionManager:
    def __init__(self):
        self.engine: Optional[AsyncEngine] = None
        self.session_maker = None
        self.session = None

    def init_db(self):
        # Creating an asynchronous engine
        self.engine = create_async_engine(
            settings.database_url,
            pool_size=100,
            max_overflow=0,
            pool_pre_ping=False,
        )

        # Creating an asynchronous session class
        self.session_maker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        # Creating a scoped session
        self.session = async_scoped_session(
            self.session_maker,
            scopefunc=current_task,
        )

    async def close(self):
        # Closing the database session...
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self.engine.dispose()


# Initialize the DatabaseSessionManager
sessionmanager = DatabaseSessionManager()


async def get_session() -> AsyncIterator[AsyncSession]:
    session = sessionmanager.session()
    if session is None:
        raise Exception("DatabaseSessionManager is not initialized")
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        # Closing the session after use...
        await session.close()
