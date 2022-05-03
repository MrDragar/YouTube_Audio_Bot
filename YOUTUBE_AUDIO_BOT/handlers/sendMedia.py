from aiogram import types
from aiogram.dispatcher import FSMContext

import os
import logging

from YOUTUBE_AUDIO_BOT.downloader import download
from YOUTUBE_AUDIO_BOT import database
from YOUTUBE_AUDIO_BOT import messages as msg


async def send_audio(message: types.Message, state: FSMContext, language: str):
    await message.answer(msg.sending_audio["waiting"][language], reply_markup=types.ReplyKeyboardRemove())
    data = await state.get_data()
    url = data["url"]

    await state.finish()
    try:
        file, videoname, filename, media_path = await download(url=url, media_type="Audio")
        message_info = await message.answer_audio(file, title=videoname)
        if not media_path is None:
            os.remove(media_path)
            fileid = message_info["audio"]["file_id"]
            database.add_file_id("Audio", filename, fileid)
        database.add_good_result()
    except Exception as ex:
        logging.exception(ex)
        await message.answer(msg.sending_audio["error"][language])
        database.add_bad_result()


async def send_video(message: types.Message, state: FSMContext, language: str):
    resolution = message.text
    data = await state.get_data()
    url = data["url"]
    await message.answer(msg.sending_video["waiting"][language], reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

    try:
        file, videoname, filename, media_path = await download(url=url, media_type="Video", resolution=resolution)
        message_info = await message.answer_video(file, caption=videoname, supports_streaming=True, width=180,
                                                  height=100)
        if media_path is not None:
            os.remove(media_path)
            fileid = message_info["video"]["file_id"]
            database.add_file_id("Video", filename, fileid, resolution)
        database.add_good_result()
    except TimeoutError as a:
        logging.exception(a)
        os.remove(media_path)
        database.add_good_result()
    except Exception as ex:
        logging.exception(ex)
        await message.answer(msg.sending_video["error"][language])
        database.add_bad_result()
