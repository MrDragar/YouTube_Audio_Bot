import re
import abc
import logging
from typing import Any

from aiogram import types, F
from aiogram.dispatcher.router import Router
from aiogram.utils.i18n import gettext as _
from aiogram.methods import SendMessage

from ..base_handlers import StateMassageHandler
from bot.states import YoutubeState, TiktokState, VKState, RutubeState
from bot.keyboards import get_type_keyboard
from bot.database.media import delete_media

entry_point_router = Router()  # Должен быть в иерархии последним


@entry_point_router.message(YoutubeState.waiting)
@entry_point_router.message(TiktokState.waiting)
@entry_point_router.message(VKState.waiting)
@entry_point_router.message(RutubeState.waiting)
async def waiting_handler(message: types.Message):
    await message.answer(_("Да подогоди ты, я занят твоим предыдущим видео"))


class DeleteMedia(StateMassageHandler, abc.ABC):
    @abc.abstractmethod
    def get_file_unique_id(self) -> str:
        raise NotImplementedError

    async def handle(self):
        logging.debug(self.event)
        error = await delete_media(self.get_file_unique_id())
        if error:
            await self.bot(
                SendMessage(
                    chat_id=self.chat.id,
                    text=_("Ошибка, такого файла нет в базе данных")
                )
            )
            return
        await self.bot(
            SendMessage(
                chat_id=self.chat.id,
                text=_("Видео успешно удалено, можете скачать его заново")
                )
        )


@entry_point_router.message(F.video)
class DeleteVideo(DeleteMedia):
    def get_file_unique_id(self) -> str:
        return self.event.video.file_unique_id


@entry_point_router.message(F.audio)
class DeleteAudio(DeleteMedia):
    def get_file_unique_id(self) -> str:
        return self.event.audio.file_unique_id


@entry_point_router.message()
class GetLinkHandler(StateMassageHandler):
    async def handle(self) -> Any:
        if not self.event.text:
            return await self.bot(
                SendMessage(chat_id=self.chat.id, text=_("Чё надо?"))
            )
        urls = re.findall(r'http(?:s)?://\S+', self.event.text)
        if not urls:
            return await self.bot(
                SendMessage(
                    chat_id=self.chat.id,
                    text=_("Нет ссылки в сообщении"),
                    reply_markup=types.ReplyKeyboardRemove()
                )
            )
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
            return await self.bot(
                SendMessage(
                    chat_id=self.chat.id,
                    text=_("Данный сайт не поддерживается"),
                    reply_markup=types.ReplyKeyboardRemove())
            )

        await self.state.update_data(url=url)
        return await self.bot(
            SendMessage(
                chat_id=self.chat.id, text=_("Выберите тип файла"),
                reply_markup=get_type_keyboard()
            )
        )
