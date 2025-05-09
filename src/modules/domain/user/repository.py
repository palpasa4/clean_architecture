from abc import ABC, abstractmethod
from src.entrypoints.api.user.models import *
from src.entrypoints.api.user.responses import *
from src.modules.domain.user.entity import BankAccount, User, BankAccount
from sqlalchemy.orm import Session
from src.modules.infrastructure.persistence.dbschemas.user import BankAccountSchema


class UserRepository(ABC):

    @abstractmethod
    def get_user(self, username: str) -> User | None:...

    @abstractmethod
    def add_user(self, entity: User) ->None: ...

    @abstractmethod
    def add_account(self, user_entity: User, account_entity: BankAccount)->None: ...

    @abstractmethod 
    def get_user_by_id(self, id:str)-> BankAccountSchema|None:...

    @abstractmethod
    def add_balance(self, model: AmountModel, id:str)->BankAccount:...

    @abstractmethod
    def get_account(self, id: str) -> BankAccountSchema | None: ...

    @abstractmethod
    def deduct_balance(self, model: AmountModel, id: str) -> BankAccountSchema:...

    @abstractmethod
    def get_detail(self, id:str)->UserViewDetailsModel|None:...

    @abstractmethod
    def get_transactions(self, id:str)->list|None:...