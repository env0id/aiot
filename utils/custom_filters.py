from aiogram.types import Message
from aiogram.filters import BaseFilter
from services.user import UserService
from config import ADMIN_ID_LIST


class AdminFilter(BaseFilter):
  async def __call__(self, message: Message):
    return message.from_user.id in ADMIN_ID_LIST

class IsUserExistFilter(BaseFilter):
  async def __call__(self, message: Message):
    return await UserService.is_exist(message.from_user.id)