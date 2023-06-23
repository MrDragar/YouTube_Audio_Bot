import asyncio

from bot.loader import dp, bot
from bot.handlers import root_router
from bot.database.init_database import init_db, close_db


async def main():
    await init_db()
    dp.include_router(root_router)
    await dp.start_polling(bot)
    await close_db()


if __name__ == "__main__":
    asyncio.run(main())
