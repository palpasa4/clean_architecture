from src.modules.infrastructure.auth.auth_bearer import JWTBearer
from src.config.database import get_db_session
from typing import Annotated
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from src.modules.infrastructure.persistence.dbschemas.admin import AdminSchema
from src.config.settings import DefaultSettings
from src.modules.infrastructure.repositories.postgres.admin_repository import (
    AdminPostgresRepository,
)
from src.modules.infrastructure.repositories.postgres.user_repository import (
    UserPostgresRepository,
)


def get_default_settings(request: Request) -> DefaultSettings:
    return request.app.state.settings.default


def get_admin_service(db: Session):
    from src.modules.application.admin.services import AdminService

    repo = AdminPostgresRepository(db)
    return AdminService(repo)


def get_user_service(db: Session):
    from src.modules.application.user.services import UserService

    repo = UserPostgresRepository(db)
    return UserService(repo)


def get_current_admin_id(admin_id: str = Depends(JWTBearer())) -> str:
    return admin_id


def get_valid_admin_id(
    admin_id: str = Depends(get_current_admin_id), db: Session = Depends(get_db_session)
) -> str | None:
    admin_service = get_admin_service(db)
    if admin_service.check_ifadmin(admin_id):
        return admin_id


def get_current_user_id(user_id: str = Depends(JWTBearer())) -> str:
    return user_id


def get_valid_user_id(
    user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db_session)
) -> str | None:
    user_service = get_user_service(db)
    if user_service.check_ifuser(user_id):
        return user_id


AnnotatedDatabaseSession = Annotated[Session, Depends(get_db_session)]

AnnotatedDefaultSettings = Annotated[DefaultSettings, Depends(get_default_settings)]

AnnotatedValidAdminID = Annotated[str, Depends(get_valid_admin_id)]

AnnotatedValidUserID = Annotated[str, Depends(get_valid_user_id)]
