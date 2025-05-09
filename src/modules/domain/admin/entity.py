from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class Admin:
    admin_id: str
    username: str
    password: str
    fullname: str
    email: str
    role : str 


@dataclass
class AdminViewDetails:
    cust_id: str
    username: str
    bank_acc_id: str
    fullname: str
    address: str
    contact_no: str
    created_at: datetime
    updated_at: datetime
    

@dataclass
class AdminTransactionDetails:
    transaction_id: str
    bank_acc_id: str
    transaction_type: str
    amount: float
    timestamp: datetime
    