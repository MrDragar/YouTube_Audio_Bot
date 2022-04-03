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
    username = message.from_user.username
    if username is None:
        username = message.from_user.first_name
    language = message.from_user.language_code
    if not language in msg.languages.keys():
        language = "en"
    database.add_user(message.from_user.id, username, language)
    language = database.get_language(message.from_user.id)
    await message.reply(msg.wellcoming[language])


async def choose_language(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.InlineKeyboardButton(text=msg.languages["en"]), types.InlineKeyboardButton(text=msg.languages["ru"]))
    keyboard.add(types.InlineKeyboardButton(text="Отмена"))
    language = database.get_language(message.from_user.id)
    text = msg.choosing_language[language]
    await message.reply(text, reply_markup=keyboard)
    await LanguageUserData.step_1.set()


async def change_language(message:types.Message, state: FSMContext):
    new_language = message.text
    language = list(msg.languages.keys())[list(msg.languages.values()).index(new_language)]
    database.change_language(language, message.from_user.id)
    await message.reply(f"{msg.changing_language[language]} {new_language}.", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()