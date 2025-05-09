from sqlite3 import Row
from typing import Optional
from src.entrypoints.api.mappers.user_mapper import *
from src.entrypoints.api.user.models import *
from src.entrypoints.api.user.responses import *
from src.modules.domain.user.repository import UserRepository
from src.modules.infrastructure.persistence.dbschemas.user import *
from sqlalchemy.orm import Session
from src.modules.domain.user.entity import *
from datetime import datetime
from sqlalchemy import select


class UserPostgresRepository(UserRepository):

    def __init__(self, db : Session):
        self._session = db


    def get_user(self, username: str) -> User | None: 
        user = self._session.query(UserSchema).filter_by(username=username).first()
        return user


    def add_user(self, entity: User):
        db_user = UserSchema(
            cust_id=entity.cust_id, username=entity.username, password=entity.hashed_pw, role=entity.role
        )
        self._session.add(db_user)
        self._session.commit()


    def add_account(self, user_entity: User, account_entity: BankAccount):
        db_acc= BankAccountSchema(
            bank_acc_id=account_entity.bank_acc_id,
            fullname=user_entity.fullname,
            address=user_entity.address,
            contact_no=user_entity.contact_no,
            balance=account_entity.balance,
            cust_id = user_entity.cust_id
        )
        self._session.add(db_acc)
        self._session.commit()


    def get_user_by_id(self, id: str)->BankAccountSchema|None:
        valid_user = self._session.query(UserSchema).filter(UserSchema.cust_id == id).first()
        if valid_user:
            return BankAccountSchema


    def add_balance(self, model: AmountModel, id:str)->BankAccount:
        account = self._session.query(BankAccountSchema).filter(BankAccountSchema.cust_id == id).first()
        if account:
            account.balance += model.amount #type:ignore
            account.updated_at = datetime.now()  #type:ignore
            self._session.commit()
        return account
    

    def get_account(self, id: str) -> BankAccountSchema | None:
        bank_acc = self._session.query(BankAccountSchema).filter(BankAccountSchema.cust_id == id).first()
        return bank_acc if bank_acc is not None else  None
    

    def deduct_balance(self, model: AmountModel, id: str) -> BankAccountSchema:
        account = self._session.query(BankAccountSchema).filter(BankAccountSchema.cust_id == id).first()
        if account:
            account.balance -= model.amount #type:ignore
            account.updated_at = datetime.now() #type: ignore
            self._session.commit()
        return account


    def get_detail(self, id:str)-> UserViewDetailsModel | None:
        user_details = self._session.execute(
            select(
                UserSchema.cust_id,
                UserSchema.username,
                BankAccountSchema.bank_acc_id,
                BankAccountSchema.fullname,
                BankAccountSchema.address,
                BankAccountSchema.contact_no,
                BankAccountSchema.balance,
                BankAccountSchema.updated_at,
            )
            .outerjoin(BankAccountSchema, UserSchema.cust_id == BankAccountSchema.cust_id)
            .where(UserSchema.cust_id == id)
        ).mappings().fetchone() 
        return UserViewDetailsModel(**user_details) if user_details else None
    

    def get_transactions(self, id:str)->list|None:
        bank_acc_id = self._session.execute(
            select(BankAccountSchema.bank_acc_id).where(BankAccountSchema.cust_id == id)
        ).scalar()
        transactions = self._session.execute(
            select(TransactionsSchema).where(TransactionsSchema.bank_acc_id == bank_acc_id)
        ).fetchall()
        transactions= [
            UserTransactionDetailsModel(**transaction[0].__dict__)
            for transaction in transactions
        ]
        return transactions
