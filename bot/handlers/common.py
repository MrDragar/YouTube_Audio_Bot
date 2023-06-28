from typing import Any

from aiogram.dispatcher.router import Router
from aiogram.handlers import MessageHandler
from aiogram.methods import SendMessage
from aiogram.filters import Command, Text
from aiogram import types

from . base_handlers import StateMassageHandler
from bot.states import Youtube

common_router = Router()


@common_router.message(Command("cancel"))
@common_router.message(Text("отмена", ignore_case=True))
@common_router.message(Text("cancel", ignore_case=True))
@common_router.message(Text("вiдмiна", ignore_case=True))
class CancelHandler(StateMassageHandler):
    text = "Отмена"

    async def handle(self) -> Any:
        await SendMessage(chat_id=self.chat.id, text=self.text,
                          reply_markup=types.ReplyKeyboardRemove())
        await self.state.clear()


@common_router.message(Command("start", "help"))
class StartHandler(StateMassageHandler):
    text = "Привет. С помощью этого бота ты можешь скачать любое видео или аудио с Ютуба. " \
           "Для этого вам необходимо скинуть ссылку на этот ролик. По всем вопросам пишите на " \
           "yshhenyaev@mail.ru\n" \
           "Для смены языка пропишите \n/language ."

    async def handle(self) -> Any:
        await self.state.set_state(Youtube.type)
        await SendMessage(chat_id=self.chat.id, text=self.text)
