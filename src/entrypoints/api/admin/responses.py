from datetime import datetime
from fastapi_pagination import Page
from pydantic import BaseModel, SecretStr


class AdminResponseModel(BaseModel):
    message: str


class TokenResponseModel(BaseModel):
    access_token: str


class AdminViewDetailsModel(BaseModel):
    cust_id: str
    username: str
    bank_acc_id: str
    fullname: str
    address: str
    contact_no: str
    created_at: datetime
    updated_at: datetime


class AdminTransactionDetailsModel(BaseModel):
    transaction_id: str
    bank_acc_id: str
    transaction_type: str
    amount: float
    timestamp: datetime
