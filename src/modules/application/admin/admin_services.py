import uuid
from src.entrypoints.api import admin, user
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


    def check_ifadmin(self, id: str):
        if not self.admin_repository.get_admin_by_id(id):
            logger.error(f"Unauthorized access attempt by user with userid: {id}")
            raise UserPermissionDeniedException(
                message="User not allowed.", status_code=401
            ) 
