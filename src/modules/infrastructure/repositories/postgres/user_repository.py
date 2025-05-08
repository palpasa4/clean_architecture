from sqlite3 import Row
from typing import Optional
from src.entrypoints.api.user.models import Amount
from src.entrypoints.api.user.responses import *
from src.modules.domain.user.repository import UserRepository
from src.modules.infrastructure.persistence.dbschemas.user import *
from sqlalchemy.orm import Session
from src.modules.domain.user.entity import User, Account
from datetime import datetime
from sqlalchemy import select


class UserPostgresRepository(UserRepository):

    def __init__(self, db : Session):
        self._session = db


    def get_user(self, username: str) -> User: 
        user = self._session.query(UserSchema).filter_by(username=username).first()
        return user


    def add_user(self, entity: User):
        db_user = UserSchema(
            cust_id=entity.cust_id, username=entity.username, password=entity.password, role=entity.role
        )
        self._session.add(db_user)
        self._session.commit()


    def add_account(self, entity: Account, new_cust_id: str):
        db_acc= BankAccount(
            bank_acc_id=entity.bank_acc_id,
            fullname=entity.fullname,
            address=entity.address,
            contact_no=entity.contact_no,
            balance=entity.balance,
            cust_id = new_cust_id
        )
        self._session.add(db_acc)
        self._session.commit()
        

    def get_user_by_id(self, id: str)->BankAccount|None:
        valid_user = self._session.query(UserSchema).filter(UserSchema.cust_id == id).first()
        if valid_user:
            return BankAccount


    def add_balance(self, model: Amount, id:str)->Account:
        account = self._session.query(BankAccount).filter(BankAccount.cust_id == id).first()
        if account:
            account.balance += model.amount #type:ignore
            account.updated_at = datetime.now()  #type:ignore
            self._session.commit()
        return account
    

    def get_account(self, id: str) -> BankAccount | None:
        bank_acc = self._session.query(BankAccount).filter(BankAccount.cust_id == id).first()
        return bank_acc if bank_acc is not None else  None
    

    def deduct_balance(self, model: Amount, id: str) -> BankAccount:
        account = self._session.query(BankAccount).filter(BankAccount.cust_id == id).first()
        if account:
            account.balance -= model.amount #type:ignore
            account.updated_at = datetime.now() #type: ignore
            self._session.commit()
        return account


    def get_detail(self, id:str)-> UserViewDetails|None:
        user_details = self._session.execute(
            select(
                UserSchema.cust_id,
                UserSchema.username,
                BankAccount.bank_acc_id,
                BankAccount.fullname,
                BankAccount.address,
                BankAccount.contact_no,
                BankAccount.balance,
                BankAccount.updated_at,
            )
            .outerjoin(BankAccount, UserSchema.cust_id == BankAccount.cust_id)
            .where(UserSchema.cust_id == id)
        ).mappings().fetchone() 
        return UserViewDetails(**user_details) if user_details else None
    

    def get_transactions(self, id:str)->list|None:
        bank_acc_id = self._session.execute(
            select(BankAccount.bank_acc_id).where(BankAccount.cust_id == id)
        ).scalar()
        transactions = self._session.execute(
            select(Transactions).where(Transactions.bank_acc_id == bank_acc_id)
        ).fetchall()
        transactions= [
            UserTransactionDetails(**transaction[0].__dict__)
            for transaction in transactions
        ]
        return transactions
