from fastapi import APIRouter

from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
