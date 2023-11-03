import logging

from aiogram.dispatcher.router import Router
from aiogram.methods import SendMessage
from aiogram.exceptions import TelegramEntityTooLarge, TelegramNetworkError
from yt_dlp.utils import DownloadError
from aiogram.utils.i18n import gettext as _
from httpx import ReadTimeout
from requests.exceptions import InvalidURL

from bot.handlers.base_handlers import StateErrorHandler
from bot.utils.downloaders.youtube import TooBigVideo, PlaylistError
from bot.database.day_statistic import add_unsuccessful_request
from bot.loader import bot

error_router = Router()


@error_router.errors()
class YoutubeErrorHandler(StateErrorHandler):
    async def handle(self):
        await self.state.clear()
        if isinstance(self.event.exception, TooBigVideo) or \
                isinstance(self.event.exception, TelegramEntityTooLarge):
            return SendMessage(chat_id=self.event.update.message.chat.id,
                               text=_("Файл весит больше 2 ГБ"))
        if isinstance(self.event.exception, PlaylistError):
            return SendMessage(chat_id=self.event.update.message.chat.id,
                               text=_("Плейлисты не поддерживаются"))

        if isinstance(self.event.exception, DownloadError):
            if "This video contains content from SME, who has blocked it in " \
               "your country on copyright grounds" in self.event.exception.msg:
                return SendMessage(chat_id=self.event.update.message.chat.id,
                                   text=_("Видео заблокировано в РФ"))
            if "The uploader has not made this video available in your country"\
                    in self.event.exception.msg:
                return SendMessage(chat_id=self.event.update.message.chat.id,
                                   text=_("Видео заблокировано в РФ"))
            if "Video unavailable" in self.event.exception.msg:
                print(self.event.exception.msg)
                return SendMessage(chat_id=self.event.update.message.chat.id,
                                   text=_("Видео недоступно для скачивания"))
            if "Unable to download API page: HTTP Error 404" \
                    in self.event.exception.msg:
                return SendMessage(chat_id=self.event.update.message.chat.id,
                                   text=_("Видео недоступно для скачивания."
                                          " Ошибка 404"))
            if "Name or service not known>" in self.event.exception.msg:
                return SendMessage(chat_id=self.event.update.message.chat.id,
                                   text=_("Некорректная ссылка"))
            if "Requested format is not available." in self.event.exception.msg:
                return SendMessage(chat_id=self.event.update.message.chat.id,
                                   text=_("Ошибка с форматом видео. Пожалуйста,"
                                          " сообщите админам об этой ошибку"))
            if "ERROR: Unable to rename file" in self.event.exception.msg:
                return SendMessage(chat_id=self.event.update.message.chat.id,
                                   text=_("Ошибка из-за того, что это видео "
                                          "сейчас кто-то скачивал. "
                                          "Пожалуйста, повторите попытку "
                                          "через 5 минут."))

            await add_unsuccessful_request()
            logging.exception(self.event.exception)
            logging.info(type(self.event.exception))
            return SendMessage(chat_id=self.event.update.message.chat.id,
                               text=_("Произошла какая-та ошибка при"
                                      " скачивании видео. Сообщите админам"))

        if isinstance(self.event.exception, ReadTimeout) or \
                isinstance(self.event.exception, InvalidURL):
            return SendMessage(chat_id=self.event.update.message.chat.id,
                               text=_("Некорректная ссылка"))

        if isinstance(self.event.exception, TelegramNetworkError):
            if "Telegram server says ClientOSError: [Errno 2]" \
               " Can not write request body " in self.event.exception.message:
                return SendMessage(chat_id=self.event.update.message.chat.id,
                                   text=_("Ошибка из-за того, что это видео "
                                          "сейчас кто-то скачивал. "
                                          "Пожалуйста, повторите попытку "
                                          "через 5 минут."))
            logging.info(self.event.exception.message)
            return SendMessage(chat_id=self.event.update.message.chat.id,
                               text=_("Ошибка из-за того, что это видео "
                                      "сейчас кто-то скачивал. "
                                      "Пожалуйста, повторите попытку "
                                      "через 5 минут."))
        if isinstance(self.event.exception, IndexError):
            return SendMessage(chat_id=self.event.update.message.chat.id,
                               text=_("Данный формат видео не поддерживается"))

        await add_unsuccessful_request()
        logging.exception(self.event.exception)
        logging.info(type(self.event.exception))
        return SendMessage(chat_id=self.event.update.message.chat.id,
                           text=_("Произошла какая-то ошибка (никто не"
                                  " знает, из-за чего она произошла). "
                                  "Сообщите админам"))
