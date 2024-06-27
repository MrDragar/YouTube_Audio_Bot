from typing import Any

from aiogram.dispatcher.router import Router
from aiogram.handlers import MessageHandler, CallbackQueryHandler
from aiogram.methods import SendMessage
from aiogram import F
from aiogram.utils.i18n import gettext as _

from bot.filters import IsSubscriberFilter, IsSubscriberCallbackFilter
from bot.keyboards import get_share_link_keyboard

subscribe_channel_router = Router()
subscribe_channel_router.message.filter(~IsSubscriberFilter())
subscribe_channel_router.callback_query.filter(~IsSubscriberFilter())


@subscribe_channel_router.message()
class ShareLinkHandler(MessageHandler):
    async def handle(self) -> Any:
        await self.bot(
            SendMessage(
                chat_id=self.chat.id,
                text=_(
                    "Для работы бота сперва необходимо подписаться на наш канал"),
                reply_markup=get_share_link_keyboard()
            )
        )


@subscribe_channel_router.callback_query(F.data == "check_subscribe")
class ShareLinkCallbackHandler(CallbackQueryHandler):
    async def handle(self) -> Any:
        await self.bot(
            SendMessage(
                chat_id=self.message.chat.id,
                text=_(
                    "Для работы бота сперва необходимо подписаться на наш канал"),
                reply_markup=get_share_link_keyboard()
            )
        )
