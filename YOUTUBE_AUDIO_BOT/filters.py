from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from YOUTUBE_AUDIO_BOT.config import admins_id, channel_chat_id, bot


class MyFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        return str(message.from_user.id) in admins_id


class IsSubscriberFilter(BoundFilter):
    key = "is_subscriber"

    def __init__(self, is_subscriber):
        self.is_subscriber = is_subscriber

    async def check(self, message: types.Message):
        user = await bot.get_chat_member(channel_chat_id, message.from_user.id)
        return user.status not in (types.ChatMemberStatus.LEFT, types.ChatMemberStatus.KICKED,
                                   types.ChatMemberStatus.BANNED) == self.is_subscriber


def register_filters(dp):
    dp.filters_factory.bind(MyFilter)
    dp.filters_factory.bind(IsSubscriberFilter)
