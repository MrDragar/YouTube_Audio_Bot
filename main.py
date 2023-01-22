from YOUTUBE_AUDIO_BOT import database
from YOUTUBE_AUDIO_BOT.middleware import register_middleware
from YOUTUBE_AUDIO_BOT.config import dp
from YOUTUBE_AUDIO_BOT.register_commands import register_handlers, register_commands
from YOUTUBE_AUDIO_BOT.filters import register_filters
from YOUTUBE_AUDIO_BOT.services import register_services

import logging
import asyncio

from aiogram import executor, Dispatcher


async def on_startup(dispatcher: Dispatcher):
    await register_commands(dispatcher)
    asyncio.create_task(register_services(dispatcher))


# Configure logging
logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    register_filters(dp)
    register_handlers(dp)
    database.init_db()
    executor.start_polling(dp, skip_updates=False, timeout=1000000, on_startup=on_startup)

