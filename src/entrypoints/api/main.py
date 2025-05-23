from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.modules.infrastructure.persistence.database import init_db
from src.modules.infrastructure.persistence.settings import AppSettings
from src.entrypoints.api.admin import routes as admin_routes
from src.entrypoints.api.user import routes as user_routes
from src.modules.infrastructure.persistence.dbschemas.admin import AdminSchema
from src.modules.infrastructure.persistence.dbschemas.user import *
from src.modules.infrastructure.persistence.database import get_db_session
from src.entrypoints.api.handlers.middleware import CustomExceptionMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = AppSettings()  # type:ignore
    print("Starting Server")
    init_db(app.state.settings.database)
    yield
    print("Stopping Server")


def init_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(admin_routes.router)
    app.include_router(user_routes.router)
    # user middlewares
    app.add_middleware(CustomExceptionMiddleware)
    return app


app = init_app()
