from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def get_type_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(types.KeyboardButton(text=_("Видео")),
                 types.KeyboardButton(text=_("Аудио")))

    keyboard.add(types.KeyboardButton(text=_("Отмена")))
    return keyboard.as_markup()
