import os
from fastapi import HTTPException, Request
from jose import jwt
from icecream import ic
from bcrypt import gensalt, hashpw, checkpw


def get_hashed_password(password: str) -> str:
    byte_password = password.encode('utf-8')
    my_salt = gensalt()
    byte_hashed_password = hashpw(byte_password, my_salt)
    return byte_hashed_password.decode('utf-8')


def verify_password(password: str, hashed_pass: str) -> bool:
    byte_password = password.encode('utf-8')
    byte_hashed_password = hashed_pass.encode('utf-8')
    return checkpw(byte_password, byte_hashed_password)


def create_access_token(to_encode):
    return jwt.encode(to_encode, os.environ.get("JWT_SECRET_KEY"), "HS256")


def decode_access_token(token: str):
    jwt_token = token.split(" ")[1]
    payload = jwt.decode(
        jwt_token, os.environ.get("JWT_SECRET_KEY"), algorithms=['HS256'])
    return payload


def verify_token(request: Request):
    try:
        authorization = request.headers.get('authorization')

        user = decode_access_token(authorization)

        if authorization == "":
            raise HTTPException(status_code=401, detail="Unauthorized")

        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if "id" in user and user['id'] == 411:
            raise HTTPException(status_code=401, detail="Unauthorized")

        return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Unauthorized")
