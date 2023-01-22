import asyncio
import logging

from YOUTUBE_AUDIO_BOT.downloaders.youtube_downloader import CantDownloadVideo, IncorrectLink


async def _make_command(url: str, filepath) -> list:
    command = ["python3", "-m", "tiktok_downloader", "--snaptik", "--url", url, "--save", filepath]
    return command


async def _use_tiktok_downloader(command: list):
    process = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE,
                                                   stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    if "ERROR" in stderr.decode():
        logging.exception(stderr.decode())
        raise CantDownloadVideo
    if not stdout:
        raise IncorrectLink


async def download_video(url: str, filepath: str):
    command = await _make_command(url=url, filepath=filepath)
    print(*command)
    await _use_tiktok_downloader(command)


# if __name__ == "__main__":
    # asyncio.run(download_video("https://www.tiktok.com/@mcrawfit/video/7184289023244979461?is_from_webapp=1&sender_device=pc&web_id=7191340886918465026", "video/123.mp4"))
