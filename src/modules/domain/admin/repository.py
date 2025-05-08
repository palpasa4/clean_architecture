from abc import ABC, abstractmethod
from pydantic import SecretStr
from src.entrypoints.api.admin.models import AdminLoginModel
from src.modules.domain.admin.entity import Admin
from sqlalchemy.orm import Session


class AdminRepository(ABC):

    @abstractmethod
    def create_admin(self, entity: Admin):...    
    
    @abstractmethod
    def check_duplicate_admin(self, entity:Admin) -> Admin|None:...

    @abstractmethod
    def get_admin_by_username(self, model: AdminLoginModel) -> Admin: ...

    @abstractmethod 
    def get_admin_by_id(self, id:str)-> bool:...
