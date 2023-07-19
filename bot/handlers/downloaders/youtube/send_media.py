from abc import ABC, abstractmethod
from typing import Union, Optional, Tuple

from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.i18n import lazy_gettext as __, gettext as _
from aiogram.methods import SendAudio, SendMessage, SendVideo

from bot.handlers.base_handlers import StateMassageHandler
from bot.handlers.callback_mixins import BaseMessageCallbackMixin, \
    VideoMassageCallbackMixin, AudioMassageCallbackMixin
from bot.states import YoutubeState
from bot.utils.downloaders.youtube import Downloader
from bot.database.day_statistic import add_successful_request
from bot.handlers.advert_mixins import AdvertMixin


send_media_router = Router()


class SendMediaHandler(AdvertMixin, BaseMessageCallbackMixin,
                       StateMassageHandler, ABC):
    SendMediaMethod: Union[SendVideo.__class__, SendAudio.__class__]

    @abstractmethod
    async def get_resolution(self) -> Tuple[Optional[str], bool]:
        raise NotImplementedError

    @abstractmethod
    def get_file_id(self, info) -> str:
        raise NotImplementedError

    async def handle(self):
        data = await self.state.get_data()
        resolution, error = await self.get_resolution()
        if error:
            return
        downloader = Downloader(data["url"], resolution,
                                callback=self.send_callback())
        media_adapter = await downloader.run()
        kwargs = {"chat_id": self.chat.id,
                  media_adapter.get_media_type().value: media_adapter(),
                  "supports_streaming": True,
                  "width": 256,
                  "height": 144,
                  "reply_markup": ReplyKeyboardRemove()
                  }

        media_info = await self.SendMediaMethod(**kwargs)
        await media_adapter.set_file_id(self.get_file_id(media_info))
        del media_adapter
        await add_successful_request()
        await self.state.clear()
        await self.send_advert()


@send_media_router.message(YoutubeState.type, F.text == __("Аудио"))
class SendAudioHandlerMixin(AudioMassageCallbackMixin, SendMediaHandler):
    SendMediaMethod = SendAudio

    async def get_resolution(self) -> Tuple[Optional[str], bool]:
        return None, False

    def get_file_id(self, info) -> str:
        return info.audio.file_id


@send_media_router.message(YoutubeState.resolution)
class SendVideoHandlerMixin(VideoMassageCallbackMixin, SendMediaHandler):
    SendMediaMethod = SendVideo

    async def get_resolution(self) -> Tuple[Optional[str], bool]:
        data = await self.state.get_data()
        if self.event.text.strip() not in data["resolution"].keys():
            await SendMessage(chat_id=self.chat.id,
                              text=_("Неверное расширение"))
            return None, True
        return data["resolution"][self.event.text.strip()], False

    def get_file_id(self, info) -> str:
        return info.video.file_id
