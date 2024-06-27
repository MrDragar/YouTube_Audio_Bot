import logging

from aiogram.dispatcher.router import Router
from aiogram.utils.i18n import lazy_gettext as __, gettext as _
from aiogram import F
from aiogram.methods import SendMessage, SendChatAction

from bot.handlers.base_handlers import StateMassageHandler
from bot.states import YoutubeState
from bot.utils.downloaders.youtube import YoutubeResolutionParser
from bot.keyboards import get_resolution_keyboard

resolution_router = Router()


@resolution_router.message(YoutubeState.type, F.text == __("Видео"))
class ShowResolutionsHandler(StateMassageHandler):
    next_state = YoutubeState.resolution.state
    Parser: YoutubeResolutionParser.__class__ = YoutubeResolutionParser

    async def handle(self):
        await self.bot(SendChatAction(chat_id=self.chat.id, action=_("typing")))
        data = await self.state.get_data()
        parser = self.Parser(data["url"])
        resolutions = await parser.run()
        await self.bot(
            SendMessage(
                chat_id=self.chat.id, text=_("Выберите разрешение"),
                reply_markup=get_resolution_keyboard(resolutions)
            )
        )
        await self.state.update_data(resolution=resolutions)
        await self.state.set_state(self.next_state)
