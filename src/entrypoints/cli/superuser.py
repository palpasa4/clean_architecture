import uuid
from src.modules.application.admin_services import AdminService
from sqlalchemy.orm import Session
from src.modules.infrastructure.persistence.database import get_db_session
from src.modules.infrastructure.repositories.postgres.admin_repository import AdminPostgresRepository


def create_super_user(db: Session):
    user_repo = AdminPostgresRepository(db)
    user_service = AdminService(user_repo)
    admin_id = f"AD-{str(uuid.uuid4())[:8]}"
    user_service.create_user_handler(admin_id,"admin","adminpw","role")


db = next(get_db_session())
create_super_user(db)
