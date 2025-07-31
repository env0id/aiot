import logging
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode


from config import BOT_TOKEN
from db import create_db_and_tables

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher(storage=MemoryStorage())

async def on_startup(bot: Bot):
  await create_db_and_tables()

async def on_shutdown():
  await dp.storage.close()
  logging.warning('Shutting down..')
  logging.warning('Bye!')

def main() -> None:
  dp.startup.register(on_startup)
  dp.shutdown.register(on_shutdown)
  dp.run_polling(bot, skip_updates=True)