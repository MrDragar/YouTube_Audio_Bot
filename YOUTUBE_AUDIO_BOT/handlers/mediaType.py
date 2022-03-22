from curses.ascii import FS
import database

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup


class InputUserData(StatesGroup):
    step_1 = State()
    step_2 = State()
    url = ''


async def chooseMeiaType(message: types.Message):
    url = message.text
    print(url)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.InlineKeyboardButton(text="Видео"),
                 types.InlineKeyboardButton(text="Аудио"))
    keyboard.add(types.InlineKeyboardButton(text="Отмена"))
    await message.answer("Выберите тип файла", reply_markup=keyboard)
    await InputUserData.step_1.set()
    InputUserData.url = url
    database.add_user(message.from_user.id, message.from_user.first_name)

