from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    cust_id: str
    username: str
    password: str
    hashed_pw: str
    role: str
    fullname: str
    address: str
    contact_no: str
    opening_balance: float


@dataclass
class BankAccount:
    bank_acc_id: str
    balance: float


@dataclass
class Transactions:
    cust_id: str
    amount: float


# @dataclass
# class UserViewDetails:
#     cust_id: str
#     username: str
#     bank_acc_id: str
#     fullname: str
#     address: str
#     contact_no: str
#     balance: float
#     updated_at: datetime


# @dataclass
# class UserTransactionDetails:
#     transaction_id: str
#     bank_acc_id: str
#     transaction_type: str
#     amount: float
#     previous_balance: float
#     new_balance: float
#     timestamp: datetime
