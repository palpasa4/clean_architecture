from email.policy import default
from fastapi import APIRouter, Request, Depends, Query
from src.entrypoints.api.mappers.admin_mapper import model_to_admin_entity
from src.modules.application.admin_services import AdminService
from src.modules.domain.admin.entity import *
from src.modules.infrastructure.repositories.postgres.admin_repository import *
from src.entrypoints.api.dependencies import *
from src.entrypoints.api.admin.models import *
from src.entrypoints.api.admin.responses import *
from src.modules.infrastructure.auth.auth_handler import sign_jwt
from src.modules.infrastructure.auth.auth_bearer import JWTBearer
from src.modules.infrastructure.logging.logconfig import logger


router = APIRouter(prefix="/admin", tags=["admin"])


# create admin
@router.post(
    "/create-admin",
    response_model=AdminResponseModel,
    tags=["create_admin"],
    status_code=200,
)
def create_admin(model: CreateAdminModel, db: AnnotatedDatabaseSession):
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


# view all or specific user's details
@router.get(
    "/details/",
    response_model=list[AdminViewDetailsModel] | AdminViewDetailsModel,
    tags=["admin_view_details"],
    status_code=200,
)
def view_details(
    admin_id: AnnotatedValidAdminID,  # _:AnnotatedCheckAdmin -> if the parameter is used no where
    db: AnnotatedDatabaseSession,
    id: str = Query(default=None),
):
    admin_service = get_admin_service(db)
    if not id:
        details = admin_service.view_details_by_admin()
        response = [AdminViewDetailsModel(**vars(detail)) for detail in details]
        logger.info(f"All user details viewed by admin with ID: {admin_id}")
        return response
    details = admin_service.view_specific_detail_by_admin(id)
    response = AdminViewDetailsModel(**vars(details))
    logger.info(
        f"Details of customer with ID: {id} viewed by admin with ID: {admin_id}"
    )
    return response


# view all or specific user's transaction details.
@router.get(
    "/transactions/",
    response_model=list[AdminTransactionDetailsModel] | AdminTransactionDetailsModel,
)
def view_transactions(
    admin_id: AnnotatedValidAdminID,
    db: AnnotatedDatabaseSession,
    id: str = Query(default=None),
):
    adminservice = get_admin_service(db)
    adminservice.check_ifadmin(admin_id)
    if not id:
        transactions = adminservice.view_transactions_by_admin()
        response = [
            AdminTransactionDetailsModel(**vars(transaction))
            for transaction in transactions
        ]
        logger.info(f"Transactions viewed by admin with ID: {admin_id}")
        return response
    transactions = adminservice.view_specific_transactions_by_admin(id)
    if transactions:
        response = [
            AdminTransactionDetailsModel(**vars(transaction))
            for transaction in transactions
        ]
        logger.info(
            f"Transactions of Customer with Customer ID {id} viewed by admin with ID {admin_id}"
        )
        return response
