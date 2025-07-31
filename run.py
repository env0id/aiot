from aiogram import Router

from bot import dp, main


main_router = Router()
dp.include_router(main_router)


if __name__ == '__main__':
  main()