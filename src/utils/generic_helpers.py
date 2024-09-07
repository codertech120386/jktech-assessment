from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import re


class DatabaseException(Exception):
    def __init__(self, value):
        self.value = value


def exception_handler_function(app):
    @app.exception_handler(DatabaseException)
    async def database_exception_handler(request: Request, exception: DatabaseException):
        return JSONResponse(status_code=500, content={'message': exception.value})


def cors_middleware(app):
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def generic_response(response_body):
    return JSONResponse(content=response_body, status_code=response_body.get("status_code"))


def check_email(email):
    """Function to check valid email"""

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if re.fullmatch(regex, email):
        return True

    return False
