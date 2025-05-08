from pydantic import BaseModel,SecretStr
from datetime import datetime


class UserResponse(BaseModel):
    message: str
    id: str
    password: str


class UserViewDetails(BaseModel):
    cust_id: str
    username: str
    bank_acc_id: str
    fullname: str
    address: str
    contact_no: str
    balance: float
    updated_at: datetime


class UserTransactionDetails(BaseModel):
    transaction_id: str
    bank_acc_id: str
    transaction_type: str
    amount: float
    previous_balance: float
    new_balance: float
    timestamp: datetime
