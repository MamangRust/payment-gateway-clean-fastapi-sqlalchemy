from pydantic import Extra, computed_field
from pydantic_settings import BaseSettings
from sqlalchemy import URL


class AppEnyTypes:
    production : str = "prod"
    development: str = "dev"
    testing: str = "test"



class BaseAppSettings(BaseSettings):
    app_env: str = AppEnyTypes.production

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str

    jwt_secret_key: str
    jwt_token_expiration_minutes: int = 60 * 24 * 7  # one week.
    jwt_algorithm: str = "HS256"

    class Config:
        env_file = ".env"
        extra = Extra.ignore

    @computed_field 
    @property
    def sql_db_uri(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )

    @computed_field  
    @property
    def sqlalchemy_engine_props(self) -> dict:
        return dict(url=self.sql_db_uri)