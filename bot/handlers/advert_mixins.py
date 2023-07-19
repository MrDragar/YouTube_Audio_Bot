from abc import ABC

from aiogram.handlers import MessageHandler
from aiogram.methods import CopyMessage, SendMessage

from bot.config import ADMINS_ID
from bot.database.advert import get_random_advert, add_current_number_to_advert


class AdvertMixin(MessageHandler, ABC):
    async def send_advert(self):
        advert = await get_random_advert()
        if not advert:
            return
        await CopyMessage(chat_id=self.chat.id, from_chat_id=advert.chat_id,
                          message_id=advert.message_id)
        if self.from_user.id in ADMINS_ID:
            full = await add_current_number_to_advert(advert.id)
            if full:
                for admin in ADMINS_ID:
                    await SendMessage(chat_id=admin,
                                      text="Реклама №{0} закончилась \n"
                                           "Набрано {1} просмотров"
                                      .format(advert.id, advert.total_number))
                    await CopyMessage(chat_id=admin,
                                      from_chat_id=advert.chat_id,
                                      message_id=advert.message_id)
