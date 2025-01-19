from config import settings
from sqlalchemy import URL, create_engine, text 
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_session

engine = create_engine(
    settings.DATABASE_URL_psycopg2, 
    # echo=True, 
    # future=True,
    max_overflow=10, 
    pool_size=5,)

with engine.connect() as connection:
    result = connection.execute(text("SELECT version()"))
    print(f'{result.all()}')