from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from YOUTUBE_AUDIO_BOT import database
from YOUTUBE_AUDIO_BOT import messages as msg


class LanguageUserData(StatesGroup):
    step_1 = State()


async def cancel(message: types.Message, state: FSMContext):
    language = database.get_language(message.from_user.id)
    await message.answer(msg.cancellation[language], reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def send_welcome(message: types.Message):
    database.add_user(message.from_user.id, message.from_user.username)
    language = database.get_language(message.from_user.id)
    await message.reply(msg.wellcoming[language])


async def choose_language(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.InlineKeyboardButton(text="en"), types.InlineKeyboardButton(text="ru"))
    keyboard.add(types.InlineKeyboardButton(text="Отмена"))
    language = database.get_language(message.from_user.id)
    await message.reply(msg.choosing_language[language], reply_markup=keyboard)
    await LanguageUserData.step_1.set()


async def change_language(message:types.Message, state: FSMContext):
    new_language = message.text
    database.change_language(new_language, message.from_user.id)
    await message.reply(f"{msg.changing_language[new_language]} {new_language}.", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()