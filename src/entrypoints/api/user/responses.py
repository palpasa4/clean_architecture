from pydantic import BaseModel,SecretStr
from datetime import datetime


class UserResponseModel(BaseModel):
    message: str
    id: str
    password: str


class TokenResponseModel(BaseModel):
    access_token: str


class TransactionResponse(BaseModel):
    message: str
    transaction_type: str
    transaction_amount: float
    previous_balance: float
    new_balance: float


class UserViewDetailsModel(BaseModel):
    cust_id: str
    username: str
    bank_acc_id: str
    fullname: str
    address: str
    contact_no: str
    balance: float
    updated_at: datetime


class UserTransactionDetailsModel(BaseModel):
    transaction_id: str
    bank_acc_id: str
    transaction_type: str
    amount: float
    previous_balance: float
    new_balance: float
    timestamp: datetime
