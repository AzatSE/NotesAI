from fastapi import APIRouter

from app.api.routers import users,tasks
from app.core.config import settings

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(tasks.router)
