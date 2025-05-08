from abc import ABC, abstractmethod
from src.modules.domain.user.entity import User, Account
from sqlalchemy.orm import Session
from src.entrypoints.api.user.models import UserLoginModel


class UserRepository(ABC):

    @abstractmethod
    def get_user(self, username: str) -> User:...

    @abstractmethod
    def add_user(self, entity: User) : ...

    @abstractmethod
    def add_account(self, entity: Account, new_cust_id: str): ...
