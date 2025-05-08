import uuid
from src.entrypoints.api import admin, user
from src.entrypoints.api.admin.responses import AdminViewDetails
from src.modules.domain.admin.repository import AdminRepository
from sqlalchemy.orm import Session
from src.entrypoints.api.admin.models import *
from src.modules.infrastructure.auth.password_utils import hash_password
from src.modules.domain.admin.entity import Admin
from src.entrypoints.api.admin.exceptions import *
from src.modules.infrastructure.auth.password_utils import check_password
from src.entrypoints.api.dependencies import AnnotatedDatabaseSession
from src.modules.infrastructure.logging.logconfig import logger
from src.entrypoints.api.user.exceptions import *


class AdminService():


    # dependency injection
    def __init__(self, admin_repository: AdminRepository) -> None:
        self.admin_repository = admin_repository


    def create_admin_handler(self, username: str, password: str):
        admin_id = f"ADMIN-{str(uuid.uuid4())[:8]}"
        hashed_pw = hash_password(password)
        #depends on a domain entity: Admin
        admin_entity = Admin(
            admin_id=admin_id,
            username=username,
            password=hashed_pw,
            role="admin"
            )
        admin=self.admin_repository.check_duplicate_admin(admin_entity) 
        if admin:
            logger.error(f"Duplicate admin creation attempt: username='{username}'")
            raise DuplicateAdminException(
            message=f"Admin with username '{admin_entity.username}' already exists.", status_code=409
        )
        self.admin_repository.create_admin(admin_entity)


    def check_valid_admin(self, model: AdminLoginModel):
            admin = self.admin_repository.get_admin_by_username(model)
            if admin is None or not check_password(
                model.password.get_secret_value(), str(admin.password)
            ):  
                logger.warning(f"Invalid admin login attempt: username='{model.username}'")
                raise InvalidAdminLoginException(
                    message=f"Login Failed: Invalid username or password.", status_code=401
                )
            return admin


    def check_ifadmin(self, id: str) -> None:
        if not self.admin_repository.get_admin_by_id(id):
            logger.error(f"Unauthorized access attempt by user with userid: {id}")
            raise UserPermissionDeniedException(
                message="User not allowed.", status_code=401
            ) 


    def admin_view_details(self, id:str) -> list[AdminViewDetails]:
        users_list = self.admin_repository.get_details()
        if not users_list:
            logger.error("Database Exception: No details found!")
            raise DetailNotFoundException(message="No details found!", status_code=404)
        return users_list


    def admin_view_specific_detail(self, id: str) -> AdminViewDetails:
        users_detail = self.admin_repository.get_specific_user_detail(id)
        if not users_detail:
            logger.error("Database Exception: No details found!")
            raise DetailNotFoundException(message="No details found!", status_code=404)
        return users_detail
    

    def admin_view_transactions(self, id:str):
        transaction_list = self.admin_repository.get_transactions(id)
        if not transaction_list:
            logger.error("Database Error: No transactions found. ")
            raise TransactionsNotFoundException(
                message="No transactions found!", status_code=404
            )
        return transaction_list