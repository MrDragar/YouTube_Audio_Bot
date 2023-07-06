from aiogram.methods import SendMessage, ForwardMessage, CopyMessage
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _

from .base_handlers import StateMassageHandler
from bot.filters import IsAdmin
from bot.states import PostingState
from bot.database.user import get_users

admin_router = Router()


@admin_router.message(Command("post"), IsAdmin())
class StartPostHandler(StateMassageHandler):
    async def handle(self):
        await SendMessage(chat_id=self.chat.id, text=_("Напишите ваш пост"))
        await self.state.set_state(PostingState.step)


@admin_router.message(PostingState.step)
class SendPostHandler(StateMassageHandler):
    async def handle(self):
        await self.state.clear()
        users = await get_users()
        for user in users:
            try:
                await CopyMessage(chat_id=user.id, from_chat_id=self.chat.id,
                                  message_id=self.event.message_id)
            except:
                ...
        await SendMessage(chat_id=self.chat.id,
                          text=_("Отправка поста закончена"))

