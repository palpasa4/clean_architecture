from dataclasses import dataclass
from uuid import UUID


@dataclass
class Admin:
    admin_id: str
    username: str
    password: str
    role : str
