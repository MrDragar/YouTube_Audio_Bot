import asyncio
from dataclasses import dataclass
from abc import ABC


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


class CantDownloadVideo(Exception):
    """Impossible to download video"""


async def _get_youtube_dl_output(url: str) -> bytes:
    process = await asyncio.create_subprocess_exec("youtube-dl", "-F", url, stdout=asyncio.subprocess.PIPE,
                                                   stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    if stderr:
        raise CantDownloadVideo(stderr.decode())
    return stdout


async def _parse_video_information(output: bytes) -> list:
    try:
        video_information_output = [x.split() for x in output.decode().split("\n")]
    except UnicodeDecodeError:
        raise CantDownloadVideo
    return video_information_output


async def _parse_video_resolution(video_information: list) -> list:
    video_resolution = []
    for i in video_information:
        if "mp4" in i and "only," in i:
            video_resolution.append(i[3])
    if not video_resolution:
        raise CantDownloadVideo
    return video_resolution


async def get_video_resolution(url: str) -> list:
    """Возвращает список из всех возможных разрешений скачиваемого видео"""
    output = await _get_youtube_dl_output(url)
    video_information = await _parse_video_information(output)
    return await _parse_video_resolution(video_information)


if __name__ == "__main__":
    print(asyncio.run(get_video_resolution("https://www.youtube.com/watch?v=W273HN3bTPk")))
