from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    cust_id: str
    username: str
    password: str
    hashed_pw: str
    role : str
    fullname: str
    address: str
    contact_no: str
    opening_balance: float


@dataclass
class BankAccount:
    bank_acc_id: str
    balance: float
    