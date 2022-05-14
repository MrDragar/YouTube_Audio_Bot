from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from YOUTUBE_AUDIO_BOT.config import admins_id


class MyFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        return str(message.from_user.id) in admins_id


def register_filters(dp):
    dp.filters_factory.bind(MyFilter)
