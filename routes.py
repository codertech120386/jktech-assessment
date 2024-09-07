from fastapi import APIRouter

from src.auth import auth_router
from src.books import books_router
from src.home import home_router

router = APIRouter(
    prefix="/api/v1",
    responses={404: {"description": "Not found"}},
)

router.include_router(auth_router)
router.include_router(books_router)
router.include_router(home_router)
