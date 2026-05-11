from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from typing import Union
from services.user import UserService

start_router = Router()

class StartCallback(CallbackData, prefix="start"):
  level: int

def create_callback_start(level: int = 0):
  return StartCallback(level=level).pack()

@start_router.message(Command("start"))
async def start(message: Union[Message, CallbackQuery]):
  telegram_user = message.from_user
  translations = await UserService.get_translations(telegram_user.id)
  await UserService.user_logged(telegram_user.id, telegram_user.username, telegram_user.full_name)
  if isinstance(message, Message):
    await message.answer(translations["start"])
  if isinstance(message, CallbackQuery):
    await message.message.edit_text(translations["start"])


@start_router.callback_query(StartCallback.filter())
async def start_menu_navigation(callback: CallbackQuery, callback_data: StartCallback):
  current_level = callback_data.level

  levels = {
    0: start,
  }
  current_level_function = levels[current_level]
  await current_level_function(callback)