from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    host: str
    port: int
    name: str
    user: str
    password: SecretStr


class DefaultSettings(BaseModel):
    secret: SecretStr
    algorithm: str


class AppSettings(BaseSettings):
    database: DatabaseSettings  
    default: DefaultSettings  

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
