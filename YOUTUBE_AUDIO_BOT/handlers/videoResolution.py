from aiogram import types
from aiogram.dispatcher import FSMContext

from downloader import get_resolutions
import database
from .mediaType import InputUserData


async def send_video_resolutions (message: types.Message, state: FSMContext):
    url = InputUserData.url
    resolutions = await get_resolutions(url)
    if resolutions is None:
        await message.answer("Произошла какая-то ошибка. Возможно вы дали некорректную ссылку",
         reply_markup=types.ReplyKeyboardRemove())
        database.add_bad_result()
        await state.finish()
    else:
        
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in resolutions:
            keyboard.insert(types.InlineKeyboardButton(text=i))
        await message.answer("Выберите разрешение видео", reply_markup=keyboard)
        await InputUserData.step_2.set()
