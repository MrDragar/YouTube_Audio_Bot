from aiogram.dispatcher.router import Router
from aiogram.utils.i18n import lazy_gettext as __
from aiogram import F

from bot.states import VKState
from bot.utils.downloaders.vk import VKResolutionParser, YoutubeResolutionParser
from ..youtube.resolution import ShowResolutionsHandler as YoutubeHandler

resolution_router = Router()


@resolution_router.message(VKState.type, F.text == __("Видео"))
class ShowResolutionsHandler(YoutubeHandler):
    next_state = VKState.resolution.state
    Parser: YoutubeResolutionParser = VKResolutionParser


