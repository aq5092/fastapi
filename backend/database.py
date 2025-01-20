from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"  # SQLite fayl uchun yo'l

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # SQLite uchun maxsus parametr
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
