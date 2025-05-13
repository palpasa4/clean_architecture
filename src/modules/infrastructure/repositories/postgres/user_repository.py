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

    def __init__(self, db: Session):
        self._session = db

    def get_user_by_username(self, username: str) -> User | None:
        user = self._session.query(UserSchema).filter_by(username=username).first()
        if user:
            user_entity = orm_to_user_entity(user.__dict__)
            return user_entity

    def add_user(self, entity: User) -> None:
        db_user = UserSchema(
            cust_id=entity.cust_id,
            username=entity.username,
            password=entity.hashed_pw,
            role=entity.role,
        )
        self._session.add(db_user)
        self._session.commit()

    def add_account(self, user_entity: User, account_entity: BankAccount) -> None:
        db_acc = BankAccountSchema(
            bank_acc_id=account_entity.bank_acc_id,
            fullname=user_entity.fullname,
            address=user_entity.address,
            contact_no=user_entity.contact_no,
            balance=account_entity.balance,
            cust_id=user_entity.cust_id,
        )
        self._session.add(db_acc)
        self._session.commit()

    def get_user_by_id(self, id: str) -> User | None:
        valid_user = (
            self._session.query(UserSchema).filter(UserSchema.cust_id == id).first()
        )
        if valid_user:
            user_entity = orm_to_user_entity(valid_user.__dict__)
            return user_entity

    def add_balance(self, entity: Transactions) -> BankAccount | None:
        account = (
            self._session.query(BankAccountSchema)
            .filter(BankAccountSchema.cust_id == entity.cust_id)
            .first()
        )
        if account:
            account.balance += entity.amount  # type:ignore
            account.updated_at = datetime.now()  # type:ignore
            self._session.commit()
            account_entity = orm_to_bankaccount_entity(account)
            return account_entity

    def get_account(self, id: str) -> BankAccount | None:
        bank_acc = (
            self._session.query(BankAccountSchema)
            .filter(BankAccountSchema.cust_id == id)
            .first()
        )
        if bank_acc:
            return orm_to_bankaccount_entity(bank_acc)

    def deduct_balance(self, entity: Transactions) -> BankAccount | None:
        account = (
            self._session.query(BankAccountSchema)
            .filter(BankAccountSchema.cust_id == entity.cust_id)
            .first()
        )
        if account:
            account.balance -= entity.amount  # type: ignore
            account.updated_at = datetime.now()  # type: ignore
            self._session.commit()
            account_entity = orm_to_bankaccount_entity(account)
            return account_entity

    def get_detail(self, id: str) -> UserViewDetails | None:
        user_details = (
            self._session.execute(
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
                .outerjoin(
                    BankAccountSchema, UserSchema.cust_id == BankAccountSchema.cust_id
                )
                .where(UserSchema.cust_id == id)
            )
            .mappings()
            .fetchone()
        )
        return UserViewDetails(**user_details) if user_details else None

    def get_transactions(self, id: str) -> list[UserTransactionDetails] | None:
        bank_acc_id = self._session.execute(
            select(BankAccountSchema.bank_acc_id).where(BankAccountSchema.cust_id == id)
        ).scalar()
        if not bank_acc_id:
            return None
        stmt = select(
            TransactionsSchema.transaction_id,
            TransactionsSchema.bank_acc_id,
            TransactionsSchema.transaction_type,
            TransactionsSchema.amount,
            TransactionsSchema.previous_balance,
            TransactionsSchema.new_balance,
            TransactionsSchema.timestamp,
        ).where(TransactionsSchema.bank_acc_id == bank_acc_id)
        transactions = self._session.execute(stmt).mappings().all()
        transactions_list = [
            UserTransactionDetails(**transaction) for transaction in transactions
        ]
        return transactions_list
