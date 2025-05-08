from src.modules.domain.user.repository import UserRepository
from src.modules.infrastructure.persistence.dbschemas.user import UserSchema, BankAccount
from sqlalchemy.orm import Session
from src.modules.domain.user.entity import User, Account


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
        