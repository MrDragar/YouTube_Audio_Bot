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
        if CHANNEL_ID == 0:
            return True
        member = await message.bot(
            GetChatMember(chat_id=CHANNEL_ID, user_id=message.from_user.id)
        )
        return isinstance(
            member,
            (
                ChatMemberMember,
                ChatMemberAdministrator,
                ChatMemberOwner,
                ChatMemberRestricted
            )
        )


class IsSubscriberCallbackFilter(Filter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if CHANNEL_ID == 0:
            return True
        member = await callback.bot(
            GetChatMember(chat_id=CHANNEL_ID, user_id=callback.from_user.id)
        )
        return isinstance(
            member,
            (
                ChatMemberMember,
                ChatMemberAdministrator,
                ChatMemberOwner,
                ChatMemberRestricted
            )
        )
