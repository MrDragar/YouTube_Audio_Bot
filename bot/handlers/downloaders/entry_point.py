import re
import logging
from typing import Any

from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.utils.i18n import gettext as _
from aiogram.methods import SendMessage

from ..base_handlers import StateMassageHandler
from bot.states import YoutubeState, TiktokState, VKState, RutubeState
from bot.keyboards import get_type_keyboard
from bot.filters import IsSubscriberFilter

entry_point_router = Router()  # Должен быть в иерархии последним


@entry_point_router.message(IsSubscriberFilter())
class GetLinkHandler(StateMassageHandler):
    async def handle(self) -> Any:
        if not self.event.text:
            return SendMessage(chat_id=self.chat.id, text=_("Чё надо?"))
        urls = re.findall(r'http(?:s)?://\S+', self.event.text)
        if not urls:
            return SendMessage(chat_id=self.chat.id,
                               text=_("Нет ссылки в сообщении"),
                               reply_markup=types.ReplyKeyboardRemove)
        url = urls[0]
        if "tiktok" in url:
            await self.state.set_state(TiktokState.type)
            logging.debug("Tiktiok link")
        elif "youtube.com" in url or "youtu.be" in url:
            logging.debug("Youtube link")
            await self.state.set_state(YoutubeState.type)
        elif "vk.com" in url:
            logging.debug("VK link")
            await self.state.set_state(VKState.type)
        elif "rutube.ru" in url:
            logging.debug("Rutube link")
            await self.state.set_state(RutubeState.type)
        else:
            return SendMessage(chat_id=self.chat.id,
                               text=_("Данный сайт не поддерживается"),
                               reply_markup=types.ReplyKeyboardRemove)

        await self.state.update_data(url=url)
        return SendMessage(chat_id=self.chat.id, text=_("Выберите тип файла"),
                           reply_markup=get_type_keyboard())
