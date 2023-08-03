import os
from typing import AsyncIterable

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

load_dotenv()

pg_user: str = os.environ.get("POSTGRES_USER")
pg_pass: str = os.environ.get("POSTGRES_PW")
pg_host: str = os.environ.get("POSTGRES_HOST")
pg_DB: str = os.environ.get("POSTGRES_DB")

engine = create_engine(f'postgresql://{pg_user}:{pg_pass}!@{pg_host}:5432/{pg_DB}')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_db():
    db = db_session
    try:
        yield db
    finally:
        db.close()
