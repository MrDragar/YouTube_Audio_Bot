import logging

from aiogram.dispatcher.router import Router
from aiogram.methods import SendMessage
from aiogram.exceptions import TelegramEntityTooLarge


from bot.handlers.base_handlers import StateErrorHandler
from bot.utils.downloaders.youtube import ToBigVideo

error_router = Router()


@error_router.errors()
class YoutubeErrorHandler(StateErrorHandler):
    async def handle(self):
        await self.state.clear()
        if isinstance(self.event.exception, ToBigVideo) or \
                isinstance(self.event.exception, TelegramEntityTooLarge):
            await SendMessage(chat_id=self.event.update.message.chat.id,
                              text="Файл весит больше 2 ГБ")
        else:
            logging.exception(type(self.event.exception), self.exception_name,
                              self.exception_message)
            # print(type(self.event.exception))

