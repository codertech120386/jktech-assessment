from fastapi import HTTPException, status

from src.auth.models import User


def check_user_with_email_exists(session, email: str):
    return session.query(User).filter(
        User.email == email).first()


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
        print(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")
