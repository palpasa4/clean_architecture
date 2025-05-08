from abc import ABC, abstractmethod
from sqlite3 import Row
from typing import Optional
from src.entrypoints.api.user.responses import UserTransactionDetails, UserViewDetails
from src.modules.domain.user.entity import User, Account
from sqlalchemy.orm import Session
from src.entrypoints.api.user.models import Amount, UserLoginModel
from src.modules.infrastructure.persistence.dbschemas.user import BankAccount


class UserRepository(ABC):

    @abstractmethod
    def get_user(self, username: str) -> User:...

    @abstractmethod
    def add_user(self, entity: User) ->None: ...

    @abstractmethod
    def add_account(self, entity: Account, new_cust_id: str)->None: ...

    @abstractmethod 
    def get_user_by_id(self, id:str)-> BankAccount|None:...

    @abstractmethod
    def add_balance(self, model: Amount, id:str)->Account:...

    @abstractmethod
    def get_account(self, id: str) -> BankAccount | None: ...

    @abstractmethod
    def deduct_balance(self, model: Amount, id: str) -> BankAccount:...

    @abstractmethod
    def get_detail(self, id:str)->UserViewDetails|None:...

    @abstractmethod
    def get_transactions(self, id:str)->list|None:...