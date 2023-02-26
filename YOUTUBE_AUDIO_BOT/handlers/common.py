from aiogram import types
from aiogram.dispatcher import FSMContext
from YOUTUBE_AUDIO_BOT import database
from YOUTUBE_AUDIO_BOT.config import languages
from YOUTUBE_AUDIO_BOT.states import LanguageUserData
from YOUTUBE_AUDIO_BOT.config import _


async def cancel(message: types.Message, state: FSMContext):
    await message.answer(_("Отмена"), reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def send_welcome(message: types.Message):
    await message.reply(_("Привет. С помощью этого бота ты можешь скачать любое видео или аудио с Ютуба."
                          "Для этого вам необходимо скинуть ссылку на этот ролик. По всем вопросам пишите на "
                          "yshhenyaev@mail.ru\n"
                          "Для смены языка пропишите \n/language ."))


async def choose_language(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.InlineKeyboardButton(text="English"),
                 types.InlineKeyboardButton(text="Русский"),
                 types.InlineKeyboardButton(text="Українська"))
    keyboard.add(types.InlineKeyboardButton(text=_("Отмена")))

    await message.reply(_("""Для смены языка выберите из списка нужный язык"""), reply_markup=keyboard)
    await LanguageUserData.step_1.set()


async def change_language(message: types.Message, state: FSMContext):
    new_language = message.text
    language = list(languages.keys())[list(languages.values()).index(new_language)]
    database.change_language(language, message.from_user.id)
    await message.reply(_('Вы успешно изменили свой язык на', locale=language) +
                        f" {new_language}.", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def share_channel_link(message: types.Message):
    button = types.inline_keyboard.InlineKeyboardButton(text="Telegram Channel", url="https://t.me/+5qfagTVTgWgxM2Qy")
    markup = types.inline_keyboard.InlineKeyboardMarkup(row_width=1, inline_keyboard=[[button]])
    await message.answer("Для работы бота сперва необходимо подписаться на наш канал\n"
                         "For the bot to work, you first need to subscribe to our channel\n"
                         "Для роботи бота спершу необхідно підписатися на наш канал \n"
                         , reply_markup=markup)
