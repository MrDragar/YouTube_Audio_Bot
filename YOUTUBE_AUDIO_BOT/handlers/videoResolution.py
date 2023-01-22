import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from YOUTUBE_AUDIO_BOT.downloader import get_video_resolution, CantDownloadVideo
from YOUTUBE_AUDIO_BOT import database
from YOUTUBE_AUDIO_BOT.states import InputUserData
from YOUTUBE_AUDIO_BOT.config import _


async def send_video_resolutions(message: types.Message, state: FSMContext):
    data = await state.get_data()
    url = data["url"]
    try:
        resolutions = await get_video_resolution(url)
    except CantDownloadVideo:
        await message.answer(_("Вы дали некорректную ссылку"))
        await state.finish()
    except Exception as e:
        logging.exception(e)
        await message.answer(_("Произошла какая-то ошибка. Возможно вы дали некорректную ссылку."),
                             reply_markup=types.ReplyKeyboardRemove())
        database.add_bad_result()
        await state.finish()
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in resolutions.keys():
            keyboard.insert(types.InlineKeyboardButton(text=i))
        await message.answer(_("Выберите разрешение видео"), reply_markup=keyboard)
        await InputUserData.step_2.set()
        await state.update_data(resolutions=resolutions, url=url)
