import logging

from aiogram.filters import Filter
from aiogram.types import Message, ChatMemberOwner, ChatMemberAdministrator, \
   CallbackQuery, ChatMemberMember, ChatMemberRestricted
from aiogram.methods import GetChatMember

from bot.config import ADMINS_ID, CHANNEL_ID


class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMINS_ID


class IsSubscriberFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        member = await GetChatMember(chat_id=CHANNEL_ID,
                                     user_id=message.from_user.id)
        return member.status in ['creator', 'administrator', 'member', 'restricted']
        return isinstance(member, (ChatMemberMember,
                                   ChatMemberAdministrator, ChatMemberOwner,
                                   ChatMemberRestricted))


class IsSubscriberCallbackFilter(Filter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        member = await GetChatMember(chat_id=CHANNEL_ID,
                                     user_id=callback.from_user.id)
        return member.status in ['creator', 'administrator', 'member', 'restricted']
        return isinstance(member, (ChatMemberMember,
                                   ChatMemberAdministrator, ChatMemberOwner,
                                   ChatMemberRestricted))
