from downloader import download

import os
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.bot.api import TelegramAPIServer
from aiogram.utils.callback_data import CallbackData


cb = CallbackData("user", "url", "action")

class InputUserData(StatesGroup):
    step_1 = State()
    url = ''


API_TOKEN = os.environ.get("API_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize FSM storage
memory_storage = MemoryStorage()

local_server = TelegramAPIServer.from_base('http://0.0.0.0:8081')

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, server=local_server)

dp = Dispatcher(bot, storage=memory_storage)


@dp.message_handler(commands=['start', 'help'], commands_prefix="/")
async def send_welcome (message: types.Message):
    await message.reply("""Привет. Я "Скачать звук с YouTube". Если хочешь получить звук видео из YouTube, тебе
     нужно написать мне url адрес видео. Чтобы сделать это, открой видео в мобильном приложении YouTube, нажми на
      кнопку "Поделиться", выберите Телеграмм отправьте мне сообщение.""")


@dp.message_handler()
async def main (message: types.Message):
    url = message.text
    print(url)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.InlineKeyboardButton(text="Видео"),
                 types.InlineKeyboardButton(text="Аудио"))
    keyboard.add(types.InlineKeyboardButton(text="Отмена"))
    await message.answer("Выберите тип файла", reply_markup=keyboard)
    InputUserData.url = url
    await InputUserData.step_1.set()


@dp.message_handler(Text(equals="Аудио"), state=InputUserData.step_1, content_types=types.ContentTypes.TEXT)
async def send_audio(message: types.Message, state: FSMContext):
    await message.answer("Подождите", reply_markup=types.ReplyKeyboardRemove())
    url = InputUserData.url
    await state.finish()
    try:
        media_path, name = download(url=url, media_type="Audio")
        with open(media_path, "rb") as f:
            await message.answer_audio(f, title=name)
        os.remove(media_path)
    except Exception as ex:
        print(ex)
        await message.answer("Произошла какая-то ошибка. Возможно вы дали некорректную ссылку")


@dp.message_handler(Text(equals="Видео"), state=InputUserData.step_1, content_types=types.ContentTypes.TEXT)
async def send_video(message: types.Message, state: FSMContext):
    await message.answer("Подождите", reply_markup=types.ReplyKeyboardRemove())
    url = InputUserData.url
    await state.finish()
    try:
        media_path, name = download(url=url, media_type="Video")
        with open(media_path, "rb") as f:
            await message.answer_video(f, supports_streaming=True)
        os.remove(media_path)
    except Exception as ex:
        print(ex)
        await bot.send_message(message.from_user.id, "Произошла какая-то ошибка. Возможно вы дали некорректную ссылку")
    await state.finish()


@dp.message_handler(Text(equals="Отмена"), state=InputUserData.step_1, content_types=types.ContentTypes.TEXT)
async def cansel(message: types.Message, state: FSMContext):
    await message.answer("Отмена", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
    # a = bot.log_out()
    # print(a)

