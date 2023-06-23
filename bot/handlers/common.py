from typing import Any

from aiogram.dispatcher.router import Router
from aiogram.handlers import MessageHandler
from aiogram.methods import SendMessage
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
class StartHandler(MessageHandler):
    async def handle(self) -> Any:
        await SendMessage(chat_id=self.chat.id, text="Message")
