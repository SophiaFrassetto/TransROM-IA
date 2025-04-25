from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

# Get database URL from environment or construct it from components
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DB_USER = quote_plus(os.getenv("POSTGRES_USER", "postgres"))
    DB_PASSWORD = quote_plus(os.getenv("POSTGRES_PASSWORD", "postgres"))
    DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
    DB_NAME = os.getenv("POSTGRES_DB", "transrom")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Create engine with explicit encoding settings
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "client_encoding": "utf8",
        "options": "-c client_encoding=utf8"
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
