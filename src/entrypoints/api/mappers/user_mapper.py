import hashlib, uuid
from src.entrypoints.api.user.models import AmountModel, CreateUserModel
from src.modules.domain.user.entity import BankAccount, Transactions, User
from src.modules.infrastructure.auth.helpers import hash_password
from src.modules.infrastructure.persistence.dbschemas.user import BankAccountSchema


def model_to_user_entity(model: CreateUserModel) -> User:
    password = hashlib.sha256(model.username.encode()).hexdigest()[:12]
    hashed_pw = hash_password(password)
    return User(
        cust_id=f"CUST-{str(uuid.uuid4())[:8]}",
        username=model.username,
        password=password,
        hashed_pw=hashed_pw,
        role="user",
        fullname=model.fullname,
        address=model.address,
        contact_no=model.contact_no,
        opening_balance=model.opening_balance,
    )


def model_to_transaction_entity(model: AmountModel, id: str) -> Transactions:
    return Transactions(cust_id=id, amount=model.amount)


def orm_to_user_entity(data: dict) -> User:
    return User(
        cust_id=data["cust_id"],
        username=data["username"],
        password=data.get("password", ""),
        hashed_pw=data.get("hashed_pw", ""),
        role=data.get("role", "user"),
        fullname=data.get("fullname", ""),
        address=data.get("address", ""),
        contact_no=data.get("contact_no", ""),
        opening_balance=data.get("opening_balance", 0.0),
    )


def orm_to_bankaccount_entity(account: BankAccountSchema) -> BankAccount:
    return BankAccount(
        bank_acc_id=str(account.bank_acc_id),
        balance=float(account.balance),  # type:ignore
    )
