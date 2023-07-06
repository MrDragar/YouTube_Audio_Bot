from typing import Callable, Dict, Optional, AsyncGenerator
import asyncio
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
import logging

from yt_dlp import YoutubeDL

from bot.database.adapters import MediaAdapter


class TooBigVideo(Exception):
    ...


class Youtube(ABC):
    ydl_opts: dict = {"quiet": True}
    _callback: Optional[AsyncGenerator] = None

    async def send_callback(self):
        if self._callback:
            await self._callback.__anext__()

    async def _run(self, function: Callable):
        loop = asyncio.get_running_loop()

        """Запускает функцию в потоке"""
        with ThreadPoolExecutor() as pool:
            task = loop.run_in_executor(pool, function)
            results = await asyncio.gather(task)
            return results[0]

    @abstractmethod
    async def run(self):
        raise NotImplementedError


class YoutubeResolutionParser(Youtube):
    _url = None

    def __init__(self, url: str):
        self._url = url

    @staticmethod
    def check_format(format_: dict):
        return format_["video_ext"] == "mp4" and format_["audio_ext"] == "none"\
            and "filesize" in format_ and "format_note" in format_ \
            and format_["protocol"] == "https"

    def get_resolutions(self) -> Dict[str, str]:
        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(self._url, download=False)
            all_formats = ydl.sanitize_info(info)["formats"]
            video_resolutions = {}
            for format_ in all_formats:
                if self.check_format(format_):
                    video_resolutions[format_["format_note"]] = \
                        format_["format_id"]
            return video_resolutions

    async def run(self) -> Dict[str, str]:
        result = await self._run(self.get_resolutions)
        return result


class Downloader(Youtube):
    media_adapter: MediaAdapter

    def __init__(self, url: str, resolution: Optional[str] = "",
                 callback: Optional[AsyncGenerator] = None):
        self._url = url
        self._resolution = resolution
        self._callback = callback
        self.ydl_opts["format"] = (resolution + "+") if resolution else ""
        self.ydl_opts["format"] += "bestaudio[ext=m4a]"
        self.ydl_opts['outtmpl'] = f'video/%(title)s {resolution}.%(ext)s'

    @staticmethod
    def check_size(size):
        return size / 1000 / 1000 / 1000 < 2

    def collect_information(self):
        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(self._url, download=False)
            # размер указан в байтах
            size = info.get("filesize_approx", info.get('filesize', None))
            if not self.check_size(size):
                raise TooBigVideo
            self.media_adapter = MediaAdapter(info["id"], self._resolution)

    def download(self):
        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(self._url, download=True)
            file_path = ydl.prepare_filename(info)
            self.media_adapter.set_file_path(file_path)

    async def get_media_adapter(self) -> MediaAdapter:
        # Смотрим, есть ли запрашенное видео в базе данных
        await self.send_callback()
        await self._run(self.collect_information)
        if self.media_adapter.is_on_server():
            return self.media_adapter
        await self.send_callback()
        await self._run(self.download)
        await self.send_callback()
        return self.media_adapter

    async def run(self) -> MediaAdapter:
        return await self.get_media_adapter()


async def main():
    ...
    # url = "https://www.youtube.com/watch?v=2ya7I81xKl8"
    # parser = YoutubeResolutionParser(url=url)
    # print(await parser.run())
    # URL = "https://www.youtube.com/watch?v=2ya7I81xKl8"
    # downloader = Downloader(url=URL, resolution="160")
    # await downloader.run()


if __name__ == "__main__":
    asyncio.run(main())
