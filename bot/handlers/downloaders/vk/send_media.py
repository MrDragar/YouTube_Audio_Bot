from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.utils.i18n import lazy_gettext as __, gettext as _
from aiogram.methods import SendAudio, SendMessage, SendVideo

from bot.states import VKState

import bot.handlers.downloaders.youtube.send_media as youtube
from bot.utils.downloaders.vk import VKDownloader

send_media_router = Router()


@send_media_router.message(VKState.type, F.text == __("Аудио"))
class SendAudioHandler(youtube.SendAudioHandler):
    SendMediaMethod = SendAudio
    Downloader = VKDownloader
    next_state = VKState.waiting.state


@send_media_router.message(VKState.resolution)
class SendVideoHandler(youtube.SendVideoHandler):
    SendMediaMethod = SendVideo
    Downloader = VKDownloader
    next_state = VKState.waiting.state
