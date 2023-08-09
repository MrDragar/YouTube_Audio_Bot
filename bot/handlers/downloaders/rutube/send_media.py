from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.utils.i18n import lazy_gettext as __, gettext as _
from aiogram.methods import SendAudio, SendMessage, SendVideo

from bot.states import RutubeState

import bot.handlers.downloaders.youtube.send_media as youtube
from bot.utils.downloaders.rutube import RutubeDownloader

send_media_router = Router()


@send_media_router.message(RutubeState.type, F.text == __("Аудио"))
class SendAudioHandler(youtube.SendAudioHandler):
    SendMediaMethod = SendAudio
    Downloader = RutubeDownloader
    next_state = RutubeState.waiting.state

    async def handle(self):
        await SendMessage(chat_id=self.chat.id,
                          text=_("Эта функция не работает и нужна "
                                 "только ради красоты"))
        await self.state.clear()


@send_media_router.message(RutubeState.resolution)
class SendVideoHandler(youtube.SendVideoHandler):
    SendMediaMethod = SendVideo
    Downloader = RutubeDownloader
    next_state = RutubeState.waiting.state


