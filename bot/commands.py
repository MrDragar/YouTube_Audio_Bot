from aiogram.types import BotCommand, BotCommandScopeDefault, \
    BotCommandScopeChat

from bot.config import ADMINS_ID
from bot.loader import bot
from bot.database.models import Language

ru_bot_commands = [
    BotCommand(command="start", description="Старт бота"),
    BotCommand(command="help", description="Помощь"),
    BotCommand(command="cancel", description="Отмена"),
    BotCommand(command="language", description="Сменить язык"),
    BotCommand(command="send_feedback", description="Отправить отзыв")
]
uk_bot_commands = [
    BotCommand(command="start", description="Старт бота"),
    BotCommand(command="help", description="Допомога"),
    BotCommand(command="cancel", description="Скасування"),
    BotCommand(command="language", description="Змінити мову"),
    BotCommand(command="send_feedback", description="Надіслати відгук")
]
en_bot_commands = [
    BotCommand(command="start", description="Start bot"),
    BotCommand(command="help", description="Help"),
    BotCommand(command="cancel", description="Cancel"),
    BotCommand(command="language", description="Change language"),
    BotCommand(command="send_feedback", description="Send feedback")
]
admin_bot_commands = [
    BotCommand(command="start", description="Старт"),
    BotCommand(command="help", description="Помощь"),
    BotCommand(command="cancel", description="Отмена"),
    BotCommand(command="language", description="Сменить язык"),
    BotCommand(command="send_feedback", description="Зачем тебе отправлять отзыв?"),
    BotCommand(command="post", description="Отправка сообщения пользователям"),
]


async def register_commands():
    await bot.set_my_commands(commands=ru_bot_commands,
                              scope=BotCommandScopeDefault(), language_code=None)

    await bot.set_my_commands(commands=uk_bot_commands,
                              scope=BotCommandScopeDefault(), language_code="uk")

    await bot.set_my_commands(commands=en_bot_commands,
                              scope=BotCommandScopeDefault(), language_code="en")

    for admin_id in ADMINS_ID:
        await bot.set_my_commands(commands=admin_bot_commands,
                                  scope=BotCommandScopeChat(chat_id=admin_id))


async def set_commands_for_user(language_code: Language, user_id: int):
    if user_id in ADMINS_ID:
        return
    match language_code:
        case Language.RUSSIAN:
            commands = ru_bot_commands
        case Language.ENGLISH:
            commands = en_bot_commands
        case Language.UKRAINIAN:
            commands = uk_bot_commands
        case _:
            return

    await bot.set_my_commands(commands=commands,
                              scope=BotCommandScopeChat(chat_id=user_id))
