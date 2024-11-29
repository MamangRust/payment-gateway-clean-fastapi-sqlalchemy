import logging

from pydantic import computed_field
from core.settings.app import AppSettings

class DevAppSettings(AppSettings):
    debug: bool= True

    title: str = "[DEV] Payment Gateway API"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env.dev"


    @computed_field
    @property
    def sqlalchemy_engine_props(self) -> dict:
        return dict(url=self.sql_db_uri, echo=True)