import asyncio
from dataclasses import dataclass
from abc import ABC
from functools import wraps, partial
from concurrent.futures import ThreadPoolExecutor
import pytube
from YOUTUBE_AUDIO_BOT import database


def wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        executor = ThreadPoolExecutor()
        return await loop.run_in_executor(executor, pfunc)
    return run


@dataclass
class Media(ABC):
    title: str
    link_id: str
    is_on_server: bool
    media_path: str or None
    file_id: str or None


@dataclass
class Audio(Media):
    pass


@dataclass
class Video(Media):
    resolution: str


@wrap
def download(url: str, media_type: str, resolution: str or None = None) -> Media:
    yt = pytube.YouTube(url, use_oauth=True)
    title = yt.title
    link_id = yt.video_id
    file_id = database.get_file_id(media_type, link_id, resolution)
    if media_type == "Audio":
        if file_id is not None:
            return Audio(title, link_id, True, None, file_id)
        stream = yt.streams.filter(only_audio=True).first()
        audio_path = f"./audio/{link_id}"
        stream.download("./audio/", link_id)
        return Audio(title, link_id, False, audio_path, None)
    elif media_type == "Video":
        if file_id is not None:
            return Video(title, link_id, True, None, file_id, resolution=resolution)
        stream = yt.streams.filter(progressive=True, resolution=resolution).first()
        media_path = f"./video/{link_id}"
        stream.download("./video/", link_id)
        return Video(title, link_id, False, media_path, None, resolution)
    raise TypeError("Incorrect media_type")


@wrap
def get_resolutions(url: str):
    yt = pytube.YouTube(url, use_oauth=True)
    streams = yt.streams.filter(progressive=True)
    resolutions = []
    for stream in streams:
        resolutions.append(stream.resolution)
    return resolutions

