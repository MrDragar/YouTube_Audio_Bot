from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.bot.api import TelegramAPIServer
import os

from YOUTUBE_AUDIO_BOT.middleware import register_middleware


admins_id = ["1241783757", "625706122"]
API_TOKEN = os.environ.get("API_TOKEN")

languages = {
    "en": "English",
    "ru": "Русский",
    "uk": "Українська"
}

# Initialize FSM storage
memory_storage = MemoryStorage()

local_server = TelegramAPIServer.from_base('http://0.0.0.0:8081')
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, server=local_server, timeout=0)
dp = Dispatcher(bot, storage=memory_storage)
i18n = register_middleware(dp)
_ = i18n.gettext
