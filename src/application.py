from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.db import sessionmanager
from src.users.routers import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    sessionmanager.init_db()
    yield
    sessionmanager.close()


app: FastAPI = FastAPI(title="lms", lifespan=lifespan)
app.include_router(user_router, prefix="/api/v1", tags=["api_v1"])
