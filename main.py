import asyncio

from bot.loader import dp, bot
from bot.handlers import root_router


async def main():
    dp.include_router(root_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
