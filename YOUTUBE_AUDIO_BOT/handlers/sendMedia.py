from aiogram import types
from aiogram.dispatcher import FSMContext

import os
import logging
from asyncio import TimeoutError

from YOUTUBE_AUDIO_BOT.downloaders.youtube_downloader import download_media, CantDownloadVideo
from YOUTUBE_AUDIO_BOT import database
from YOUTUBE_AUDIO_BOT.config import _


async def send_audio(message: types.Message, state: FSMContext):
    await message.answer(_("Подождите"), reply_markup=types.ReplyKeyboardRemove())
    data = await state.get_data()
    url = data["url"]
    await state.finish()
    try:
        audio = await download_media(url=url, video_format="audio")
    except CantDownloadVideo:
        return await message.answer(_("Вы дали некорректную ссылку."))
    except Exception as ex:
        logging.exception(ex)
        database.add_bad_result()
        return await message.answer(_("Произошла какая-то ошибка. Возможно вы дали некорректную ссылку."))
    if audio.is_on_server:
        await message.answer_audio(audio.file_id, title=audio.title)
    else:
        try:
            message_info = await message.answer_audio(audio.media_path, title=audio.title)
        except Exception as ex:
            logging.exception(Exception)
            return os.remove(audio.media_path)
        os.remove(audio.media_path)
        file_id = message_info["audio"]["file_id"]
        database.add_file_id("Audio", audio.link_id, file_id)
    database.add_good_result()


async def send_video(message: types.Message, state: FSMContext):
    resolution = message.text
    data = await state.get_data()
    url = data["url"]
    resolutions = data["resolutions"]
    if resolution not in resolutions.keys():
        return await message.answer(_("Невозможное разрешение"))
    await message.answer(_("Подождите"), reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

    try:
        video = await download_media(url=url, video_format=resolutions[resolution], resolution=resolution)
    except CantDownloadVideo:
        return await message.answer(_("Вы дали некорректную ссылку."))
    except Exception as ex:
        logging.exception(ex)
        database.add_bad_result()
        return await message.answer(_("Произошла какая-то ошибка. Возможно вы дали некорректную ссылку."))

    if video.is_on_server:
        await message.answer_video(video.file_id, caption=video.title, supports_streaming=True,
                                                  width=180, height=100)
    else:
        try:
            message_info = await message.answer_video(video.media_path, caption=video.title, supports_streaming=True,
                                                  width=180, height=100)
        except Exception as ex:
            os.remove(video.media_path)
            if isinstance(ex, TimeoutError):
                await message.answer(_("Видео слишком большое"))
            else:
                logging.exception(ex)
                await message.answer(_("Я не могу отправить это видео"))
            return

        os.remove(video.media_path)
        file_id = message_info["video"]["file_id"]
        database.add_file_id("Video", video.link_id, file_id, resolution)
    database.add_good_result()
