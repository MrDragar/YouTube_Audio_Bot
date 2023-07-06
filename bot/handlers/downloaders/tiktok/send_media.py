from abc import ABC
from typing import Union

from aiogram.utils.i18n import lazy_gettext as __
from aiogram.dispatcher.router import Router
from aiogram.methods import SendAudio, SendVideo
from aiogram import F
from aiogram.types import ReplyKeyboardRemove

from bot.handlers.base_handlers import StateMassageHandler, \
    AudioMassageHandlerCallback, VideoMassageHandlerCallback, \
    BaseMessageHandlerCallback
from bot.utils.downloaders.tiktok import Downloader, TiktokVideo
from bot.database.models import MediaType
from bot.states import TiktokState
from bot.database.day_statistic import add_successful_request


send_media_router = Router()


class SendTiktokMedia(StateMassageHandler, BaseMessageHandlerCallback, ABC):
    type: MediaType
    SendMediaMethod: Union[SendVideo.__class__, SendAudio.__class__]

    async def handle(self):
        data = await self.state.get_data()
        url = data["url"]
        media = TiktokVideo(self.type, self.chat.id, self.event.message_id)
        downloader = Downloader(url, media, self.send_callback())
        await downloader.run()
        kwargs = {"chat_id": self.chat.id,
                  self.type.value: media(),
                  "reply_markup": ReplyKeyboardRemove()
                  }
        await self.SendMediaMethod(**kwargs)
        del media
        await add_successful_request()
        await self.state.clear()


@send_media_router.message(TiktokState.type, F.text == __("Аудио"))
class SendTiktokAudio(SendTiktokMedia, AudioMassageHandlerCallback):
    type = MediaType.AUDIO
    SendMediaMethod = SendAudio


@send_media_router.message(TiktokState.type, F.text == __("Видео"))
class SendTiktokVideo(SendTiktokMedia, VideoMassageHandlerCallback):
    type = MediaType.VIDEO
    SendMediaMethod = SendVideo