import asyncio

from bot.loader import dp, bot
from bot.commands import register_commands
from bot.database.init_database import init_db, close_db
from bot.middlewares import setup_i18n
from bot.utils.services import register_services
from bot.handlers import root_router


async def main():
    await init_db()
    setup_i18n(dp)
    await register_commands()
    dp.include_router(root_router)
    register_services()
    await dp.start_polling(bot)
    await close_db()


if __name__ == "__main__":
    asyncio.run(main())
