from abc import ABC

from aiogram.handlers import MessageHandler
from aiogram.methods import CopyMessage, SendMessage

from bot.config import ADMINS_ID
from bot.database.advert import get_random_advert, add_current_number_to_advert


class AdvertMixin(MessageHandler, ABC):
    async def send_advert(self):
        if self.from_user.id in ADMINS_ID:
            return

        advert = await get_random_advert()
        if not advert:
            return

        await self.bot(
            CopyMessage(
                chat_id=self.chat.id, from_chat_id=advert.chat_id,
                message_id=advert.message_id
            )
        )
        full = await add_current_number_to_advert(advert.id)

        if not full:
            return
        for admin in ADMINS_ID:
            await self.bot(
                SendMessage(
                    chat_id=admin,
                    text="Реклама №{0} закончилась \n Набрано {1} просмотров"
                    .format(advert.id, advert.total_number)
                )
            )
            await self.bot(
                CopyMessage(
                    chat_id=self.chat.id, from_chat_id=advert.chat_id,
                    message_id=advert.message_id
                )
            )
