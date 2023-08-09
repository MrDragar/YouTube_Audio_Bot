from aiogram.dispatcher.router import Router
from aiogram.utils.i18n import lazy_gettext as __
from aiogram import F

from bot.states import RutubeState
from bot.utils.downloaders.rutube import RutubeResolutionParser
from ..youtube.resolution import ShowResolutionsHandler as YoutubeHandler

resolution_router = Router()


@resolution_router.message(RutubeState.type, F.text == __("Видео"))
class ShowResolutionsHandler(YoutubeHandler):
    next_state = RutubeState.resolution.state
    Parser = RutubeResolutionParser


