from aiogram.types import Update
from fastapi import FastAPI
import uvicorn

import asyncio

from bot.loader import dp, bot
from bot.commands import register_commands
from bot.database.init_database import init_db, close_db
from bot.middlewares import setup_i18n
from bot.utils.services import register_services
from bot.handlers import root_router
import bot.config as config


async def main():
    await init_db()
    setup_i18n(dp)
    dp.include_router(root_router)
    await register_commands()
    register_services()
    # if config.DEBUG:
    await dp.start_polling(bot)
    # else:
    #     app = FastAPI(docs_url=None)
    #     @app.post("/webhoock")
    #     async def webhoock_response(update: dict):
    #         return await dp.feed_update(bot=bot, update=Update(**update))
    #
    #     @app.on_event("startup")
    #     async def init_bot():
    #         await init_db()
    #         await register_commands()
    #         await bot.set_webhook("127.0.0.1:8081/bot/" + config.API_TOKEN)
    #     uvicorn.run(app, host=config.WEBHOOK_HOST, port=config.WEBHOOK_PORT)
    await close_db()


if __name__ == "__main__":
    main()
