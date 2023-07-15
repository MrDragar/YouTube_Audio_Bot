from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def register_commands(bot: Bot):
    ru_bot_commands = [
        BotCommand(command="start", description="Старт бота"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="cancel", description="Отмена"),
        BotCommand(command="send_feedback", description="Отправить отзыв")
                       ]
    await bot.set_my_commands(commands=ru_bot_commands,
                              scope=BotCommandScopeDefault(), language_code=None)

    uk_bot_commands = [
        BotCommand(command="start", description="Старт бота"),
        BotCommand(command="help", description="Допомога"),
        BotCommand(command="cancel", description="Скасування"),
        BotCommand(command="send_feedback", description="Надіслати відгук")
                       ]
    await bot.set_my_commands(commands=uk_bot_commands,
                              scope=BotCommandScopeDefault(), language_code="uk")

    en_bot_commands = [
        BotCommand(command="start", description="Start bot"),
        BotCommand(command="help", description="Help"),
        BotCommand(command="cancel", description="Cancel"),
        BotCommand(command="send_feedback", description="Send feedback")
                       ]
    await bot.set_my_commands(commands=en_bot_commands,
                              scope=BotCommandScopeDefault(), language_code="en")