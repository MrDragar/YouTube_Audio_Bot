import asyncio
from functools import wraps, partial
from concurrent.futures import ThreadPoolExecutor
import pytube
from typing import Optional
from awaits.awaitable import awaitable


def wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        executor = ThreadPoolExecutor()
        return await loop.run_in_executor(executor, pfunc)
    return run


@wrap
def download(url: str, media_type: str):
    yt = pytube.YouTube(url)
    video_name = yt.title
    name = yt.video_id
    if media_type == "Audio":
        stream = yt.streams.filter(only_audio=True).first()
        stream.download("./audio/", filename=name)
        media_path = "./audio/" + name
    elif media_type == "Video":
        stream = yt.streams.filter().get_highest_resolution()
        stream.download("./video/", filename=name)
        media_path = "./video/" + name
    return media_path, video_name

