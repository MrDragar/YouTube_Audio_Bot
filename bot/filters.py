from aiogram.filters import Filter
from aiogram.types import Message, ChatMemberOwner, ChatMemberAdministrator, \
    ChatMemberRestricted
from aiogram.methods import GetChatMember

from bot.config import ADMINS_ID, CHANNEL_ID


class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMINS_ID


class IsSubscriberFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        member = await GetChatMember(chat_id=CHANNEL_ID,
                                     user_id=message.from_user.id)
        return member in (ChatMemberRestricted, ChatMemberAdministrator,
                          ChatMemberOwner)
