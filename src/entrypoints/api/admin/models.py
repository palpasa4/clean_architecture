from pydantic.main import BaseModel
from pydantic import EmailStr, SecretStr
from pydantic.main import BaseModel


class CreateAdminModel(BaseModel):
    username: str
    password: str
    fullname: str
    email: EmailStr


class AdminLoginModel(BaseModel):
    username: str
    password: SecretStr


class ListUserParams(BaseModel):
    page_number: int | None = None
    page_size: int | None = None
    user_id: str | None = None


# class Token(BaseModel):
#     access_token: str
#     token_type: str
