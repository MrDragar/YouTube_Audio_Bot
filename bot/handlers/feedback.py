from aiogram.methods import SendMessage, ForwardMessage, CopyMessage
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _

from .base_handlers import StateMassageHandler
from bot.states import FeedBackState
from bot.config import ADMINS_ID


feedback_router = Router()


@feedback_router.message(Command("send_feedback"))
class StartPostHandler(StateMassageHandler):
    async def handle(self):
        await SendMessage(chat_id=self.chat.id, text=_("Напишите ваш отзыв"))
        await self.state.set_state(FeedBackState.step)


@feedback_router.message(FeedBackState.step)
class SendPostHandler(StateMassageHandler):
    async def handle(self):
        await self.state.clear()
        for admin_id in ADMINS_ID:
            await ForwardMessage(chat_id=admin_id, from_chat_id=self.chat.id,
                                 message_id=self.event.message_id)
