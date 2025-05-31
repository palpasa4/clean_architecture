import uuid
from fastapi_pagination import Page, paginate
from src.entrypoints.api import admin, user
from src.entrypoints.api.admin.responses import *
from src.modules.domain.admin.repository import AdminRepository
from sqlalchemy.orm import Session
from src.entrypoints.api.admin.models import *
from src.core.auth.helpers import hash_password, check_password
from src.modules.domain.admin.entity import *
from src.modules.domain.admin.exceptions import *
from src.entrypoints.api.dependencies import AnnotatedDatabaseSession
from src.core.logging.logconfig import logger
from src.modules.domain.user.exceptions import *


class AdminService:

    # dependency injection
    def __init__(self, admin_repository: AdminRepository) -> None:
        self.admin_repository = admin_repository

    def create_admin_handler(self, admin_entity: Admin) -> None:
        self.check_admin_username(admin_entity)
        self.check_admin_email(admin_entity)
        try:
            self.admin_repository.create_admin(admin_entity)
        except Exception as e:
            logger.error(
                f"Database Error: Admin creation failed for username='{admin_entity.username}': {str(e)}"
            )
            raise AdminDatabaseOperationError(
                message="Database Error: Unable to create admin.", status_code=500
            )

    def check_admin_username(self, entity: Admin) -> None:
        if len(entity.username) < 7:
            # simple input validation issue
            logger.warning("Username too short: must be at least 7 characters long")
            raise UsernameValidationException(
                message="Username must be at least 7 characters long!", status_code=400
            )
        if len(entity.username) > 20:
            logger.warning("Username too long: cannot be more than 20 characters!")
            raise UsernameValidationException(
                message="Username cannot include more than 20 characters!",
                status_code=400,
            )
        try:
            admin_username = self.admin_repository.check_duplicate_username(entity)
            if admin_username:
                logger.error(
                    f"Duplicate admin creation attempt: username='{entity.username}'"
                )
            raise DuplicateUsernameException(
                message=f"Admin with username '{entity.username}' already exists.",
                status_code=409,
            )
        except DuplicateUsernameException:
            raise
        except Exception as e:
            logger.error(
                f"Database Error: Admin creation failed for username='{entity.username}': {str(e)}"
            )
            raise AdminDatabaseOperationError(
                message="Database Error: Unable to create admin.", status_code=500
            )
    
    def check_admin_email(self, entity: Admin) -> None:
        try:
            admin_email = self.admin_repository.check_duplicate_email(entity)
            if admin_email:
                logger.error(
                    f"Duplicate admin creation attempt with email='{entity.email}'"
                )
                raise DuplicateEmailException(
                    message=f"Admin with email '{entity.email}' already exists.",
                    status_code=409,
                )
        except DuplicateEmailException:
            raise
        except Exception as e:
            logger.error(
                f"Database Error: Admin creation failed for username='{entity.username}': {str(e)}"
            )
            raise AdminDatabaseOperationError(
                message="Database Error: Unable to create admin.", status_code=500
            )

    def check_valid_admin(self, model: AdminLoginModel) -> Admin:
        try:
            admin = self.admin_repository.get_admin_by_username(model)
            if not admin or not check_password(
                model.password.get_secret_value(), str(admin.password)
            ):
                logger.warning(
                    f"Invalid admin login attempt: username='{model.username}'"
                )
                raise InvalidAdminLoginException(
                    message=f"Login Failed: Invalid username or password.",
                    status_code=401,
                )
            return admin
        except InvalidAdminLoginException:
            raise
        except Exception as e:
            logger.error(
                f"Database error while validating admin '{model.username}': {str(e)}"
            )
            raise AdminDatabaseOperationError(
                message="Error while validating admin!", status_code=500
            )

    def check_ifadmin(self, id: str) -> bool:
        try:  # for db error
            admin = self.admin_repository.get_admin_by_id(id)
            if not admin:  # Business logic error
                logger.error(f"Unauthorized access attempt by user with userid: {id}")
                raise UserPermissionDeniedException(
                    message="User not allowed.", status_code=401
                )
            return True
        except UserPermissionDeniedException:
            raise
        except Exception as e:  # db error
            logger.error(f"Database error while fetching admin id={id}: {str(e)}")
            raise AdminDatabaseOperationError(
                message="Database error!", status_code=500
            )


    def view_details_by_admin(self) -> Page[AdminViewDetailsModel]:
        try:
            details =  self.admin_repository.get_details()
            if not details.items:
                logger.error("No details found.")
                raise DetailNotFoundException(message = "No details found.", status_code=404)
            return details
        except DetailNotFoundException:
            raise
        except Exception as e:
            logger.error(
                f"[Admin Access] Database error while retrieving user details: {str(e)}"
            )
            raise AdminDatabaseOperationError(
                message="Database error while retrieving user details.", status_code=500
            )
    

    def view_specific_detail_by_admin(self, id: str) -> AdminViewDetailsModel:
        try:
            users_detail = self.admin_repository.get_specific_user_detail(id)
            if not users_detail:
                logger.error("Database Exception: No details found!")
                raise DetailNotFoundException(
                    message="No details found!", status_code=404
                )
            return users_detail
        except DetailNotFoundException:
            raise
        except Exception as e:
            logger.error(
                f"[Admin Access] Database error while retrieving user details for id='{id}': {str(e)}"
            )
            raise AdminDatabaseOperationError(
                message="Database error while retrieving user details.", status_code=500
            )


    def view_transactions_by_admin(self) -> Page[AdminTransactionDetailsModel]:
        try:
            transactions = self.admin_repository.get_transactions()
            if not transactions.items:
                logger.error("Database Error: No transactions found. ")
                raise TransactionsNotFoundException(
                    message="No transactions found!", status_code=404
                )
            return transactions
        except TransactionsNotFoundException:
            raise
        except Exception as e:
            logger.error(
                f"[Admin Access] Database error while retrieving transaction details: {str(e)}"
            )
            raise AdminDatabaseOperationError(
                message="Database error while retrieving transaction details.",
                status_code=500,
            )

    def view_specific_transactions_by_admin(
        self, id: str
    ) -> Page[AdminTransactionDetailsModel]:
        try:
            transactions = self.admin_repository.get_specific_transactions(id)

            if not transactions.items:
                logger.error(
                    f"DatabaseException: No transactions found for user with ID: {id}."
                )
                raise TransactionsNotFoundException(
                    message="No transactions found.", status_code=404
                )
            return transactions
        except TransactionsNotFoundException:
            raise
        except Exception as e:
            logger.error(
                f"[Admin Access] Database error while retrieving transaction details for user  {id}: {str(e)}"
            )
            raise AdminDatabaseOperationError(
                message="Database error while retrieving transaction details.",
                status_code=500,
            )
