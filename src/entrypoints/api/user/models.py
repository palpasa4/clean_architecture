from pydantic import BaseModel, SecretStr


class CreateUserModel(BaseModel):
    username: str
    fullname: str
    address: str
    contact_no: str
    opening_balance: float


class UserLoginModel(BaseModel):
    username: str
    password: SecretStr


class AmountModel(BaseModel):
    amount: float
