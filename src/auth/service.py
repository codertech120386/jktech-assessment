from fastapi import HTTPException, status
from icecream import ic

from src.auth.models import User


def check_user_with_email_exists(session, email: str):
    try:
        return session.query(User).filter(
            User.email == email).first()
    except Exception as e:
        ic(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")


def add_user(session, user, password):
    try:
        new_user = User(
            name=user.name,
            email=user.email,
            password=password
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user
    except Exception as e:
        ic(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")
