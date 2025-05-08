from src.modules.domain.admin.repository import AdminRepository
from sqlalchemy.orm import Session
from src.modules.infrastructure.persistence.dbschemas.admin import AdminSchema
from src.modules.domain.admin.entity import Admin
from src.entrypoints.api.admin.models import AdminLoginModel


class AdminPostgresRepository(AdminRepository):

    def __init__(self, db : Session):
        self._session = db


    def create_admin(self, entity: Admin):
        user= AdminSchema(admin_id=entity.admin_id, username=entity.username, password=entity.password, role=entity.role)
        self._session.add(user)
        self._session.commit()


    def check_duplicate_admin(self, entity: Admin) -> Admin | None:
        admin = self._session.query(AdminSchema).filter(AdminSchema.username== entity.username).first()
        if admin: 
            return admin


    def get_admin_by_username(self, model: AdminLoginModel) -> Admin: 
        admin = self._session.query(AdminSchema).filter_by(username=model.username).first()
        return admin


    def get_admin_by_id(self, id: str) -> AdminSchema | None:
        valid_admin = self._session.query(AdminSchema).filter(AdminSchema.admin_id == id).first()
        return None if not valid_admin else valid_admin
