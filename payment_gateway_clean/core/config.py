from functools import lru_cache
from enum import Enum
from core.settings.app import AppSettings
from core.settings.base import AppEnyTypes, BaseAppSettings
from core.settings.development import DevAppSettings
from core.settings.production import ProdAppSettings
from core.settings.test import TestAppSettings

class AppEnvTypes(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"

environment: dict[AppEnvTypes, type[AppSettings]] = {
    AppEnvTypes.DEVELOPMENT: DevAppSettings,
    AppEnvTypes.TESTING: TestAppSettings,
    AppEnvTypes.PRODUCTION: ProdAppSettings,
}

@lru_cache
def get_app_settings() -> AppSettings:
    # Get the app environment from base settings
    app_env = BaseAppSettings().app_env

    # Normalize the app_env value
    normalized_env = {
        'prod': AppEnvTypes.PRODUCTION,
        'production': AppEnvTypes.PRODUCTION,
        'dev': AppEnvTypes.DEVELOPMENT,
        'development': AppEnvTypes.DEVELOPMENT,
        'test': AppEnvTypes.TESTING,
        'testing': AppEnvTypes.TESTING
    }.get(app_env.lower())

    if normalized_env is None:
        raise ValueError(f"Unknown environment: {app_env}")


    # Get the corresponding config class and instantiate
    config_class = environment[normalized_env]

    return config_class()