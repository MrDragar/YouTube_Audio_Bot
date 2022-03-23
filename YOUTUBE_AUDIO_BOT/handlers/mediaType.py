from YOUTUBE_AUDIO_BOT import database
from YOUTUBE_AUDIO_BOT import messages as msg

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup


class InputUserData(StatesGroup):
    step_1 = State()
    step_2 = State()
    url = ''


async def chooseMeiaType(message: types.Message):
    url = message.text
    language = database.get_language(message.from_user.id)
    print(url)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.InlineKeyboardButton(text=msg.media_buttons["video"][language]),
                 types.InlineKeyboardButton(text=msg.media_buttons["audio"][language]))
    keyboard.add(types.InlineKeyboardButton(text=msg.media_buttons["cancel"][language]))
    await message.answer(msg.choosing_media_type[language], reply_markup=keyboard)
    await InputUserData.step_1.set()
    InputUserData.url = url
    database.add_user(message.from_user.id, message.from_user.first_name)

