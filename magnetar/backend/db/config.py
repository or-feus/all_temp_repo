import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

from utils.logger import get_logger

logger = get_logger(__name__)
load_dotenv()


class Settings(BaseSettings):
    pg_user = os.environ.get("POSTGRES_USER")
    pg_pass = os.environ.get("POSTGRES_PW")
    pg_host = os.environ.get("POSTGRES_HOST")
    pg_DB = os.environ.get("POSTGRES_DB")

    print(f"pg_user: {pg_user}, pg_pass:{pg_pass}, pg_host: {pg_host}, pg_db: {pg_DB}")

    asyncpg_url: str = f"postgresql+asyncpg://{pg_user}:{pg_pass}@{pg_host}:5432/{pg_DB}"


@lru_cache
def get_settings():
    logger.info("Loading config settings from the environment...")
    return Settings()
