from abc import ABC, abstractmethod

from aiogram.handlers import MessageHandler
from aiogram.methods import SendMessage, EditMessageText
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.i18n import gettext as _

from bot.loader import bot


class BaseMessageCallbackMixin(MessageHandler, ABC):
    @abstractmethod
    async def send_callback(self):
        while True:
            yield


class AudioMassageCallbackMixin(BaseMessageCallbackMixin, ABC):
    async def send_callback(self):
        message = await self.bot(
            SendMessage(
                chat_id=self.chat.id,
                text=_("Сбор данных о аудио")
            )
        )
        yield
        message = await self.bot(
            EditMessageText(
                chat_id=self.chat.id,
                text=_("Скачивание аудио"),
                message_id=message.message_id
            )
        )
        yield
        async with ChatActionSender.upload_voice(bot=bot, chat_id=self.chat.id):
            await self.bot(
                EditMessageText(
                    chat_id=self.chat.id,
                    text=_("Отправление аудио"),
                    message_id=message.message_id
                )
            )
            yield


class VideoMassageCallbackMixin(BaseMessageCallbackMixin, ABC):
    async def send_callback(self):
        message = await self.bot(
            SendMessage(chat_id=self.chat.id, text=_("Сбор данных о видео"))
        )
        yield
        message = await self.bot(
            EditMessageText(
                chat_id=self.chat.id,
                text=_("Скачивание видео"),
                message_id=message.message_id
            )
        )
        yield
        async with ChatActionSender.upload_video(bot=bot, chat_id=self.chat.id):
            await self.bot(
                EditMessageText(
                    chat_id=self.chat.id,
                    text=_("Отправление видео"),
                    message_id=message.message_id
                )
            )
            yield
