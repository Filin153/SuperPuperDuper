from fastapi import APIRouter
from .user import router as u_router

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

router.include_router(u_router)