from email.policy import default
from fastapi import APIRouter,Request, Depends, Query
from src.entrypoints.api.mappers.admin_mapper import model_to_admin_entity
from src.modules.application.admin_services import AdminService
from src.modules.domain.admin.entity import *
from src.modules.infrastructure.repositories.postgres.admin_repository import AdminPostgresRepository
from src.entrypoints.api.dependencies import get_admin_service,AnnotatedDatabaseSession, AnnotatedDefaultSettings
from src.entrypoints.api.admin.models import *
from src.entrypoints.api.admin.responses import *
from src.modules.infrastructure.auth.auth_handler import sign_jwt
from src.modules.infrastructure.auth.auth_bearer import JWTBearer
from src.modules.infrastructure.logging.logconfig import logger


router = APIRouter(prefix="/admin", tags=["admin"])


# create admin
@router.post("/create-admin", tags=["create_admin"], status_code=200)
def create_admin(model: CreateAdminModel, db: AnnotatedDatabaseSession):
    adminservice= get_admin_service(db)
    admin_entity = model_to_admin_entity(model)
    adminservice.create_admin_handler(admin_entity)
    logger.info(f"New admin added to table 'admin_data' with username: {model.username}")
    return {"message": f"Admin with username '{model.username}' created successfully!"}


# admin login
@router.post(
    "/login/", response_model=TokenResponseModel, tags=["admin_login"], status_code=200
)
def admin_login(
    model: AdminLoginModel,
    db: AnnotatedDatabaseSession,
    settings: AnnotatedDefaultSettings,
):
    adminservice= get_admin_service(db)
    admin = adminservice.check_valid_admin(model)
    token = sign_jwt(str(admin.admin_id), settings)
    logger.info(f"Admin login successful for username: {model.username}")
    return TokenResponseModel(access_token=token)


# view all or specific user's details
@router.get("/details/", response_model= list[AdminViewDetailsModel] | AdminViewDetailsModel, tags=["admin_view_details"], status_code=200)
def view_details(
    db: AnnotatedDatabaseSession, adminid: str = Depends(JWTBearer()),id: str = Query(default=None)
):
    adminservice= get_admin_service(db)
    adminservice.check_ifadmin(adminid)
    if not id:
        details= adminservice.admin_view_details()
        response = [AdminViewDetailsModel(**vars(detail)) for detail in details]
        logger.info(f"All user details viewed by admin with ID: {adminid}")
        return response
    details = adminservice.admin_view_specific_detail(id)
    response = AdminViewDetailsModel(**vars(details))
    logger.info(f"Details of customer with ID: {id} viewed by admin with ID: {adminid}")
    return response


# view all or specific user's transaction details.
@router.get("/transactions/", response_model= list[AdminTransactionDetailsModel] | AdminTransactionDetailsModel, )
def view_transactions(
    db: AnnotatedDatabaseSession, adminid: str = Depends(JWTBearer()),id: str = Query(default=None)
):
    adminservice= get_admin_service(db)
    adminservice.check_ifadmin(adminid)
    if not id:
        transactions = adminservice.admin_view_transactions()
        response = [AdminTransactionDetailsModel(**vars(transaction)) for transaction in transactions]
        logger.info(f"Transactions viewed by admin with ID: {id}")
        return response
    transactions=adminservice.admin_view_specific_transactions(id)
    if transactions:
        response = [AdminTransactionDetailsModel(**vars(transaction)) for transaction in transactions]
        logger.info(f"Transactions of Customer with Customer ID {id} viewed by admin with ID {adminid}")
        return response
    