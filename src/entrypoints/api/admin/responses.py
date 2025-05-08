from datetime import datetime
from email import message
from pydantic import BaseModel, SecretStr


class TokenResponse(BaseModel):
    access_token: str


class AdminViewDetails(BaseModel):
    cust_id: str
    username: str
    fullname: str
    address: str
    contact_no: str
    created_at: datetime
    updated_at: datetime


class AdminTransactionDetails(BaseModel):
    transaction_id: str
    bank_acc_id: str
    transaction_type: str
    amount: float
    timestamp: datetime
