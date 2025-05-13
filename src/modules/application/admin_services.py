import uuid
from src.entrypoints.api import admin, user
from src.entrypoints.api.admin.responses import *
from src.modules.domain.admin.repository import AdminRepository
from sqlalchemy.orm import Session
from src.entrypoints.api.admin.models import *
from src.modules.infrastructure.auth.password_utils import hash_password
from src.modules.domain.admin.entity import *
from src.entrypoints.api.admin.exceptions import *
from src.modules.infrastructure.auth.password_utils import check_password
from src.entrypoints.api.dependencies import AnnotatedDatabaseSession
from src.modules.infrastructure.logging.logconfig import logger
from src.entrypoints.api.user.exceptions import *


class AdminService():


    # dependency injection
    def __init__(self, admin_repository: AdminRepository) -> None:
        self.admin_repository = admin_repository


    def create_admin_handler(self, admin_entity: Admin) -> None:
        try:
            admin=self.admin_repository.check_duplicate_admin(admin_entity) 
            if admin:
                logger.error(f"Duplicate admin creation attempt: username='{admin_entity.username}'")
                raise DuplicateAdminException(
                message=f"Admin with username '{admin_entity.username}' already exists.", status_code=409
            )
            self.admin_repository.create_admin(admin_entity) 
        except Exception as e:
            logger.error(f"Admin creation failed for username='{admin_entity.username}': {str(e)}")
            raise AdminDatabaseOperationError(message="Unable to create admin.", status_code=500)


    def check_valid_admin(self, model: AdminLoginModel) -> Admin:
            try:
                admin = self.admin_repository.get_admin_by_username(model)
                if not admin or not check_password(
                    model.password.get_secret_value(), str(admin.password)
                ):  
                    logger.warning(f"Invalid admin login attempt: username='{model.username}'")
                    raise InvalidAdminLoginException(
                        message=f"Login Failed: Invalid username or password.", status_code=401
                    )
                return admin
            except Exception as e:
                logger.error(f"Database error while validating admin '{model.username}': {str(e)}")
                raise AdminDatabaseOperationError(message="Error while validating admin!", status_code=500)


    def check_ifadmin(self, id: str) -> None:
        try:
            if not self.admin_repository.get_admin_by_id(id):
                logger.error(f"Unauthorized access attempt by user with userid: {id}")
                raise UserPermissionDeniedException(
                    message="User not allowed.", status_code=401
                ) 
        except Exception as e:
            logger.error(f"Database error while checking admin for userid='{id}': {str(e)}")
            raise AdminDatabaseOperationError(message="Error while checking admin status.", status_code=500)


    def view_details_by_admin(self) -> list[AdminViewDetails]:
        try:
            users_list = self.admin_repository.get_details()
            if not users_list:
                logger.error("Database Exception: No details found!")
                raise DetailNotFoundException(message="No details found!", status_code=404)
            return users_list
        except Exception as e:
            logger.error(f"[Admin Access] Database error while retrieving user details: {str(e)}")
            raise AdminDatabaseOperationError(message="Database error while retrieving user details.", status_code=500)


    def view_specific_detail_by_admin(self, id: str) -> AdminViewDetails:
        try:
            users_detail = self.admin_repository.get_specific_user_detail(id)
            if not users_detail:
                logger.error("Database Exception: No details found!")
                raise DetailNotFoundException(message="No details found!", status_code=404)
            return users_detail
        except Exception as e:
            logger.error(f"[Admin Access] Database error while retrieving user details for id='{id}': {str(e)}")
            raise AdminDatabaseOperationError(message="Database error while retrieving user details.", status_code=500)


    def view_transactions_by_admin(self) -> list[AdminTransactionDetails]:
        try:
            transaction_list = self.admin_repository.get_transactions()
            if not transaction_list:
                logger.error("Database Error: No transactions found. ")
                raise TransactionsNotFoundException(
                    message="No transactions found!", status_code=404
                )
            return transaction_list
        except Exception as e:
            logger.error(f"[Admin Access] Database error while retrieving transaction details: {str(e)}")
            raise AdminDatabaseOperationError(message="Database error while retrieving transaction details.", status_code=500)


    def view_specific_transactions_by_admin(self, id: str)-> list[AdminTransactionDetails] | None:
        try:
            transactions = self.admin_repository.get_specific_transactions(id)
            if not transactions:
                logger.error(
                    f"DatabaseException: No transactions found for user with ID: {id}."
                )
                raise TransactionsNotFoundException(
                    message="No transactions found.", status_code=404
                )
            return transactions
        except Exception as e:
            logger.error(f"[Admin Access] Database error while retrieving transaction details for user  {id}: {str(e)}")
            raise AdminDatabaseOperationError(message="Database error while retrieving transaction details.", status_code=500)
        