from src.modules.infrastructure.persistence.database import get_db_session
from typing import Annotated
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from src.modules.infrastructure.persistence.settings import DefaultSettings
from src.modules.infrastructure.repositories.postgres.admin_repository import AdminPostgresRepository
from src.modules.infrastructure.repositories.postgres.user_repository import UserPostgresRepository


def get_default_settings(request: Request) -> DefaultSettings:
    return request.app.state.settings.default


def get_admin_service(db : Session) :
    from src.modules.application.admin_services import AdminService
    repo = AdminPostgresRepository(db)
    return AdminService(repo)


def get_user_service(db : Session):
    from src.modules.application.user_services import UserService 
    repo = UserPostgresRepository(db)
    return UserService(repo)


AnnotatedDatabaseSession = Annotated[Session, Depends(get_db_session)]

AnnotatedDefaultSettings = Annotated[DefaultSettings, Depends(get_default_settings)]
