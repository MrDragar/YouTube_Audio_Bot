from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.utils.i18n import lazy_gettext as __, gettext as _
from aiogram.methods import SendAudio

from bot.handlers.base_handlers import StateMassageHandler
from bot.states import YoutubeState
from bot.utils.downloaders.youtube import Downloader


send_media_router = Router()


@send_media_router.message(YoutubeState.type, F.text == __("Аудио"))
class SendAudioHandler(StateMassageHandler):
    async def handle(self):
        data = await self.state.get_data()
        downloader = Downloader(data["url"])
        media_adapter = await downloader.run()
        audio_info = await SendAudio(chat_id=self.chat.id,
                                     audio=media_adapter())
        await media_adapter.set_file_id(audio_info.audio.file_id)
        await self.state.clear()
