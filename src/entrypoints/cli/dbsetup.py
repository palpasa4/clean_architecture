from src.config.postgresdb import init_db
from src.config.settings import AppSettings


def setup_db():
    settings = AppSettings()  # type: ignore
    init_db(settings.database)


if __name__ == "__main__":
    setup_db()
