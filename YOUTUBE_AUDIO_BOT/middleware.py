from typing import Tuple, Optional, Any

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram import Dispatcher

from YOUTUBE_AUDIO_BOT import database

I18N_DOMAIN = 'messages'
LOCALES_DIR = 'locales'


class UsersLanguage(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> Optional[str]:
        user = types.User.get_current()
        language = database.get_language(user.id)
        return language or user.locale


def register_middleware(dp: Dispatcher):
    i18n = UsersLanguage(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n
