import re
from fastapi import HTTPException, status

from src.utils import generic_response, get_hashed_password, create_access_token, check_email, verify_password
from .service import check_user_with_email_exists, add_user
from .schema import LoginSchema


def register(user, session):
    try:
        name, email, password, confirm_password = user.name, user.email, user.password, user.confirm_password
        errors = register_validations(confirm_password, email, name, password)

        if len(errors) > 0:
            errors_string = "\n".join(errors)
            return generic_response(
                {"message": f"Please check below errors and fix them \n {errors_string}",
                 "status_code": status.HTTP_400_BAD_REQUEST})

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


def login(user: LoginSchema, session):
    try:
        email, password = user.email, user.password

        errors = login_validations(email=email, password=password)
        if len(errors) > 0:
            errors_string = "\n".join(errors)
            return generic_response(
                {"message": f"Please check below errors and fix them \n {errors_string}",
                 "status_code": status.HTTP_400_BAD_REQUEST})

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


def login_validations(email: str, password: str):
    errors = []
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        errors.append("Please provide a valid email\n")
    if len(password) < 6 or len(password) > 20:
        errors.append("Password must be between 6 characters and 20 characters long\n")

    return errors


def register_validations(confirm_password, email, name, password):
    errors = []
    if len(name) < 2 or len(name) > 50:
        errors.append("Name must be between 2 characters and 50 characters long\n")
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        errors.append("Please provide a valid email\n")
    if len(password) < 6 or len(password) > 20:
        errors.append("Password must be between 6 characters and 20 characters long\n")
    if len(confirm_password) < 6 or len(confirm_password) > 20:
        errors.append("Confirm Password must be between 6 characters and 20 characters long\n")
    if password != confirm_password:
        errors.append("Password and Confirm Password are not same \n")
    return errors
