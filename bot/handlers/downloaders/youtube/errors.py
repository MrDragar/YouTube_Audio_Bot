import logging

from aiogram.dispatcher.router import Router
from aiogram.methods import SendMessage
from aiogram.exceptions import TelegramEntityTooLarge
from yt_dlp.utils import DownloadError
from aiogram.utils.i18n import gettext as _

from bot.handlers.base_handlers import StateErrorHandler
from bot.utils.downloaders.youtube import ToBigVideo

error_router = Router()


@error_router.errors()
class YoutubeErrorHandler(StateErrorHandler):
    async def handle(self):
        await self.state.clear()
        if isinstance(self.event.exception, ToBigVideo) or \
                isinstance(self.event.exception, TelegramEntityTooLarge):
            return SendMessage(chat_id=self.event.update.message.chat.id,
                               text=_("Файл весит больше 2 ГБ", locale="ru"))
        if isinstance(self.event.exception, DownloadError):
            if "This video contains content from SME, who has blocked it in " \
               "your country on copyright grounds" in self.event.exception.msg:
                return SendMessage(chat_id=self.event.update.message.chat.id,
                                   text=_("Видео заблокировано в РФ"))
            if "Video unavailable" in self.event.exception.msg:
                return SendMessage(chat_id=self.event.update.message.chat.id,
                                   text=_("Видео недоступно для скачивания"))
            if "Unable to download API page: HTTP Error 404" \
                    in self.event.exception.msg:
                return SendMessage(chat_id=self.event.update.message.chat.id,
                                   text=_("Видео недоступно для скачивания."
                                          " Ошибка 404"))

            logging.exception(self.event.exception)
            logging.info(type(self.event.exception))
            return SendMessage(chat_id=self.event.update.message.chat.id,
                               text=_("Произошла какая-та ошибка при"
                                      " скачивании видео"))

        logging.exception(self.event.exception)
        logging.info(type(self.event.exception))
        return SendMessage(chat_id=self.event.update.message.chat.id,
                           text=_("Произошла какая-то ошибка (никто не"
                                  " знает, из-за чего она произошла)"))
