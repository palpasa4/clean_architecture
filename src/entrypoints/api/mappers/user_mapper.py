import hashlib, uuid
from src.entrypoints.api.user.models import CreateUserModel
from src.modules.domain.user.entity import User
from src.modules.infrastructure.auth.password_utils import hash_password


def model_to_user_entity(model: CreateUserModel) -> User:
    password= hashlib.sha256(model.username.encode()).hexdigest()[:12]
    hashed_pw = hash_password(password)
    return User(
        cust_id= f"CUST-{str(uuid.uuid4())[:8]}",
        username= model.username,
        password= password,
        hashed_pw= hashed_pw,
        role="user",
        fullname= model.fullname,
        address= model.address,
        contact_no=model.contact_no,
        opening_balance=model.opening_balance
    )


# def orm_to_user_entity(data : dict) -> User:
#     return User(
#         cust_id= data["cust_id"],
#         username= data["username"],
#         password= data["password"],
#         role = data["role"]
#     )
