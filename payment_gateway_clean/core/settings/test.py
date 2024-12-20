import logging 

from pydantic import computed_field
from sqlalchemy import NullPool

from core.settings.app import AppSettings

class TestAppSettings(AppSettings):
    debug: bool =True


    title: str = "[TEST] Payment Gateway"
    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env.test"

    

    @computed_field
    @property
    def sqlalchemy_engine_props(self) -> dict:
        return dict(
            url=self.sql_db_uri,
            echo=False,
            poolclass=NullPool,
            isolation_level="AUTOCOMMIT"
        )
