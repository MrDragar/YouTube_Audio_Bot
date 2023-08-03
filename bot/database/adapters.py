import logging
from typing import Optional
import asyncio
import os

from aiogram.types import FSInputFile

from .models import Media, MediaType, Platform
from .media import get_media, create_media


class MediaAdapter:
    """Это адаптер модели Media для отправки его в телеграм чат"""
    _media: Media
    _file_path: Optional[str] = None
    _on_server: bool = False

    def __init__(self, link_id: str, platform: Platform,
                 resolution: Optional[str] = None) -> None:
        self._type = MediaType.VIDEO if resolution else MediaType.AUDIO
        self._link_id = link_id
        self._resolution = resolution
        self._platform = platform

    async def get_media(self):
        self._media = await get_media(link_id=self._link_id, type=self._type,
                                      resolution=self._resolution,
                                      platform=self._platform)
        if self._media:
            self._on_server = self._media.file_id is not None
        else:
            self._media = await create_media(link_id=self._link_id,
                                             type=self._type,
                                             resolution=self._resolution,
                                             platform=self._platform)

    def is_on_server(self) -> bool:
        return self._on_server

    def set_file_path(self, file_path: str) -> None:
        self._file_path = file_path

    async def set_file_id(self, file_id: str) -> None:
        self._media.file_id = file_id
        await self._media.save()

    def __call__(self) -> FSInputFile:
        if self.is_on_server():
            return self._media.file_id
        else:
            return FSInputFile(self._file_path)

    def __del__(self) -> None:
        if self.is_on_server():
            return
        if self._file_path:
            try:
                os.remove(self._file_path)
            except Exception as ex:
                logging.info(ex)

    def get_media_type(self) -> MediaType:
        return self._media.type
