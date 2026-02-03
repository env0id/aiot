from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.engine import make_url
from sqlalchemy import inspect
from pathlib import Path
from models.base import Base
from config import DB_URL


engine = create_async_engine(DB_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)

def ensure_db_directory(db_url: str) -> None:
  url = make_url(db_url)
  if url.drivername.startswith("sqlite") and url.database:
    Path(url.database).parent.mkdir(parents=True, exist_ok=True)

async def check_all_tables_exist(db_engine):
  async with db_engine.connect() as conn:
    existing_tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
    for table in Base.metadata.tables.values():
      if table.name not in existing_tables:
        return False
    return True

async def create_db_and_tables():
  ensure_db_directory(DB_URL)
  async with engine.begin() as conn:
    if not await check_all_tables_exist(engine):
      await conn.run_sync(Base.metadata.drop_all)
      await conn.run_sync(Base.metadata.create_all)