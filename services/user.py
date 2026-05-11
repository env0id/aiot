from sqlalchemy import select, update, func
from db import async_session_maker
from models.user import User
from services.language import LanguageService
from config import PAGE_ENTRIES
import datetime


class UserService:
  @staticmethod
  async def is_exist(telegram_id: int) -> bool:
    async with async_session_maker() as session:
      stmt = select(User).where(User.telegram_id == telegram_id)
      is_exist = await session.execute(stmt)
      return is_exist.scalar() is not None

  @staticmethod
  async def get_next_user_id() -> int:
    async with async_session_maker() as session:
      query = select(User.id).order_by(User.id.desc()).limit(1)
      last_user_id = await session.execute(query)
      last_user_id = last_user_id.scalar()
      if last_user_id is None:
        return 0
      else:
        return int(last_user_id) + 1

  @staticmethod
  async def create(telegram_id: int, telegram_username: str, full_name: str):
    async with async_session_maker() as session:
      next_user_id = await UserService.get_next_user_id()
      new_user = User(
        id=next_user_id,
        telegram_username=telegram_username,
        full_name=full_name,
        telegram_id=telegram_id,
      )
      session.add(new_user)
      await session.commit()

  @staticmethod
  async def user_logged(telegram_id: int, telegram_username: str, full_name: str):
    is_exist = await UserService.is_exist(telegram_id)
    if is_exist is False:
      await UserService.create(telegram_id, telegram_username, full_name)
    else:
      await UserService.update_user(telegram_id, telegram_username, full_name, True)

  @staticmethod
  async def update_user(telegram_id: int, telegram_username: str, full_name: str, can_receive_messages: bool):
    async with async_session_maker() as session:
      stmt = update(User).where(User.telegram_id == telegram_id).values(
          can_receive_messages=can_receive_messages,
          telegram_username=telegram_username,
          full_name=full_name,
        )
      await session.execute(stmt)
      await session.commit()

  @staticmethod
  async def get_by_tgid(telegram_id: int) -> User:
    async with async_session_maker() as session:
      stmt = select(User).where(User.telegram_id == telegram_id)
      user_from_db = await session.execute(stmt)
      user_from_db = user_from_db.scalar()
      return user_from_db
    
  @staticmethod
  async def update_language(telegram_id: int, language_code):
    async with async_session_maker() as session:
      user_from_db = await UserService.get_by_tgid(telegram_id)
      if user_from_db and user_from_db.language != language_code:
        stmt = update(User).where(User.telegram_id == telegram_id).values(language=language_code)
        await session.execute(stmt)
        await session.commit()
      
  @staticmethod
  async def get_max_page_for_users_by_timedelta(timedelta_int):
    async with async_session_maker() as session:
      current_time = datetime.datetime.now()
      one_day_interval = datetime.timedelta(days=int(timedelta_int))
      time_to_subtract = current_time - one_day_interval
      stmt = select(func.count(User.id)).where(User.registered_at >= time_to_subtract, User.telegram_username != None)
      users = await session.execute(stmt)
      users = users.scalar_one()
      if users % PAGE_ENTRIES == 0:
        return users // PAGE_ENTRIES - 1
      else:
        return users // PAGE_ENTRIES

  @staticmethod
  async def get_translations(telegram_id):
    user = await UserService.get_by_tgid(telegram_id)
    if user is None:
      return LanguageService.get_default_translation()
    return LanguageService.get_by_code(user.language)
  
  @staticmethod
  async def get_all_users_count():
    async with async_session_maker() as session:
      stmt = func.count(User.id)
      users_count = await session.execute(stmt)
      return users_count.scalar()

  @staticmethod
  async def get_users_tg_ids_for_sending():
    async with async_session_maker() as session:
      stmt = select(User.telegram_id).where(User.can_receive_messages == True)
      user_ids = await session.execute(stmt)
      user_ids = user_ids.scalars().all()
      return user_ids
    
  @staticmethod
  async def get_new_users_by_timedelta(timedelta_int, page):
    async with async_session_maker() as session:
      current_time = datetime.datetime.now()
      one_day_interval = datetime.timedelta(days=int(timedelta_int))
      time_to_subtract = current_time - one_day_interval
      stmt = select(User).where(User.registered_at >= time_to_subtract, User.telegram_username != None).limit(
        PAGE_ENTRIES).offset(page * PAGE_ENTRIES)
      count_stmt = select(func.count(User.id)).where(User.registered_at >= time_to_subtract)
      users = await session.execute(stmt)
      users_count = await session.execute(count_stmt)
      return users.scalars().all(), users_count.scalar_one()