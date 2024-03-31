import re
import logging
from typing import Any

from aiogram import types, F
from aiogram.dispatcher.router import Router
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.methods import SendMessage

from ..base_handlers import StateMassageHandler
from bot.states import YoutubeState, TiktokState, VKState, RutubeState, JokeState
from bot.keyboards import get_type_keyboard, get_joke_keyboard
from bot.filters import IsSubscriberFilter

entry_point_router = Router()  # Должен быть в иерархии последним


@entry_point_router.message(YoutubeState.waiting)
@entry_point_router.message(TiktokState.waiting)
@entry_point_router.message(VKState.waiting)
@entry_point_router.message(RutubeState.waiting)
async def waiting_handler(message: types.Message):
    await message.answer(_("Да подогоди ты, я занят твоим предыдущим видео"))


@entry_point_router.message(F.text == "Купить подписку", JokeState.step1)
class JokeHandler2(StateMassageHandler):
    async def handle(self) -> Any:
        await self.bot(
            SendMessage(
                chat_id=self.chat.id,
                text=_('Админ стал богаче на 0 рублей, теперь можете отправить мне ссылку на видео'),
                reply_markup=types.ReplyKeyboardRemove()
            )
        )
        await self.state.set_state(JokeState.step2)


@entry_point_router.message(F.text == "Админ лох", JokeState.step1)
class JokeHandler2(StateMassageHandler):
    async def handle(self) -> Any:
        await self.bot(
            SendMessage(
                chat_id=self.chat.id,
                text=_('Админ стал беднее на 0 рублей, теперь ты можешь отправить мне ссылку на видео'),
                reply_markup=types.ReplyKeyboardRemove()
            )
        )
        await self.state.set_state(JokeState.step2)


@entry_point_router.message(JokeState.step2)
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


@entry_point_router.message()
class JokeHandler(StateMassageHandler):
    async def handle(self) -> Any:
        await self.bot(
            SendMessage(
                chat_id=self.chat.id,
                text=_('Для продолжения работы бота купите подписку'),
                reply_markup=get_joke_keyboard()
            )
        )
        await self.state.set_state(JokeState.step1)

