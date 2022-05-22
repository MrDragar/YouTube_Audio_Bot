from aiogram import types
from aiogram.dispatcher import FSMContext
from pytube.exceptions import RegexMatchError, VideoUnavailable

import os
import logging

from YOUTUBE_AUDIO_BOT.downloader import download, Media, Audio, Video
from YOUTUBE_AUDIO_BOT import database
from YOUTUBE_AUDIO_BOT import messages as msg


async def send_audio(message: types.Message, state: FSMContext, language: str):
    await message.answer(msg.sending_media["waiting"][language], reply_markup=types.ReplyKeyboardRemove())
    data = await state.get_data()
    url = data["url"]

    await state.finish()
    try:
        audio = await download(url=url, media_type="Audio")
    except RegexMatchError:
        return await message.answer(msg.sending_media["RegexMatchError"][language])
    except VideoUnavailable:
        return await message.answer(msg.sending_media["VideoUnavailable"][language])
    except KeyError:
        return await message.answer(msg.sending_media["KeyError"][language])
    except Exception as ex:
        logging.exception(ex)
        database.add_bad_result()
        return await message.answer(msg.sending_media["error"][language])
    if audio.is_on_server:
        await message.answer_audio(audio.file_id, title=audio.title)
    else:
        with open(audio.media_path, "rb") as f:
            message_info = await message.answer_audio(f, title=audio.title)
        os.remove(audio.media_path)
        file_id = message_info["audio"]["file_id"]
        database.add_file_id("Audio", audio.link_id, file_id)
    database.add_good_result()


async def send_video(message: types.Message, state: FSMContext, language: str):
    resolution = message.text
    data = await state.get_data()
    url = data["url"]
    await message.answer(msg.sending_media["waiting"][language], reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

    try:
        video = await download(url=url, media_type="Video", resolution=resolution)
    except RegexMatchError:
        return await message.answer(msg.sending_media["RegexMatchError"][language])
    except VideoUnavailable:
        return await message.answer(msg.sending_media["VideoUnavailable"][language])
    except KeyError:
        return await message.answer(msg.sending_media["KeyError"][language])
    except Exception as ex:
        logging.exception(ex)
        database.add_bad_result()
        return await message.answer(msg.sending_media["error"][language])

    if video.is_on_server:
        await message.answer_video(video.file_id, caption=video.title, supports_streaming=True,
                                                  width=180, height=100)
    else:
        with open(video.media_path, "rb") as f:

            message_info = await message.answer_video(f, caption=video.title, supports_streaming=True,
                                                  width=180, height=100)

        os.remove(video.media_path)
        file_id = message_info["video"]["file_id"]
        database.add_file_id("Video", video.link_id, file_id, video.resolution)
    database.add_good_result()
