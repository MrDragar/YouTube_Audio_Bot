from .vk import VKResolutionParser, VKDownloader
from bot.database.models import Platform


class RutubeResolutionParser(VKResolutionParser):
    ...


class RutubeDownloader(VKDownloader):
    platform = Platform.RUTUBE
