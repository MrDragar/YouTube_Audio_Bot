import re
import logging
from typing import Any

from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.utils.i18n import gettext as _
from aiogram.methods import SendMessage
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ButtonType

from ..base_handlers import StateMassageHandler
from bot.states import YoutubeState
from bot.keyboards import get_type_keyboard


entry_point_router = Router()


@entry_point_router.message()
class GetLinkHandler(StateMassageHandler):
    async def handle(self) -> Any:
        urls = re.findall(r'http(?:s)?://\S+', self.event.text)
        if not urls:
            return SendMessage(chat_id=self.chat.id,
                               text=_("Нет ссылки в сообщении"),
                               reply_markup=types.ReplyKeyboardRemove)
        url = urls[0]
        if "tiktok" in url:
            logging.info("Tiktiok link")
        elif "youtube.com" in url or "youtu.be" in url:
            logging.info("Youtube link")
            await self.state.set_state(YoutubeState.type)
        else:
            return SendMessage(chat_id=self.chat.id,
                               text=_("Данный сайт не поддерживается"),
                               reply_markup=types.ReplyKeyboardRemove)

        await self.state.update_data(url=url)
        return SendMessage(chat_id=self.chat.id, text=_("Выберите тип файла"),
                           reply_markup=get_type_keyboard())

