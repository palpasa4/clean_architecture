import bcrypt
from fastapi import Depends
from sqlalchemy.orm import Session
from src.modules.infrastructure.persistence.database import get_db_session
from src.modules.infrastructure.persistence.dbschemas.admin import *
from src.modules.infrastructure.persistence.dbschemas.user import *


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())



