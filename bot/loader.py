import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from bot.config import API_TOKEN

logging.basicConfig(level=logging.INFO)
print(API_TOKEN)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
