from abc import ABC, abstractmethod
from pydantic import SecretStr
from src.entrypoints.api.admin.models import AdminLoginModel
from src.entrypoints.api.admin.responses import *
from src.modules.domain.admin.entity import *
from sqlalchemy.orm import Session
from src.modules.domain.user.entity import BankAccount
from src.modules.infrastructure.persistence.dbschemas.admin import AdminSchema


class AdminRepository(ABC):

    @abstractmethod
    def create_admin(self, entity: Admin) :...    
    
    @abstractmethod
    def check_duplicate_admin(self, entity:Admin) -> Admin|None:...

    @abstractmethod
    def get_admin_by_username(self, model: AdminLoginModel) -> Admin | None:...

    @abstractmethod 
    def get_admin_by_id(self, id:str)-> Admin|None:...

    @abstractmethod
    def get_bank_acc(self, id: str) -> BankAccount |None:...

    @abstractmethod
    def get_details(self) ->list[AdminViewDetails]| None:...

    @abstractmethod
    def get_specific_user_detail(self, id: str)  -> AdminViewDetails | None:...

    @abstractmethod
    def get_transactions(self) -> list[AdminTransactionDetails]:...

    @abstractmethod
    def get_specific_transactions(self, bank_acc_id: str ) -> list[AdminTransactionDetails] | None:...
