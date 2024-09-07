from pydantic import BaseModel


class RegistrationSchema(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "test",
                "email": "dummy@dummy.com",
                "password": "test",
                "confirm_password": "test"
            }
        }


class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "dummy@dummy.com",
                "password": "dummy@123"
            }
        }
