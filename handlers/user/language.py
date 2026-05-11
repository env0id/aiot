from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.user import UserService
from utils.custom_filters import IsUserExistFilter
from services.language import LanguageService

language_router = Router()

class LanguageCallback(CallbackData, prefix="language"):
  level: int
  language_code: str

def create_callback_language(level: int = 0, language_code: str = ""):
  return LanguageCallback(level=level, language_code=language_code).pack()

  
async def select_language(callback: CallbackQuery):
  from handlers.user.start import create_callback_start
  translations = await UserService.get_translations(callback.from_user.id)
  language_builder = InlineKeyboardBuilder()
  languages = LanguageService.get_all()
  for language in languages:
    language_builder.button(text=language["name"], callback_data=create_callback_language(1, language["code"]))
  language_builder.button(text=translations["back"], callback_data=create_callback_start(0))
  language_builder.adjust(1)
  await callback.message.edit_text(translations["select_language"], reply_markup=language_builder.as_markup())


async def change_language(callback: CallbackQuery):
  from handlers.user.start import start
  unpacked_callback = LanguageCallback.unpack(callback.data)
  telegram_id = callback.from_user.id
  await UserService.update_language(telegram_id, unpacked_callback.language_code)
  await start(callback)


@language_router.callback_query(LanguageCallback.filter(), IsUserExistFilter())
async def navigate(callback: CallbackQuery, callback_data: LanguageCallback):
  current_level = callback_data.level

  levels = {
    0: select_language,
    1: change_language,
  }

  current_level_function = levels[current_level]
  await current_level_function(callback)