from aiogram.types import Update, FSInputFile
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


async def run_polling():
    await init_db()
    await register_commands()
    await dp.start_polling(bot)
    await close_db()

def main():
    setup_i18n(dp)
    dp.include_router(root_router)
    register_services()
    if config.DEBUG:
        asyncio.run(run_polling())
    else:
        app = FastAPI(docs_url=None)
        WEBHOOK_PATH = "/bot/" + config.API_TOKEN
        WEBHOOK_URL = f"https://{config.WEBHOOK_HOST}:{config.WEBHOOK_PORT}" +\
                      WEBHOOK_PATH
        @app.post(WEBHOOK_PATH)
        async def webhoock_response(update: dict):
            return await dp.feed_update(bot=bot, update=Update(**update))

        @app.on_event("startup")
        async def init_bot():
            await init_db()
            await register_commands()
            webhook_info = await bot.get_webhook_info()
            if webhook_info.url != WEBHOOK_URL:
                await bot.set_webhook(
                    url=WEBHOOK_URL,
                    certificate=FSInputFile("cert.pem")
                )

        @app.on_event("shutdown")
        async def on_shutdown():
            await bot.delete_webhook()
            await close_db()

        uvicorn.run(app, host=config.WEBHOOK_HOST, port=config.WEBHOOK_PORT,
                    ssl_certfile="./cert.pem", ssl_keyfile="./key.pem")



if __name__ == "__main__":
    main()
