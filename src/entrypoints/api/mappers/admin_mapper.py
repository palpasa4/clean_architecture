import uuid
from src.entrypoints.api.admin.models import *
from src.modules.domain.admin.entity import *
from src.modules.infrastructure.auth.helpers import hash_password
from src.modules.infrastructure.persistence.dbschemas.admin import AdminSchema


def model_to_admin_entity(model: CreateAdminModel) -> Admin:
    return Admin(
        admin_id=f"ADMIN-{str(uuid.uuid4())[:8]}",
        username=model.username,
        password=hash_password(model.password),
        fullname=model.fullname,
        email=model.email,
        role="admin",
    )


def orm_to_admin_entity(data: dict) -> Admin:
    return Admin(
        admin_id=data["admin_id"],
        username=data["username"],
        password=data["password"],
        fullname=data["fullname"],
        email=data["email"],
        role=data["role"],
    )
