from aiogram import types
from aiogram.dispatcher import FSMContext

import os
from downloader import download
import database
from handlers.mediaType import InputUserData

async def send_audio (message: types.Message, state: FSMContext):
    await message.answer("Подождите", reply_markup=types.ReplyKeyboardRemove())
    url = InputUserData.url
    await state.finish()
    try:
        media_path, name = await download(url=url, media_type="Audio")
        with open(media_path, "rb") as f:
            await message.answer_audio(f, title=name)
        os.remove(media_path)
        database.add_good_result()
    except Exception as ex:
        print(ex)
        await message.answer("Произошла какая-то ошибка. Возможно вы дали некорректную ссылку")
        database.add_bad_result()


async def send_video (message: types.Message, state: FSMContext):
    resolution = message.text
    url = InputUserData.url
    await message.answer("Подождите", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    try:
        media_path, name = await download(url=url, media_type="Video", resolution=resolution)
        with open(media_path, "rb") as f:
            await message.answer_video(f, supports_streaming=True, width=180, height=100, caption=name)
        os.remove(media_path)
        database.add_good_result()
    except TimeoutError as a:
        print(a)
        os.remove(media_path)
        database.add_good_result()
    except Exception as ex:
        print(ex, type(ex))
        await message.answer("Простите, что-то пошло нетак.")
        database.add_bad_result()