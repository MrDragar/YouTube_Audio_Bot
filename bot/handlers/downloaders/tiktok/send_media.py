from abc import ABC
from typing import Union

from aiogram.utils.i18n import lazy_gettext as __
from aiogram.dispatcher.router import Router
from aiogram.methods import SendAudio, SendVideo, SendMessage, DeleteMessage
from aiogram import F
from aiogram.types import ReplyKeyboardRemove

from bot.handlers.base_handlers import StateMassageHandler
from bot.handlers.callback_mixins import BaseMessageCallbackMixin, \
    VideoMassageCallbackMixin, AudioMassageCallbackMixin
from bot.utils.downloaders.tiktok import Downloader, TiktokVideo
from bot.database.models import MediaType
from bot.states import TiktokState
from bot.database.day_statistic import add_successful_request
from bot.handlers.advert_mixins import AdvertMixin

send_media_router = Router()


class SendTiktokMedia(AdvertMixin, StateMassageHandler,
                      BaseMessageCallbackMixin, ABC):
    type: MediaType
    SendMediaMethod: Union[SendVideo.__class__, SendAudio.__class__]
    next_state = TiktokState.waiting.state

    async def handle(self):
        data = await self.state.get_data()
        url = data["url"]
        await self.state.set_state(self.next_state)
        media = TiktokVideo(self.type, self.chat.id, self.event.message_id)

        message = await self.bot(
            SendMessage(
                chat_id=self.chat.id,
                text="Удаление клавиатуры",
                disable_notification=True,
                reply_markup=ReplyKeyboardRemove()
            )
        )
        await self.bot(
            DeleteMessage(chat_id=self.chat.id, message_id=message.message_id)
        )

        callback = self.send_callback()
        downloader = Downloader(url, media, callback=callback)
        await downloader.run()
        kwargs = {
            "chat_id": self.chat.id,
            "supports_streaming": True,
            self.type.value: media(),
            "reply_markup": ReplyKeyboardRemove()
        }
        await self.bot(self.SendMediaMethod(**kwargs))
        await callback.aclose()
        del media
        await add_successful_request()
        await self.state.clear()
        await self.send_advert()


@send_media_router.message(TiktokState.type, F.text == __("Аудио"))
class SendTiktokAudio(SendTiktokMedia, AudioMassageCallbackMixin):
    type = MediaType.AUDIO
    SendMediaMethod = SendAudio


@send_media_router.message(TiktokState.type, F.text == __("Видео"))
class SendTiktokVideo(SendTiktokMedia, VideoMassageCallbackMixin):
    type = MediaType.VIDEO
    SendMediaMethod = SendVideo
