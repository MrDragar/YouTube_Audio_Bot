from aiogram.types import Message
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import I18nMiddleware, ConstI18nMiddleware
from aiogram import Dispatcher

from typing import Dict, Any
from bot.database.user import create_user


class DatabaseI18nMiddleware(I18nMiddleware):
    async def get_locale(self, event: Message, data: Dict[str, Any]) -> str:
        user = await create_user(id=event.from_user.id,
                                 name=event.from_user.full_name,
                                 language=event.from_user.language_code)
        return user.language.value


def setup_i18n(dp: Dispatcher):
    i18n = I18n(path="locales", domain="messages", default_locale="ru")
    middleware = DatabaseI18nMiddleware(i18n)
    dp.message.middleware.register(middleware)
    dp.message.outer_middleware(middleware)

