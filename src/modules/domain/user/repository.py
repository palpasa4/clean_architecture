from abc import ABC, abstractmethod
from src.entrypoints.api.user.models import *
from src.entrypoints.api.user.responses import *
from src.modules.domain.user.entity import (
    BankAccount,
    Transactions,
    User,
    BankAccount,
    UserTransactionDetails,
    UserViewDetails,
)
from sqlalchemy.orm import Session
from src.modules.infrastructure.persistence.dbschemas.user import BankAccountSchema


class UserRepository(ABC):

    @abstractmethod
    def get_user_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    def add_user(self, entity: User) -> None: ...

    @abstractmethod
    def add_account(self, user_entity: User, account_entity: BankAccount) -> None: ...

    @abstractmethod
    def get_user_by_id(self, id: str) -> User | None: ...

    @abstractmethod
    def add_balance(self, entity: Transactions) -> BankAccount | None: ...

    @abstractmethod
    def get_account(self, id: str) -> BankAccount | None: ...

    @abstractmethod
    def deduct_balance(self, entity: Transactions) -> BankAccount | None: ...

    @abstractmethod
    def get_detail(self, id: str) -> UserViewDetails | None: ...

    @abstractmethod
    def get_transactions(self, id: str) -> list[UserTransactionDetails] | None: ...
