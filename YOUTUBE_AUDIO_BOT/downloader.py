import asyncio
from typing import NamedTuple
from yt_dlp import YoutubeDL
from YOUTUBE_AUDIO_BOT.database import get_file_id


class Video(NamedTuple):
    title: str
    link_id: str
    is_on_server: bool
    media_path: str or None
    file_id: str or None


class CantDownloadVideo(Exception):
    """Impossible to download video"""


class BlockedVideoInCountry(CantDownloadVideo):
    """Video is blocked in this country"""


async def _parse_video_information(output: bytes) -> list:
    try:
        video_information_output = output.decode().split("\n")
    except UnicodeDecodeError:
        raise CantDownloadVideo
    return video_information_output


async def _parse_video_resolution(video_information: list) -> dict:
    video_resolution = {}
    video_information = [x.split() for x in video_information]
    for i in video_information:
        if "mp4" in i and "only" in i:
            video_resolution[i[-2][:-1]] = i[0]
    if not video_resolution:
        raise CantDownloadVideo
    return video_resolution


async def _make_command_for_video(resolution_id: str, url: str) -> list:
    command = ["yt-dlp", "-f", f"{resolution_id}+bestaudio[ext=m4a]", "--merge-output-format", "mp4",
               "-P", "video/", url]
    return command


async def _make_command_for_audio(url: str) -> list:
    command = ["yt-dlp", "--no-playlist", "-f", "bestaudio[ext=m4a]", "-P", "video/", url]
    return command


async def _make_command_for_resolution(url: str) -> list:
    command = ["yt-dlp", "--no-playlist", "-F", url]
    return command


async def _use_yt_dlp(command: list) -> bytes:
    process = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE,
                                                   stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    if stderr:
        print(stderr.decode())
        raise CantDownloadVideo
    return stdout


async def _find_string_about_file(video_information: list) -> str:
    info = ""
    for i in video_information:
        if "FixupM4a" in i or "Merger" in i:
            info = i
    if info:
        return info
    raise CantDownloadVideo


async def _parse_file_path(file_string: str) -> str:
    path = file_string.split('''"''')[1]
    return path


async def get_video_resolution(url: str) -> dict:
    """Возвращает список из всех возможных разрешений скачиваемого видео"""
    command = await _make_command_for_resolution(url)
    output = await _use_yt_dlp(command)
    video_information = await _parse_video_information(output)
    return await _parse_video_resolution(video_information)


async def download_media(video_format: str, url: str, resolution: str or None = None) -> Video:
    try:
        with YoutubeDL(params={"noplaylist":True}) as ydl:
            info_dict = ydl.extract_info(url=url, download=False)
            video_id = info_dict.get("id", None)
            video_title = info_dict.get('title', None)
    except Exception as exception:
        if """This video contains content from SME, who has blocked it in your country""" in exception.args[0]:
            raise BlockedVideoInCountry
        raise CantDownloadVideo
    if video_format == "audio":
        file_id = get_file_id("Audio", video_id)
        command = await _make_command_for_audio(url)
    else:
        file_id = get_file_id("Video", video_id, resolution)
        command = await _make_command_for_video(video_format, url)
    if file_id:
        return Video(title=video_title, link_id=video_id, is_on_server=True, media_path=None, file_id=file_id)
    output = await _use_yt_dlp(command)
    video_information = await _parse_video_information(output)
    string_file = await _find_string_about_file(video_information)
    file_path = await _parse_file_path(string_file)
    return Video(title=video_title, link_id=video_id, is_on_server=False, media_path=file_path, file_id=None)


if __name__ == "__main__":
    pass
    # print(asyncio.run(get_video_resolution("https://www.youtube.com/watch?v=W273HN3bTPk")))
    # video = (asyncio.run(download_media("audio", "https://www.youtube.com/watch?v=yRbR-Rh2EXU")))
    # print(asyncio.run(download_media("135", "https://www.youtube.com/watch?v=W273HN3bTPk")))
