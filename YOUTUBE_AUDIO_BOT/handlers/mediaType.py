from YOUTUBE_AUDIO_BOT import database
from YOUTUBE_AUDIO_BOT import messages as msg
import re
from aiogram import types, Dispatcher
from YOUTUBE_AUDIO_BOT.states import InputUserData


async def choose_media_type(message: types.Message, language: str):
    text = message.text

    urls = re.findall(r'http(?:s)?://\S+', text)
    if not urls:
        return await message.answer("Нет ссылки в сообщении")
    url = urls[0]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row(types.InlineKeyboardButton(text=msg.media_buttons["video"][language]),
                 types.InlineKeyboardButton(text=msg.media_buttons["audio"][language]))
    keyboard.add(types.InlineKeyboardButton(text=msg.media_buttons["cancel"][language]))
    await message.answer(msg.choosing_media_type[language], reply_markup=keyboard)
    await InputUserData.step_1.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(url=url)


