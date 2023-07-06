import logging

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

from bot.config import API_TOKEN

logging.basicConfig(level=logging.INFO)
session = AiohttpSession(
    api=TelegramAPIServer.from_base('http://192.168.0.108:8081'),
    timeout=0
)
bot = Bot(token=API_TOKEN, session=session)
dp = Dispatcher()
