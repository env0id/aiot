from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from db import create_db_and_tables
from config import BOT_TOKEN
import logging

logger = logging.getLogger(__name__)

bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

async def on_startup(bot: Bot):
  await bot.set_my_commands([BotCommand(command="start", description="Start the bot")])
  await create_db_and_tables()
  me = await bot.get_me()
  logger.warning(f'@{me.username} is running..')

async def on_shutdown():
  await dp.storage.close()
  logger.warning('Shutting down..')

def main() -> None:
  dp.startup.register(on_startup)
  dp.shutdown.register(on_shutdown)
  dp.run_polling(bot)