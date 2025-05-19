from fastapi import APIRouter, Request, Depends, Query
from fastapi_pagination import Page
from src.entrypoints.api.mappers.admin_mapper import model_to_admin_entity
from src.modules.application.admin.services import AdminService
from src.modules.domain.admin.entity import *
from src.modules.infrastructure.repositories.postgres.admin_repository import *
from src.entrypoints.api.dependencies import *
from src.entrypoints.api.admin.models import *
from src.entrypoints.api.admin.responses import *
from src.modules.infrastructure.auth.auth_handler import sign_jwt
from src.modules.infrastructure.auth.auth_bearer import JWTBearer
from src.core.logging.logconfig import logger


router = APIRouter(prefix="/admin", tags=["admin"])


# create admin
@router.post(
    "/create-admin",
    response_model=AdminResponseModel,
    tags=["create_admin"],
    status_code=200,
)
def create_admin(model: CreateAdminModel, db: AnnotatedDatabaseSession,):

    adminservice = get_admin_service(db)
    admin_entity = model_to_admin_entity(model)
    adminservice.create_admin_handler(admin_entity)
    logger.info(
        f"New admin added to table 'admin_data' with username: {model.username}"
    )
    return AdminResponseModel(
        message=f"Admin with username '{model.username}' created successfully!"
    )


# admin login
@router.post(
    "/login/", response_model=TokenResponseModel, tags=["admin_login"], status_code=200
)
def admin_login(
    model: AdminLoginModel,
    db: AnnotatedDatabaseSession,
    settings: AnnotatedDefaultSettings,
):
    adminservice = get_admin_service(db)
    admin = adminservice.check_valid_admin(model)
    token = sign_jwt(str(admin.admin_id), settings)
    logger.info(f"Admin login successful for username: {model.username}")
    return TokenResponseModel(access_token=token)


@router.get(
    "/view-user-details/",
    response_model= Page[AdminViewDetailsModel],
    tags=["admin_view_details"],
    status_code=200,
)
def view_user_details(
    admin_id: AnnotatedValidAdminID,
    db: AnnotatedDatabaseSession
):
    admin_service = get_admin_service(db)
    logger.info(f"All user details viewed by admin with ID: {admin_id}")
    return admin_service.view_details_by_admin()


@router.get(
    "/view-specific-user-details/",
    response_model= AdminViewDetailsModel,
    tags=["admin_view_details"],
    status_code=200,
)
def view_specific_user_details(
    admin_id: AnnotatedValidAdminID,
    db: AnnotatedDatabaseSession,
    id: str 
):
    admin_service = get_admin_service(db)
    details = admin_service.view_specific_detail_by_admin(id)
    logger.info(
        f"Details of customer with ID: {id} viewed by admin with ID: {admin_id}"
    )
    return details


@router.get(
    "/view-user-transactions/",
    response_model=Page[AdminTransactionDetailsModel],
)
def view_user_transactions(
    admin_id: AnnotatedValidAdminID,
    db: AnnotatedDatabaseSession,
    id: str= Query(default=None)
):
    adminservice = get_admin_service(db)
    if not id:
        logger.info(f"Transactions viewed by admin with ID: {admin_id}")
        return adminservice.view_transactions_by_admin()
    transactions = adminservice.view_specific_transactions_by_admin(id)
    logger.info(
        f"Transactions of Customer with Customer ID {id} viewed by admin with ID {admin_id}"
    )
    return transactions
