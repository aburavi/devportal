import os

import structlog
from sqlalchemy.ext.asyncio import create_async_engine

from repository import UserappRepository
from application import UserappApplication
from api import UserappAPI

POSTGRES_DB_SERVER = os.getenv("POSTGRES_DB_SERVER", "10.8.0.25")
POSTGRES_DB_PORT = os.getenv("POSTGRES_DB_PORT", "5432")
POSTGRES_DB_API_USER = os.getenv("POSTGRES_DB_API_USER", "postgres")
POSTGRES_DB_API_PASSWORD = os.getenv("POSTGRES_DB_API_PASSWORD", "password")
POSTGRES_DB_API = os.getenv("POSTGRES_DB_API", "openapi.public")
POSTGRES_DB_URI = f"postgresql+asyncpg://{POSTGRES_DB_API_USER}:{POSTGRES_DB_API_PASSWORD}@{POSTGRES_DB_SERVER}:{POSTGRES_DB_PORT}/{POSTGRES_DB_API}"
SERVICE_CORE_URL = os.getenv("SERVICE_CORE_URL", "http://34.126.180.185:8888")
JWT_PUBKEY = os.getenv("SERVICE_APP_JWT_PUBKEY", 'None')

engine = create_async_engine(
    POSTGRES_DB_URI,
    echo=False,  # set it to True if you wanna know what sqlalchemy did
    pool_size=100,
    max_overflow=200,
    pool_recycle=300,
    pool_pre_ping=True,
    pool_use_lifo=True,
)
logger = structlog.get_logger("userapp")

repo = UserappRepository(engine, logger)
app = UserappApplication(repo, logger, SERVICE_CORE_URL)
api = UserappAPI(app)
