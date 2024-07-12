import asyncio
import os.path
import random
import shutil
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Dict, Optional, AsyncGenerator

from yt_dlp import YoutubeDL
from yt_dlp.networking import Request
from yt_dlp.networking.exceptions import network_exceptions

from bot.config import BROWSERS
from bot.database.adapters import MediaAdapter
from bot.database.models import Platform


class TooBigVideo(Exception):
    ...


class PlaylistError(Exception):
    ...


class Youtube(ABC):
    ydl_opts: dict = {
        "quiet": True,
        "noplaylist": True,
        "no_warnings": True
    }
    _callback: Optional[AsyncGenerator] = None

    def __init__(self):
        if BROWSERS:
            self.ydl_opts["cookiesfrombrowser"] = (random.choice(BROWSERS))

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
    resolution_name = "format_note"

    def __init__(self, url: str):
        super().__init__()
        self._url = url

    @staticmethod
    def check_format(format_: dict):
        return (
                format_["video_ext"] == "mp4"
                and "filesize" in format_ and "format_note" in format_
                and format_["protocol"] == "https"
        )

    def get_resolutions(self) -> Dict[str, str]:
        with YoutubeDL(self.ydl_opts) as ydl:
            ydl.format_selector = None
            info = ydl.extract_info(self._url, download=False)
            if "entries" in info:
                raise PlaylistError
            all_formats = ydl.sanitize_info(info)["formats"]
            video_resolutions = {}
            for format_ in all_formats:
                if self.check_format(format_):
                    if format_[self.resolution_name] not in video_resolutions:
                        video_resolutions[format_[self.resolution_name]] = \
                            format_["format_id"]
                    elif "asr" not in format_ or format_["asr"] is not None:
                        video_resolutions[format_[self.resolution_name]] = \
                            format_["format_id"]
            return video_resolutions

    async def run(self) -> Dict[str, str]:
        result = await self._run(self.get_resolutions)
        return result


class YoutubeDownloader(Youtube):
    media_adapter: MediaAdapter
    platform: Platform = Platform.YOUTUBE

    # proxy: str = "socks://127.0.0.1:8888"

    def __init__(self, url: str, resolution: Optional[str] = "",
                 callback: Optional[AsyncGenerator] = None):
        super().__init__()
        self._url = url
        self._resolution = resolution
        self._callback = callback
        self.ydl_opts["merge_output_format"] = "mp4"
        # self.ydl_opts["writethumbnail"] = True
        self.ydl_opts["format"] = f"{resolution + '+'}" if resolution else ""
        self.ydl_opts["format"] += "bestaudio[ext=m4a]"
        self.ydl_opts['outtmpl'] = {'default': 'video/%(title).40s.%(ext)s'}
        # self.ydl_opts["proxy"] = self.proxy

    @staticmethod
    def check_size(size):
        return size / 1000 / 1000 / 1000 < 2

    def collect_information(self):
        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(self._url, download=False)
            if "entries" in info:
                raise PlaylistError
            # размер указан в байтах
            size = info.get("filesize_approx", info.get('filesize', None))
            if not self.check_size(size):
                raise TooBigVideo
            self.media_adapter = MediaAdapter(info["id"],
                                              platform=self.platform,
                                              resolution=self._resolution)

    def _download_thumbnail(self, info: dict, video_path: str,
                            ydl: YoutubeDL) -> Optional[str]:
        thumbnails = info.get('thumbnails') or []
        for idx, t in list(enumerate(thumbnails))[::-1]:
            url: str = t.get("url", None)
            if url is None:
                continue
            if not (t.get("height", 321) <= 320 and t.get("width") <= 321):
                continue
            filepath = os.path.splitext(video_path)[0] + ".jpg"
            try:
                uf = ydl.urlopen(
                    Request(t['url'], headers=t.get('http_headers', {})))
                with open(filepath, 'wb') as thumbf:
                    shutil.copyfileobj(uf, thumbf)
            except network_exceptions as err:
                continue
            return filepath

    def download(self):
        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(self._url, download=True)
            file_path = ydl.prepare_filename(info)
            self.media_adapter.set_thumbnail_path(
                self._download_thumbnail(info, file_path, ydl),
            )
            self.media_adapter.set_file_path(file_path)

    async def get_media_adapter(self) -> MediaAdapter:
        # Смотрим, есть ли запрашенное видео в базе данных
        await self.send_callback()
        await self._run(self.collect_information)
        await self.media_adapter.get_media()
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
