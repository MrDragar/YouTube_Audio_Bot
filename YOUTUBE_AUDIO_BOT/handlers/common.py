from aiogram import types
from aiogram.dispatcher import FSMContext
from YOUTUBE_AUDIO_BOT import database
from YOUTUBE_AUDIO_BOT import messages as msg
from YOUTUBE_AUDIO_BOT.states import LanguageUserData


async def cancel(message: types.Message, state: FSMContext, language: str):
    await message.answer(msg.cancellation[language], reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def send_welcome(message: types.Message, language: str):
    await message.reply(msg.wellcoming[language])


async def choose_language(message: types.Message, language: str):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.InlineKeyboardButton(text=msg.languages["en"]),
                 types.InlineKeyboardButton(text=msg.languages["ru"]))
    keyboard.add(types.InlineKeyboardButton(text="Отмена"))

    await message.reply(msg.choosing_language[language], reply_markup=keyboard)
    await LanguageUserData.step_1.set()


async def change_language(message: types.Message, state: FSMContext):
    new_language = message.text
    language = list(msg.languages.keys())[list(msg.languages.values()).index(new_language)]
    database.change_language(language, message.from_user.id)
    await message.reply(f"{msg.changing_language[language]} {new_language}.", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
