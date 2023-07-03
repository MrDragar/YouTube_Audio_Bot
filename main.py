import asyncio

from bot.loader import dp, bot
from bot.database.init_database import init_db, close_db
from bot.middlewares import setup_i18n


async def main():
    await init_db()
    setup_i18n(dp)
    from bot.handlers import root_router
    dp.include_router(root_router)
    await dp.start_polling(bot)
    await close_db()


if __name__ == "__main__":
    asyncio.run(main())
