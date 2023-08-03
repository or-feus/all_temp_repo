from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

info = {
    "id": "root",
    "password": "tkvkdldj1!",
    "host": "localhost",
    "port": 3306,
}

sql_db_url = f"mysql://{info['id']}:{info['password']}@{info['host']}/"

engine = create_engine(sql_db_url)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



