from YOUTUBE_AUDIO_BOT.config import _
import re
from aiogram import types, Dispatcher
from YOUTUBE_AUDIO_BOT.states import InputUserData


async def choose_media_type(message: types.Message):
    text = message.text

    urls = re.findall(r'http(?:s)?://\S+', text)
    if not urls:
        return await message.answer(_("Нет ссылки в сообщении"))
    url = urls[0]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row(types.InlineKeyboardButton(text=_("Видео")),
                 types.InlineKeyboardButton(text=_("Аудио")))
    keyboard.add(types.InlineKeyboardButton(text=_("Отмена")))
    await message.answer(_("Выберите тип файла"), reply_markup=keyboard)
    await InputUserData.step_1.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(url=url)


