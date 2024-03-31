from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from bot.database.models import Language
from bot.callbacks import FeedbackCallback


def get_type_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.add(types.KeyboardButton(text=_("Видео")))
    keyboard.add(types.KeyboardButton(text=_("Аудио")))
    keyboard.add(types.KeyboardButton(text=_("Отмена")))

    keyboard.adjust(2, 1)

    markup = keyboard.as_markup()
    markup.resize_keyboard = True
    markup.one_time_keyboard = True
    return markup


def get_resolution_keyboard(resolutions: dict[str, str]) \
        -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    for resolution in resolutions.keys():
        keyboard.add(types.KeyboardButton(text=resolution))
    keyboard.adjust(3)

    keyboard.row(types.KeyboardButton(text=_("Отмена")))
    markup = keyboard.as_markup()
    markup.one_time_keyboard = True
    markup.resize_keyboard = True
    return markup


def get_language_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    for language in Language:
        keyboard.button(text=language.get_language_name())

    keyboard.row(types.KeyboardButton(text=_("Отмена")))
    markup = keyboard.as_markup()
    markup.one_time_keyboard = True
    markup.resize_keyboard = True
    return markup


def get_share_link_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=_("Подписаться на канал"),
                    url="https://t.me/AudioDownloader")
    keyboard.button(text=_("Проверить подписку"),
                    callback_data="check_subscribe")
    return keyboard.as_markup()


def get_feedback_keyboard(user_id: int) -> types.InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=_("Ответить пользователю"),
                    callback_data=FeedbackCallback(user_id=user_id).pack())
    return keyboard.as_markup()


def get_joke_keyboard() -> types.reply_keyboard_markup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=_("Купить подписку"))
    keyboard.button(text=_("Админ лох"))
    keyboard.button(text=_("Отмена"))
    keyboard.adjust(2, 1)
    markup = keyboard.as_markup()
    markup.resize_keyboard = True

    return markup
