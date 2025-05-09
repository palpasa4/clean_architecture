import time, jwt, bcrypt
from src.modules.infrastructure.persistence.dbschemas.user import UserSchema
from src.modules.infrastructure.persistence.dbschemas.admin import AdminSchema
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.modules.infrastructure.persistence.database import get_db_session


# For successful login
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def check_role(id: str, db: Session = Depends(get_db_session)):
    valid_admin = db.query(AdminSchema).filter(AdminSchema.admin_id == id).first()
    valid_user = db.query(UserSchema).filter(UserSchema.cust_id == id).first()
    return "user" if not valid_admin else "admin"
