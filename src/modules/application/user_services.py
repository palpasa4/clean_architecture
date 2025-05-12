import hashlib, uuid
from src.entrypoints.api.user.models import *
from src.entrypoints.api.user.responses import *
from src.modules.domain.user.entity import BankAccount, BankAccount, Transactions, User, UserTransactionDetails, UserViewDetails
from src.modules.domain.user.repository import UserRepository
from src.modules.infrastructure.auth.password_utils import hash_password
from src.modules.infrastructure.logging.logconfig import logger
from src.entrypoints.api.user.exceptions import *
from sqlalchemy.orm import Session
from src.entrypoints.api.user.models import *
from src.modules.infrastructure.auth.password_utils import check_password


class UserService():
        
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository


    def check_duplicate_user(self, username:str) -> None:
        user = self.user_repository.get_user_by_username(username)
        if user:
            logger.error(f"Duplicate user creation attempt: username= {user.username}")
            raise DuplicateUserException(
                message=f"User with username {user.username} already exists.", status_code=409
            )


    def check_user_details(self, entity: User) -> None:
        if len(entity.username) < 7:
            # simple input validation issue
            logger.warning("Username too short: must be at least 7 characters long")
            raise ValidationException(
                message="Username must be at least 7 characters long!", status_code=400
            )
        if len(entity.username) > 20:
            logger.warning("Username too long: cannot be more than 20 characters!")
            raise ValidationException(
                message="Username cannot include more than 20 characters!", status_code=400
            )
        if entity.opening_balance < 500:
            # business rule violation
            logger.error(
                "Bank account creation failed: opening balance below minimum requirement"
            )
            raise ValidationException(
                message="Minimum opening balance is 500!", status_code=400
            )


    def create_user_handler(self, user_entity: User) -> User:
        self.check_duplicate_user(user_entity.username)
        self.check_user_details(user_entity)
        try:
            self.user_repository.add_user(user_entity)
            self.create_bank_acc(user_entity)
            return user_entity
        except Exception as e:
            logger.error(
                f"Database error: Unable to add user '{user_entity.username}' to table 'user_data'.Error: {str(e)}"
            )
            raise DatabaseException("Database error: Unable to add user.", status_code=500)


    def create_bank_acc(self, user_entity: User) -> None:
        try:
            account_entity=BankAccount(
                bank_acc_id= f"ACC-{str(uuid.uuid4())[:8]}",
                balance=user_entity.opening_balance
            )
            self.user_repository.add_account(user_entity, account_entity)
        except Exception as e:
            logger.error(
                f"Database error: Unable to create bank_acc for '{user_entity.username}'.Error: {str(e)}"
            )
            raise DatabaseException(
                "Database error: Unable to create bank account.", status_code=500
            )
    

    def check_valid_user(self, model: UserLoginModel) -> User: 
        user = self.user_repository.get_user_by_username(model.username)
        if user is None or not check_password(
            model.password.get_secret_value(), str(user.password)
        ):
            logger.warning(f"Invalid user login attempt: username='{model.username}'")
            raise InvalidUserLoginException(
                message=f"Login Failed: Invalid username or password.", status_code=401
            )
        return user
    

    def check_ifuser(self, id: str) -> None:
        if not self.user_repository.get_user_by_id(id):
            logger.error(f"Unauthorized access attempt by user with userid: {id}")
            raise UserPermissionDeniedException(
                message="User not allowed.", status_code=401
            ) 
        

    def deposit(self, transaction_entity: Transactions) -> BankAccount | None:
        if transaction_entity.amount < 500:
            logger.error(
                "DepositBalanceException: Trying to deposit less than minimum amount!"
            )
            raise ValidationException(
                message="Minimum amount of deposit is 500!", status_code=400
            )
        try:
            account_entity = self.user_repository.add_balance(transaction_entity)
            return account_entity
        except Exception as e:
            logger.error(f"Database error: Unable to deposit amount for user with ID: {transaction_entity.cust_id}")
            raise DatabaseException(
                message="Database error: Unable to deposit money.", status_code=500
            )

    
    def withdraw(self, transaction_entity: Transactions):
        bank_acc= self.user_repository.get_account(transaction_entity.cust_id)
        if transaction_entity.amount < 500:
            logger.error(
                "WithdrawBalanceException: Trying to withdraw less than minimum amount!"
            )
            raise ValidationException(
                message="Minimum amount of withdrawal is 500!", status_code=400
            )
        if (
            bank_acc
            and isinstance(bank_acc.balance, (float))
            and float(bank_acc.balance) - 500 < transaction_entity.amount
        ):
            logger.error(
                "WithdrawBalanceException: Trying to withdraw more than existing balance!"
            )
            raise ValidationException(
                message=f"Withdrawal exceeds existing balance. Minimum existing balance should be NPR 500 Existing balance is : {bank_acc.balance}",
                status_code=400,
            )
        try:
            account_entity = self.user_repository.deduct_balance(transaction_entity)
            return account_entity
        except Exception as e:
            logger.error(
                f"Database error: Unable to withdraw amount for user with ID: {transaction_entity.cust_id}"
            )
            raise DatabaseException(
                message="Database error: Unable to withdraw money.", status_code=500
            )
       

    def user_view_details(self, id) -> UserViewDetails:
        details = self.user_repository.get_detail(id)
        if not details:
            logger.error(
                f"DatabaseException raised: Detail Not Found for user with ID: {id}."
            )
            raise DetailNotFoundException(message="Detail Not found.", status_code=404)
        return details
    

    def user_view_transactions(self, id: str)-> list[UserTransactionDetails]:
        transactions = self.user_repository.get_transactions(id)
        if not transactions:
            logger.error(
                f"DatabaseException: No transactions found for user with ID: {id}."
            )
            raise TransactionsNotFoundException(
                message="No transactions found.", status_code=404
            )
        return transactions
    