from sqlalchemy import select
from src.entrypoints.api.admin.responses import *
from src.entrypoints.api.mappers.admin_mapper import orm_to_admin_entity
from src.entrypoints.api.mappers.user_mapper import orm_to_bankaccount_entity
from src.modules.domain.admin.repository import AdminRepository
from sqlalchemy.orm import Session
from src.modules.domain.user.entity import BankAccount
from src.modules.infrastructure.persistence.dbschemas.admin import AdminSchema
from src.modules.domain.admin.entity import *
from src.entrypoints.api.admin.models import AdminLoginModel
from src.modules.infrastructure.persistence.dbschemas.user import *


class AdminPostgresRepository(AdminRepository):

    def __init__(self, db : Session):
        self._session = db


    def create_admin(self, entity: Admin):
        user= AdminSchema(admin_id=entity.admin_id, username=entity.username, password=entity.password, fullname=entity.fullname, email=entity.email ,role=entity.role)
        self._session.add(user)
        self._session.commit()


    def check_duplicate_admin(self, entity: Admin) -> Admin | None:
        admin = self._session.query(AdminSchema).filter(AdminSchema.username== entity.username).first()
        if admin: 
            admin_entity= orm_to_admin_entity(admin.__dict__)
            return admin_entity


    def get_admin_by_username(self, model: AdminLoginModel) -> Admin | None: 
        admin = self._session.query(AdminSchema).filter_by(username=model.username).first()
        if admin: 
            admin_entity= orm_to_admin_entity(admin.__dict__)
            return admin_entity


    def get_admin_by_id(self, id: str) -> Admin | None:
        valid_admin = self._session.query(AdminSchema).filter(AdminSchema.admin_id == id).first()
        if valid_admin:
            admin_entity= orm_to_admin_entity(valid_admin.__dict__)
            return admin_entity


    def get_bank_acc(self, cust_id: str) -> BankAccount | None:
        account = self._session.query(BankAccountSchema).filter(BankAccountSchema.cust_id == cust_id).first()
        breakpoint()
        if account:
            account_entity = orm_to_bankaccount_entity(account)
            return account_entity
        
        
    def get_details(self) -> list[AdminViewDetails] | None:
        details = self._session.execute(
            select(
                UserSchema.cust_id,
                UserSchema.username,
                BankAccountSchema.bank_acc_id,
                BankAccountSchema.fullname,
                BankAccountSchema.address,
                BankAccountSchema.contact_no,
                BankAccountSchema.created_at,
                BankAccountSchema.updated_at,
            ).outerjoin(BankAccountSchema, UserSchema.cust_id == BankAccountSchema.cust_id)
        ).fetchall()
        users_list = [AdminViewDetails(**dict(detail._mapping)) for detail in details]
        return users_list
    

    def get_specific_user_detail(self, id: str) -> AdminViewDetails | None:
        details = self._session.execute(
            select(
                UserSchema.cust_id,
                UserSchema.username,
                BankAccountSchema.bank_acc_id,
                BankAccountSchema.fullname,
                BankAccountSchema.address,
                BankAccountSchema.contact_no,
                BankAccountSchema.created_at,
                BankAccountSchema.updated_at,
            )
            .outerjoin(BankAccountSchema, UserSchema.cust_id == BankAccountSchema.cust_id)
            .where(UserSchema.cust_id == id)
        ).first()
        if details:
            return AdminViewDetails(**dict(details._mapping))


    def get_transactions(self) -> list[AdminTransactionDetails]:
        transactions = (
            self._session.execute(
                select(
                    TransactionsSchema.transaction_id,
                    TransactionsSchema.bank_acc_id,
                    TransactionsSchema.transaction_type,
                    TransactionsSchema.amount,
                    TransactionsSchema.timestamp,
                )
            )
            .mappings()
            .all()
        )
        transaction_list = [
            AdminTransactionDetails(**transaction) for transaction in transactions
        ]
        return transaction_list
    

    def get_specific_transactions(self, id: str) -> list[AdminTransactionDetails] | None:
        bank_acc_id = self._session.execute(
            select(BankAccountSchema.bank_acc_id).where(BankAccountSchema.cust_id == id)
        ).scalar()
        stmt = select(
            TransactionsSchema.transaction_id,
            TransactionsSchema.bank_acc_id,
            TransactionsSchema.transaction_type,
            TransactionsSchema.amount,
            TransactionsSchema.timestamp,
        ).where(TransactionsSchema.bank_acc_id == bank_acc_id)
        transactions = (
            self._session.execute(stmt)
            .mappings()
            .all()
        )
        if transactions:
            transaction_list = [
                AdminTransactionDetails(**transaction) for transaction in transactions
            ]
            return transaction_list
        