from fastapi import APIRouter,Request, Depends
from src.entrypoints.api.user.models import *
from src.entrypoints.api.user.responses import *
from src.entrypoints.api.dependencies import AnnotatedDatabaseSession, AnnotatedDefaultSettings
from src.modules.infrastructure.repositories.postgres.user_repository import UserPostgresRepository
from src.modules.infrastructure.repositories.postgres.admin_repository import AdminPostgresRepository
from src.modules.application.user.user_services import UserService
from src.modules.application.admin.admin_services import AdminService
from src.modules.infrastructure.auth.auth_bearer import JWTBearer
from src.modules.infrastructure.logging.logconfig import logger
from src.modules.infrastructure.auth.auth_handler import sign_jwt


router = APIRouter(prefix="/users", tags=["user"])


# admin validation and create user
@router.post(
    "/create-user", response_model=UserResponse, tags=["create_users"], status_code=200
)
def create_user_resource(
    model: CreateUserModel, db: AnnotatedDatabaseSession, id: str = Depends(JWTBearer())
):
    admin_repo = AdminPostgresRepository(db)
    adminservice= AdminService(admin_repo)
    adminservice.check_ifadmin(id)

    user_repo = UserPostgresRepository(db)
    userservice= UserService(user_repo)
    userservice.check_duplicate_user(model.username)
    userservice.check_user_details(model)
    user_info = userservice.create_user_handler(model)

    logger.info(f"New user added to table 'user_data' with username: {model.username}"f"Bank account created successfully to the table 'bank_acc' for '{model.username}'")
    return UserResponse(
        message=f"Bank account has been created successfully for new user with username: '{model.username}'",
        id=user_info[0],
        password=user_info[1]
    )


# user login
@router.post("/login/", tags=["user_login"], status_code=200)
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
    return {"access_token":token}
