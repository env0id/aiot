import os
from sqlalchemy import event, Engine, inspect, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import DB_NAME
from models.base import Base


url = f"sqlite+aiosqlite:///data/{DB_NAME}"

os.makedirs("data", exist_ok=True)
engine = create_async_engine(url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
  cursor = dbapi_connection.cursor()
  cursor.execute("PRAGMA foreign_keys=ON")
  cursor.close()


async def check_all_tables_exist(db_engine):
  async with db_engine.begin() as conn:
    for table in Base.metadata.tables.values():
      result = await conn.execute(
        text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table.name}'"))
      if result.scalar() is None:
        return False
  return True


async def create_db_and_tables():
  async with engine.begin() as conn:
    if not await check_all_tables_exist(engine):
      await conn.run_sync(Base.metadata.drop_all)
      await conn.run_sync(Base.metadata.create_all)