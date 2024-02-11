from aiogram.methods import SendMessage, ForwardMessage, CopyMessage
from aiogram.dispatcher.router import Router
from aiogram.handlers.callback_query import CallbackQueryHandler
from aiogram.utils.i18n import gettext as _

from bot.handlers.base_handlers import (
    StateMassageHandler,
    StateCallbackQueryHandler
)
from bot.callbacks import FeedbackCallback
from bot.states import AnswerFeedbackState

feedback_router = Router()


@feedback_router.callback_query(FeedbackCallback.filter())
class AnswerPostHandler(StateCallbackQueryHandler):
    async def handle(self):
        await self.state.set_state(AnswerFeedbackState.step1)
        await SendMessage(
            chat_id=self.message.chat.id,
            text=_("Отправьте сообщение для ответа пользователю")
        )
        forwarded_chat_id = FeedbackCallback.unpack(self.callback_data)
        await self.state.update_data(chat_id=forwarded_chat_id.user_id)


@feedback_router.message(AnswerFeedbackState.step1)
class SendPostHandler(StateMassageHandler):
    async def handle(self):
        user_chat_id = (await self.state.get_data())["chat_id"]
        await self.state.clear()
        try:
            sent_massage = await SendMessage(
                chat_id=user_chat_id,
                text=_("Ответ админа:")
            )
            await CopyMessage(
                chat_id=user_chat_id,
                from_chat_id=self.chat.id,
                message_id=self.event.message_id,
                reply_to_message_id=sent_massage.message_id
            )
        except Exception:
            await SendMessage(
                chat_id=self.chat.id,
                text=_("Скорее всего, пользователь заблокировал бота")
            )
        else:
            await SendMessage(
                chat_id=self.chat.id,
                text=_("Ответ отправлен")
            )