from sqlalchemy import select
from src.entrypoints.api.admin.responses import *
from src.modules.domain.admin.repository import AdminRepository
from sqlalchemy.orm import Session
from src.modules.infrastructure.persistence.dbschemas.admin import AdminSchema
from src.modules.domain.admin.entity import Admin
from src.entrypoints.api.admin.models import AdminLoginModel
from src.modules.infrastructure.persistence.dbschemas.user import *


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
        if valid_admin:
            return valid_admin


    def get_details(self) -> list | None:
        details = self._session.execute(
            select(
                UserSchema.cust_id,
                UserSchema.username,
                BankAccount.bank_acc_id,
                BankAccount.fullname,
                BankAccount.address,
                BankAccount.contact_no,
                BankAccount.created_at,
                BankAccount.updated_at,
            ).outerjoin(BankAccount, UserSchema.cust_id == BankAccount.cust_id)
        ).fetchall()
        users_list = [AdminViewDetails(**dict(detail._mapping)) for detail in details]
        return users_list
    

    def get_specific_user_detail(self, id: str) -> AdminViewDetails | None:
        details = self._session.execute(
            select(
                UserSchema.cust_id,
                UserSchema.username,
                BankAccount.bank_acc_id,
                BankAccount.fullname,
                BankAccount.address,
                BankAccount.contact_no,
                BankAccount.created_at,
                BankAccount.updated_at,
            )
            .outerjoin(BankAccount, UserSchema.cust_id == BankAccount.cust_id)
            .where(UserSchema.cust_id == id)
        ).first()
        if details:
            return AdminViewDetails(**dict(details._mapping))


    def get_transactions(self, id:str) -> list[AdminTransactionDetails]:
        transactions = (
            self._session.execute(
                select(
                    Transactions.transaction_id,
                    Transactions.bank_acc_id,
                    Transactions.transaction_type,
                    Transactions.amount,
                    Transactions.timestamp,
                )
            )
            .mappings()
            .all()
        )
        transaction_list = [
            AdminTransactionDetails(**transaction) for transaction in transactions
        ]
        return transaction_list