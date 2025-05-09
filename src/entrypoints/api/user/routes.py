from fastapi import APIRouter,Request, Depends
from src.entrypoints.api.mappers.user_mapper import model_to_user_entity
from src.entrypoints.api.user.models import *
from src.entrypoints.api.user.responses import *
from src.entrypoints.api.dependencies import get_admin_service, get_user_service,AnnotatedDatabaseSession, AnnotatedDefaultSettings
from src.modules.infrastructure.repositories.postgres.user_repository import UserPostgresRepository
from src.modules.infrastructure.repositories.postgres.admin_repository import AdminPostgresRepository
from src.modules.application.user_services import UserService
from src.modules.application.admin_services import AdminService
from src.modules.infrastructure.auth.auth_bearer import JWTBearer
from src.modules.infrastructure.logging.logconfig import logger
from src.modules.infrastructure.auth.auth_handler import sign_jwt


router = APIRouter(prefix="/users", tags=["user"])


# admin validation and create user
@router.post(
    "/create-user", response_model=UserResponseModel, tags=["create_users"], status_code=200
)
def create_user_resource(
    model: CreateUserModel, db: AnnotatedDatabaseSession, id: str = Depends(JWTBearer())
):
    adminservice= get_admin_service(db)
    adminservice.check_ifadmin(id)

    userservice= get_user_service(db)
    user_entity = model_to_user_entity(model)
    response_entity = userservice.create_user_handler(user_entity)

    logger.info(f"New user added to table 'user_data' with username: {response_entity.username}"f"Bank account created successfully to the table 'bank_acc' for '{model.username}'")
    return UserResponseModel(
        message=f"Bank account has been created successfully for new user with username: '{response_entity.username}'",
        id=response_entity.cust_id,
        password=response_entity.password
    )


# user login
@router.post("/login/", response_model=TokenResponseModel, tags=["user_login"], status_code=200)
async def user_login(
    model: UserLoginModel,
    settings: AnnotatedDefaultSettings,
    db: AnnotatedDatabaseSession,
):
    user_repo = UserPostgresRepository(db)
    userservice= UserService(user_repo)
    user=userservice.check_valid_user(model)
    token = sign_jwt(str(user.cust_id), settings)
    logger.info(f"User login successful for username: {model.username}")
    return TokenResponseModel(access_token=token)


# user: deposit
@router.post("/deposit/", tags=["user_deposit"], status_code=200)
def deposit_amount(
    model: AmountModel, db: AnnotatedDatabaseSession, id: str = Depends(JWTBearer())
):
    user_repo = UserPostgresRepository(db)
    userservice= UserService(user_repo)
    userservice.check_ifuser(id)
    account = userservice.deposit(model, id)
    logger.info(
        f"Amount of {model.amount} deposited to bank account {account.bank_acc_id}"
    )
    return {
        "message": f"Amount of {model.amount} successfully deposited to Bank Account {account.bank_acc_id}",
        "Deposited amount": model.amount,
        "Previous Balance": account.balance - model.amount,
        "New Balance": account.balance,
    }


# user: withdraw
@router.post("/withdraw/")
def withdraw_amount(
    model: AmountModel, db: AnnotatedDatabaseSession, id: str = Depends(JWTBearer())
):
    user_repo = UserPostgresRepository(db)
    userservice= UserService(user_repo)
    userservice.check_ifuser(id)
    account = userservice.withdraw(model, id)
    logger.info(
        f"Amount of {model.amount} withdrawn from bank account {account.bank_acc_id}"
    )
    return {
        "message": f"Amount of {model.amount} successfully withdrawn from Bank Account {account.bank_acc_id}",
        "Deposited amount": model.amount,
        "Previous Balance": account.balance + model.amount,
        "New Balance": account.balance,
    }


# view details
@router.get("/details/")
def view_details(db: AnnotatedDatabaseSession, id: str = Depends(JWTBearer())):
    user_repo = UserPostgresRepository(db)
    userservice= UserService(user_repo)
    userservice.check_ifuser(id)
    details = userservice.user_view_details(id)
    return {"details": details}


# view transactions
@router.get("/transactions/")
def view_transactions(db: AnnotatedDatabaseSession, id: str = Depends(JWTBearer())):
    user_repo = UserPostgresRepository(db)
    userservice= UserService(user_repo)
    userservice.check_ifuser(id)
    transactions = userservice.user_view_transactions(id)
    return {
        "transactions": transactions
    }
