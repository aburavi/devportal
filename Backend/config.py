from typing import Dict, Any, Optional
from pydantic import (
    validator,
)
from baseconfig import BaseAppSettings
import os

# BaseSettings get data from .env
class Settings(BaseAppSettings):
    POSTGRES_DB_SERVER_TEST: str = ''
    POSTGRES_DB_USER_TEST: str = ''
    POSTGRES_DB_PASSWORD_TEST: str = ''
    POSTGRES_DB_TEST: str = ''
    SQLALCHEMY_WITH_DRIVER_URI_TEST: Optional[str] = None

    @validator("SQLALCHEMY_WITH_DRIVER_URI_TEST", pre=True)
    def postgresql_db_connection_test(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if isinstance(v, str):
            return v

        # dialect[+driver]://user:password@host/dbname[?key=value..]
        scheme = "postgresql"
        driver = "asyncpg"
        user = values.get("POSTGRES_DB_USER_TEST")
        password = values.get("POSTGRES_DB_PASSWORD_TEST")
        host = values.get("POSTGRES_DB_SERVER_TEST")
        database = values.get("POSTGRES_DB_TEST")
        return "{}+{}://{}:{}@{}/{}".format(scheme, driver, user, password, host, database)

    # --

# --


settings = Settings()
