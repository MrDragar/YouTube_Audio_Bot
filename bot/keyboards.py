from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from bot.database.models import Language

def get_type_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.add(types.KeyboardButton(text=_("Видео")))
    keyboard.add(types.KeyboardButton(text=_("Аудио")))
    keyboard.add(types.KeyboardButton(text=_("Отмена")))

    keyboard.adjust(2, 1)

    markup = keyboard.as_markup()
    markup.resize_keyboard = True
    return markup


def get_resolution_keyboard(resolutions: dict[str, str]) \
        -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    for resolution in resolutions.keys():
        keyboard.add(types.KeyboardButton(text=resolution))
    keyboard.adjust(3)

    keyboard.row(types.KeyboardButton(text=_("Отмена")))
    markup = keyboard.as_markup()
    markup.resize_keyboard = True
    return markup


def get_language_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    for language in Language:
        keyboard.button(text=language.get_language_name())

    keyboard.row(types.KeyboardButton(text=_("Отмена")))
    markup = keyboard.as_markup()
    markup.resize_keyboard = True
    return markup
