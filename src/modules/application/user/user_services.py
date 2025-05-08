import hashlib, uuid
from src.entrypoints.api.user.models import CreateUserModel
from src.modules.domain.user.entity import Account, User
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


    def check_duplicate_user(self, username:str):
        user = self.user_repository.get_user(username)
        if user:
            logger.error("Admin attempted to create a user with an existing username")
            raise DuplicateUserException(
                message=f"User with username {username} already exists.", status_code=409
            )


    def check_user_details(self, model: CreateUserModel):
        if len(model.username) < 7:
            # simple input validation issue
            logger.warning("Username too short: must be at least 7 characters long")
            raise ValidationException(
                message="Username must be at least 7 characters long!", status_code=400
            )
        if len(model.username) > 20:
            logger.warning("Username too long: cannot be more than 20 characters!")
            raise ValidationException(
                message="Username cannot include more than 20 characters!", status_code=400
            )
        if model.opening_balance < 500:
            # business rule violation
            logger.error(
                "Bank account creation failed: opening balance below minimum requirement"
            )
            raise ValidationException(
                message="Minimum opening balance is 500!", status_code=400
            )


    def create_user_handler(self, model: CreateUserModel) -> list:
        try:
            new_cust_id = f"CUST-{str(uuid.uuid4())[:8]}"
            password = hashlib.sha256(model.username.encode()).hexdigest()[:12]
            hashed_pw = hash_password(password)
            user_entity = User(
                cust_id=new_cust_id,
                username=model.username,
                password=hashed_pw,
                role="user"
            )
            self.user_repository.add_user(user_entity)
            self.create_bank_acc(model, new_cust_id)
            return [new_cust_id, password]
        except Exception as e:
            logger.error(
                f"Database error: Unable to add user '{model.username}' to table 'user_data'.Error: {str(e)}"
            )
            raise DatabaseException("Database error: Unable to add user.", status_code=500)


    def create_bank_acc(self, model: CreateUserModel, new_cust_id: str):
        try:
            new_bankid = f"ACC-{str(uuid.uuid4())[:8]}"
            account_entity=Account(
                bank_acc_id= new_bankid,
                fullname= model.fullname,
                address= model.address,
                contact_no= model.contact_no,
                balance=model.opening_balance
            )
            self.user_repository.add_account(account_entity, new_cust_id)
        except Exception as e:
            logger.error(
                f"Database error: Unable to create bank_acc for '{model.username}'.Error: {str(e)}"
            )
            raise DatabaseException(
                "Database error: Unable to create bank account.", status_code=500
            )
    

    def check_valid_user(self, model: UserLoginModel): 
        user = self.user_repository.get_user(model.username)
        if user is None or not check_password(
            model.password.get_secret_value(), str(user.password)
        ):
            logger.warning(f"Invalid user login attempt: username='{model.username}'")
            raise InvalidUserLoginException(
                message=f"Login Failed: Invalid username or password.", status_code=401
            )
        return user
    