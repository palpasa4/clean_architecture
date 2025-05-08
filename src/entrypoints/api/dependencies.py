from src.modules.infrastructure.persistence.database import get_db_session
from typing import Annotated
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from src.modules.infrastructure.persistence.settings import DefaultSettings


def get_default_settings(request: Request) -> DefaultSettings:
    return request.app.state.settings.default


AnnotatedDatabaseSession = Annotated[Session, Depends(get_db_session)]

AnnotatedDefaultSettings = Annotated[DefaultSettings, Depends(get_default_settings)]
