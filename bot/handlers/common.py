from typing import Any

from aiogram.dispatcher.router import Router
from aiogram.handlers import CallbackQueryHandler
from aiogram.methods import SendMessage
from aiogram.filters import Command
from aiogram import types
from aiogram.utils.i18n import lazy_gettext as __, gettext as _
from aiogram import F

from .base_handlers import StateMassageHandler

common_router = Router()


@common_router.message(Command("cancel"))
@common_router.message(F.text == __("Отмена"))
@common_router.message(F.text.lower() == __("отмена"))
class CancelHandler(StateMassageHandler):
    async def handle(self) -> Any:

        await self.bot(
            SendMessage(
                chat_id=self.chat.id, text=_("Отмена"),
                reply_markup=types.ReplyKeyboardRemove()
            )
        )
        await self.state.clear()


@common_router.message(Command("start", "help"))
class StartHandler(StateMassageHandler):
    async def handle(self) -> Any:
        await self.bot(
            SendMessage(
                chat_id=self.chat.id,
                text=_(
                    "Привет. С помощью этого бота ты можешь "
                    "скачать любое видео или аудио с Ютуба. "
                    "Для этого вам необходимо скинуть ссылку на этот ролик. "
                    "По всем вопросам пишите на yshhenyaev@mail.ru\n"
                    "Для смены языка пропишите /language \n"
                    "Если бот отправил вам сломанное видео или аудио, "
                    "перешлите боту это видео или аудио "
                    "и повторите скачивание."
                )
            )
        )


@common_router.callback_query(F.data == "check_subscribe")
class StartCallbackHandler(CallbackQueryHandler):
    async def handle(self) -> Any:
        await self.bot(
            SendMessage(
                chat_id=self.message.chat.id,
                text=_(
                    "Привет. С помощью этого бота ты можешь "
                    "скачать любое видео или аудио с Ютуба. "
                    "Для этого вам необходимо скинуть ссылку на этот ролик. "
                    "По всем вопросам пишите на yshhenyaev@mail.ru\n"
                    "Для смены языка пропишите /language \n"
                    "Если бот отправил вам сломанное видео или аудио, "
                    "перешлите боту это видео или аудио "
                    "и повторите скачивание."
                )
            )
        )
