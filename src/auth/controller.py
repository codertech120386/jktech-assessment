import re
from fastapi import HTTPException, status

from src.utils import generic_response, get_hashed_password, create_access_token, check_email, verify_password, errors_response
from database import SessionLocal

from .service import check_user_with_email_exists, add_user
from .schema import LoginSchema, RegistrationSchema
from .validators import login_validations, register_validations


def register(user: RegistrationSchema, session: SessionLocal):
    try:
        name, email, password, confirm_password = user.name, user.email, user.password, user.confirm_password
        errors = register_validations(confirm_password, email, name, password)

        if len(errors) > 0:
            return errors_response(errors)

        if check_user_with_email_exists(session=session, email=email):
            return generic_response(
                {"message": "Email already exist.", "status_code": status.HTTP_400_BAD_REQUEST})

        password = get_hashed_password(password)

        new_user = add_user(session=session, user=user, password=password)
        data = {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
        }

        data["token"] = create_access_token(data)

        return generic_response({"data": data, "status_code": status.HTTP_201_CREATED})
    except Exception as e:
        return generic_response({"message": "Something went wrong", "status_code": 500})


def login(user: LoginSchema, session: SessionLocal):
    try:
        email, password = user.email, user.password

        errors = login_validations(email=email, password=password)
        if len(errors) > 0:
            return errors_response(errors)

        if not check_email(email):
            return HTTPException(400, detail="Invalid Email")

        user = check_user_with_email_exists(session=session, email=email)
        if not user:
            return generic_response(
                {"message": "email or password does not match.",
                 "status_code": status.HTTP_400_BAD_REQUEST})

        if not verify_password(password, user.password):
            return HTTPException(401, detail="email or password does not match.")

        data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }

        data["token"] = create_access_token(data)

        return generic_response({"data": data, "status_code": status.HTTP_200_OK})
    except Exception as e:
        return generic_response({"message": "Something went wrong", "status_code": 500})
