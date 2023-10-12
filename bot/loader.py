from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

from bot.config import API_TOKEN, DEBUG

session = AiohttpSession(
    api=TelegramAPIServer.from_base('http://localhost:8081'),
    timeout=0
)
if DEBUG:
    session = AiohttpSession(
        timeout=0
    )

bot = Bot(token=API_TOKEN, session=session)
dp = Dispatcher()
