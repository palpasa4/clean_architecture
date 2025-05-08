from fastapi import APIRouter,Request, Depends
from src.modules.application.admin.admin_services import AdminService
from src.modules.infrastructure.repositories.postgres.admin_repository import AdminPostgresRepository
from src.entrypoints.api.dependencies import AnnotatedDatabaseSession, AnnotatedDefaultSettings
from src.entrypoints.api.admin.models import *
from src.entrypoints.api.admin.responses import *
from src.modules.infrastructure.auth.auth_handler import sign_jwt
from src.modules.infrastructure.auth.auth_bearer import JWTBearer
from src.modules.infrastructure.logging.logconfig import logger


router = APIRouter(prefix="/admin", tags=["admin"])


# create admin
@router.post("/create-admin")
def create_admin(model: CreateAdminModel, db: AnnotatedDatabaseSession):
    repo = AdminPostgresRepository(db)
    userservice= AdminService(repo)
    userservice.create_admin_handler(model.username, model.password)
    logger.info(f"New admin added to table 'admin_data' with username: {model.username}")
    return {"message": "Admin created successfully!"}


# admin login
@router.post(
    "/login/", response_model=TokenResponse, tags=["admin_login"], status_code=200
)
async def admin_login(
    model: AdminLoginModel,
    db: AnnotatedDatabaseSession,
    settings: AnnotatedDefaultSettings,
):
    repo = AdminPostgresRepository(db)
    adminservice= AdminService(repo)
    admin = adminservice.check_valid_admin(model)
    token = sign_jwt(str(admin.admin_id), settings)
    logger.info(f"Admin login successful for username: {model.username}")
    return TokenResponse(access_token=token)
