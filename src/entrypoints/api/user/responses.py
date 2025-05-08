from pydantic import BaseModel,SecretStr


class UserResponse(BaseModel):
    message: str
    id: str
    password: str
