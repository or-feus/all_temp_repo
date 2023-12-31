from typing import AsyncGenerator

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from db.config import get_settings

Base = declarative_base()

global_settings = get_settings()
url = global_settings.asyncpg_url

engine = create_async_engine(url, future=True, echo=True)

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        try:
            yield session
            await session.commit()

        except SQLAlchemyError as sql_ex:
            await session.rollback()
            raise sql_ex

        except HTTPException as http_ex:
            await session.rollback()
            raise http_ex

        finally:
            await session.close()

