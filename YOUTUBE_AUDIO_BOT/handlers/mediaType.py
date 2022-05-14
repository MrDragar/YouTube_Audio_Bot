from YOUTUBE_AUDIO_BOT import database
from YOUTUBE_AUDIO_BOT import messages as msg

from aiogram import types, Dispatcher
from YOUTUBE_AUDIO_BOT.states import InputUserData


async def chooseMeiaType(message: types.Message, language: str):
    url = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row(types.InlineKeyboardButton(text=msg.media_buttons["video"][language]),
                 types.InlineKeyboardButton(text=msg.media_buttons["audio"][language]))
    keyboard.add(types.InlineKeyboardButton(text=msg.media_buttons["cancel"][language]))
    await message.answer(msg.choosing_media_type[language], reply_markup=keyboard)
    await InputUserData.step_1.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(url=url)


