from typing import AsyncGenerator, Optional
import logging

from tiktok_downloader.tikwm import tikwm_async
from tiktok_downloader.mdown import mdown_async

from aiogram.types import FSInputFile

from bot.database.media import MediaType
import os


class TiktokVideo:
    path: Optional[str]
    type: MediaType

    def __call__(self, *args, **kwargs) -> FSInputFile:
        return FSInputFile(self.path)

    def __init__(self, type: MediaType, user_id: int, message_id: int) -> None:
        self.type = type
        self.path = f"video/{user_id}{message_id}." + \
                    ("mp4" if type == MediaType.VIDEO else "m4a")

    def __del__(self) -> None:
        if self.path:
            try:
                os.remove(path=self.path)
            except Exception as ex:
                if not isinstance(ex, FileNotFoundError):
                    logging.exception(ex)


class Downloader:
    def __init__(self, url: str, video: TiktokVideo,
                 callback: Optional[AsyncGenerator]):
        self._callback = callback
        self._url = url
        self._video = video

    async def send_callback(self):
        if self._callback:
            await self._callback.__anext__()

    async def run(self):
        await self.send_callback()

        if self._video.type == MediaType.VIDEO:
            d = await mdown_async(self._url)
            i = 0
        else:
            d = await tikwm_async(self._url)
            i = 2
        # print(d)
        await self.send_callback()
        await d[i].download(self._video.path)
        await self.send_callback()
