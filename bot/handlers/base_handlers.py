from abc import ABC, abstractmethod

from aiogram.handlers import MessageHandler, ErrorHandler
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage, EditMessageText
from aiogram.types import Message, error_event, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _
from aiogram.utils.chat_action import ChatActionSender

from bot.loader import bot


class StateMassageHandler(MessageHandler, ABC):
    state: FSMContext
    event: Message

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = self.data["state"]


class StateErrorHandler(ErrorHandler, ABC):
    state: FSMContext
    event: error_event.ErrorEvent

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = self.data["state"]


class BaseMessageHandlerCallback(MessageHandler, ABC):
    @abstractmethod
    async def send_callback(self):
        while True:
            yield


class AudioMassageHandlerCallback(BaseMessageHandlerCallback, ABC):
    async def send_callback(self):
        message = await SendMessage(chat_id=self.chat.id,
                                    text=_("Сбор данных о аудио"),
                                    reply_markup=ReplyKeyboardRemove())
        yield
        message = await EditMessageText(chat_id=self.chat.id,
                                        text=_("Скачивание аудио"),
                                        message_id=message.message_id)
        yield
        async with ChatActionSender.upload_voice(bot=bot, chat_id=self.chat.id):
            await EditMessageText(chat_id=self.chat.id,
                                  text=_("Отправление аудио"),
                                  message_id=message.message_id)
            yield


class VideoMassageHandlerCallback(BaseMessageHandlerCallback, ABC):
    async def send_callback(self):
        message = await SendMessage(chat_id=self.chat.id,
                                    text=_("Сбор данных о видео"),
                                    reply_murkup=ReplyKeyboardRemove())
        yield
        message = await EditMessageText(chat_id=self.chat.id,
                                        text=_("Скачивание видео"),
                                        message_id=message.message_id)
        yield
        async with ChatActionSender.upload_video(bot=bot, chat_id=self.chat.id):
            await EditMessageText(chat_id=self.chat.id,
                                  text=_("Отправление видео"),
                                  message_id=message.message_id)
            yield
