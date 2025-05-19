from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base
from src.config.settings import DatabaseSettings


# private varialbe, do not import
_engine = None


Base = declarative_base()


def init_db(settings: DatabaseSettings):
    global _engine
    _engine = create_engine(
        f"postgresql://{settings.user}:{settings.password.get_secret_value()}@{settings.host}:{settings.port}/{settings.name}"
    )
    Base.metadata.create_all(bind=_engine)


def get_db_session():
    with Session(_engine) as session:
        yield session
