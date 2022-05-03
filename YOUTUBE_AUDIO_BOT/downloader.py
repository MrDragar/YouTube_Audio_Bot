import asyncio
import logging
from functools import wraps, partial
from concurrent.futures import ThreadPoolExecutor
import pytube
from YOUTUBE_AUDIO_BOT import database
from aiogram.types import InputFile


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
def download(url: str, media_type: str, resolution: str = None):
    yt = pytube.YouTube(url)
    video_name = yt.title
    filename = yt.video_id
    fileid = database.get_file_id(media_type, filename, resolution)
    media_path = ''
    if fileid is not None:
        return fileid, video_name, filename, None
    if media_type == "Audio":
        stream = yt.streams.filter(only_audio=True).first()
        stream.download("./audio/", filename=filename)
        media_path = "./audio/" + filename
    elif media_type == "Video":
        stream = yt.streams.filter(progressive=True, resolution=resolution).first()
        stream.download("./video/", filename=filename)
        media_path = "./video/" + filename
    return InputFile(media_path), video_name, filename, media_path


@wrap
def get_resolutions(url: str):
    try:
        yt = pytube.YouTube(url)
        streams = yt.streams.filter(progressive=True)
        resolutions = []
        for stream in streams:
            resolutions.append(stream.resolution)
        return resolutions
    except Exception as ex:
        logging.exception(ex)
        return
