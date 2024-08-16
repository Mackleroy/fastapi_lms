from fastapi import FastAPI

from src.db import sessionmanager
from src.users.routers import router as user_router

app: FastAPI = FastAPI(title="lms")
app.include_router(user_router, prefix="/api/v1", tags=["api_v1"])


@app.on_event("startup")
async def startup():
    sessionmanager.init_db()


@app.on_event("shutdown")
async def shutdown():
    pass
