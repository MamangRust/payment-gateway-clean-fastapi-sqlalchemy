from functools import lru_cache
from enum import Enum
from core.settings.app import AppSettings
from core.settings.base import AppEnvTypes, BaseAppSettings
from core.settings.development import DevAppSettings
from core.settings.production import ProdAppSettings
from core.settings.test import TestAppSettings

AppEnvType = DevAppSettings | TestAppSettings | ProdAppSettings

environments: dict[str, type[AppEnvType]] = {
    AppEnvTypes.development: DevAppSettings,
    AppEnvTypes.testing: TestAppSettings,
    AppEnvTypes.production: ProdAppSettings,
}

@lru_cache
def get_app_settings() -> AppSettings:
    base_settings = BaseAppSettings()
    app_env = base_settings.app_env

    if app_env not in environments:
        raise ValueError(f"Invalid app_env: {app_env}")

    config_class = environments[app_env]
    return config_class()
