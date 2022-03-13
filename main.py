from downloader import get_resolutions, download
import database

import os
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.bot.api import TelegramAPIServer
from aiogram.utils.callback_data import CallbackData
from asyncio.exceptions import TimeoutError

cb = CallbackData("user", "url", "action")


class InputUserData(StatesGroup):
    step_1 = State()
    step_2 = State()
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
    database.add_user(message.from_user.id, message.from_user.first_name)


@dp.message_handler(Text(equals="Аудио"), state=InputUserData.step_1, content_types=types.ContentTypes.TEXT)
async def send_audio (message: types.Message, state: FSMContext):
    await message.answer("Подождите", reply_markup=types.ReplyKeyboardRemove())
    url = InputUserData.url
    await state.finish()
    try:
        media_path, name = await download(url=url, media_type="Audio")
        with open(media_path, "rb") as f:
            await message.answer_audio(f, title=name)
        os.remove(media_path)
        database.add_good_result()
    except Exception as ex:
        print(ex)
        await message.answer("Произошла какая-то ошибка. Возможно вы дали некорректную ссылку")
        database.add_bad_result()


# noinspection PyBroadException
@dp.message_handler(Text(equals="Видео"), state=InputUserData.step_1, content_types=types.ContentTypes.TEXT)
async def send_video_resolutions (message: types.Message, state: FSMContext):
    # await message.answer("Подождите", reply_markup=types.ReplyKeyboardRemove())
    url = InputUserData.url
    resolutions = await get_resolutions(url)
    if resolutions is None:
        await bot.send_message(message.from_user.id, "Произошла какая-то ошибка. Возможно вы дали некорректную ссылку")
        database.add_bad_result()
        await state.finish()
    else:
 
        
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in resolutions:
            keyboard.insert(types.InlineKeyboardButton(text=i))
        await bot.send_message(message.from_user.id, "Выберите разрешение видео", reply_markup=keyboard)
        await InputUserData.step_2.set()



@dp.message_handler(Text(equals=["144p", "360p", "720p", "1080p"]), state=InputUserData.step_2, content_types=types.ContentTypes.TEXT)
async def send_video (message: types.Message, state: FSMContext):
    resolution = message.text
    url = InputUserData.url
    await bot.send_message(message.from_user.id, "Подождите", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    try:
        media_path, name = await download(url=url, media_type="Video", resolution=resolution)
        with open(media_path, "rb") as f:
            await bot.send_video(message.from_user.id, f, supports_streaming=True, width=180, height=100, caption=name)
        os.remove(media_path)
        database.add_good_result()
    except TimeoutError as a:
        print(a)
        os.remove(media_path)
        database.add_good_result()
    except Exception as ex:
        print(ex, type(ex))
        await bot.send_message(message.from_user.id, "Простите, что-то пошло нетак.")
        database.add_bad_result()


@dp.message_handler(Text(equals="Отмена"), state=InputUserData.step_1, content_types=types.ContentTypes.TEXT)
async def cansel (message: types.Message, state: FSMContext):
    await message.answer("Отмена", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


if __name__ == '__main__':
    database.init_db()
    executor.start_polling(dp, skip_updates=False, timeout=1000000)
    # a = bot.log_out()
    # print(a)
