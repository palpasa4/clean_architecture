from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    cust_id: str
    username: str
    password: str
    role : str

@dataclass
class Account:
    bank_acc_id: str
    fullname: str
    address: str
    contact_no: str
    balance: float
