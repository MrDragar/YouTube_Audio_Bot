from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from aiogram import Dispatcher

from YOUTUBE_AUDIO_BOT import database


class UsersLanguage(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        database.add_user(message.from_user.id, message.from_user.full_name, message.from_user.language_code)
        language = database.get_language(message.from_user.id)
        data["language"] = language
        if language == "uk":
            data["language"] = 'ru'


def register_middleware(dp: Dispatcher):
    dp.middleware.setup(UsersLanguage())
