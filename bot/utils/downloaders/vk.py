from typing import Optional, AsyncGenerator

from yt_dlp import YoutubeDL

from .youtube import YoutubeResolutionParser, YoutubeDownloader, PlaylistError, \
    TooBigVideo
from ...database.adapters import MediaAdapter
from ...database.models import Platform


class VKResolutionParser(YoutubeResolutionParser):
    resolution_name = "resolution"

    def __init__(self, url: str):
        super().__init__(url)
        del self.ydl_opts['proxy']

    @staticmethod
    def check_format(format_: dict):
        return format_["video_ext"] == "mp4" and format_["audio_ext"] == "none" \
            and format_["protocol"] == "m3u8_native"


class VKDownloader(YoutubeDownloader):
    platform = Platform.VK
    proxy = ""

    def __init__(
            self, url: str,
            resolution: Optional[str] = "",
            callback: Optional[AsyncGenerator] = None
    ):
        super().__init__(url, resolution, callback)
        del self.ydl_opts['proxy']

    def collect_information(self):
        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(self._url, download=False)
            if "entries" in info:
                raise PlaylistError
            info = ydl.sanitize_info(info)
            # размер указан в байтах
            size = int(info['duration'] * info['tbr'] * (1024 / 8))
            if not self.check_size(size):
                raise TooBigVideo

            self.media_adapter = MediaAdapter(info["id"],
                                              platform=self.platform,
                                              resolution=self._resolution)

    def download(self):
        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(self._url, download=True)
            file_path = ydl.prepare_filename(info)
            self.media_adapter.set_file_path(file_path)
