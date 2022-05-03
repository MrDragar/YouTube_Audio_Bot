from aiogram import types
from aiogram.dispatcher import FSMContext

from YOUTUBE_AUDIO_BOT.downloader import get_resolutions
from YOUTUBE_AUDIO_BOT import database
from YOUTUBE_AUDIO_BOT import messages as msg
from .mediaType import InputUserData


async def send_video_resolutions(message: types.Message, state: FSMContext, language: str):
    data = await state.get_data()
    url = data["url"]
    resolutions = await get_resolutions(url)
    if resolutions is None:
        await message.answer(msg.video_resolution["error"][language],
                             reply_markup=types.ReplyKeyboardRemove())
        database.add_bad_result()
        await state.finish()
    else:

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in resolutions:
            keyboard.insert(types.InlineKeyboardButton(text=i))
        await message.answer(msg.video_resolution["success"][language], reply_markup=keyboard)
        await InputUserData.step_2.set()
