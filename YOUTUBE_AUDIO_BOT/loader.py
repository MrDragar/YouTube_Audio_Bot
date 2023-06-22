from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.bot.api import TelegramAPIServer
from YOUTUBE_AUDIO_BOT.middleware import register_middleware

from YOUTUBE_AUDIO_BOT.config import API_TOKEN


# Initialize FSM storage
memory_storage = MemoryStorage()

local_server = TelegramAPIServer.from_base('http://0.0.0.0:8081')
# Initialize bot and dispatcher
# bot = Bot(token=API_TOKEN, server=local_server, timeout=0)
bot = Bot(token=API_TOKEN, timeout=0)

dp = Dispatcher(bot, storage=memory_storage)
i18n = register_middleware(dp)
_ = i18n.gettext
