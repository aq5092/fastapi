from sqlalchemy.ext.asyncio import create_async_engine, async_session

engine = create_async_engine("sqlite+aiosqlite:///books.db", echo=True, future=True)
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column, Column, Integer, String

new_session = async_session(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

class Base(DeclarativeBase):
    pass

class BookModel(Base):
    __tablename__ = "books"

    id = Mapped[int] = ma