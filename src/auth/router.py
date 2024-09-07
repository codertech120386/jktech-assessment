from fastapi import APIRouter, Depends
from src.auth import RegistrationSchema, LoginSchema, register, login
from database import SessionLocal, get_db

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Auth routes Not found"}},
)


@auth_router.post('/register')
def register_user(user: RegistrationSchema, session: SessionLocal = Depends(get_db)):
    return register(user, session)


@auth_router.post('/login')
def login_user(user: LoginSchema, session: SessionLocal = Depends(get_db)):
    return login(user, session)
