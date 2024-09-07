import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

username = os.environ.get("DB_USERNAME"),
password = os.environ.get("DB_PASSWORD"),
host = os.environ.get("DB_HOST"),
db_name = os.environ.get("DB_NAME")

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{username[0]}:{password[0]}@{host[0]}/{db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
