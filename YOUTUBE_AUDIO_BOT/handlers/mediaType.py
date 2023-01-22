import os

from YOUTUBE_AUDIO_BOT import database
from YOUTUBE_AUDIO_BOT.config import _
import re
from aiogram import types, Dispatcher
from YOUTUBE_AUDIO_BOT.states import InputUserData
from YOUTUBE_AUDIO_BOT.downloaders.tiktok_downloader import download_video
from YOUTUBE_AUDIO_BOT.downloaders.youtube_downloader import IncorrectLink, CantDownloadVideo


async def send_tiktok_video(message: types.Message, url: str):
    await message.answer(_("Подождите"))
    filepath = "video/" + str(message.from_user.id) + str(message.message_id) + ".mp4"
    try:
        await download_video(url, filepath)
    except IncorrectLink:
        await message.answer(_("Вы дали некорректную ссылку"))
    except CantDownloadVideo():
        await message.answer(_("Произошла какая-то ошибка. Возможно вы дали некорректную ссылку."))
    with open(filepath, "rb") as f:
        await message.answer_video(f, supports_streaming=True)
    os.remove(filepath)
    database.add_good_result()


async def choose_media_type(message: types.Message):
    text = message.text

    urls = re.findall(r'http(?:s)?://\S+', text)
    if not urls:
        return await message.answer(_("Нет ссылки в сообщении"))
    url = urls[0]
    if "tiktok" in url:
        return await send_tiktok_video(message, url)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row(types.InlineKeyboardButton(text=_("Видео")),
                 types.InlineKeyboardButton(text=_("Аудио")))
    keyboard.add(types.InlineKeyboardButton(text=_("Отмена")))
    await message.answer(_("Выберите тип файла"), reply_markup=keyboard)
    await InputUserData.step_1.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(url=url)
