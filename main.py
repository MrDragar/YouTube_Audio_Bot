from YOUTUBE_AUDIO_BOT import database
from YOUTUBE_AUDIO_BOT.config import register_handlers
from YOUTUBE_AUDIO_BOT.middleware import register_middleware

import os
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.bot.api import TelegramAPIServer


API_TOKEN = os.environ.get("API_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize FSM storage
memory_storage = MemoryStorage()

local_server = TelegramAPIServer.from_base('http://0.0.0.0:8081')

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, server=local_server)
# bot = Bot(token=API_TOKEN)


dp = Dispatcher(bot, storage=memory_storage)


if __name__ == '__main__':
    register_handlers(dp)
    register_middleware(dp)
    database.init_db()
    executor.start_polling(dp, skip_updates=False, timeout=1000000)

