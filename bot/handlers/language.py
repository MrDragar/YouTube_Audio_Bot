from aiogram.methods import SendMessage
from aiogram.utils.i18n import gettext as _
from aiogram.dispatcher.router import Router
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import Command

from bot.database.models import Language
from bot.states import ChangingLanguage
from .base_handlers import StateMassageHandler
from bot.database.user import change_language


language_router = Router()


@language_router.message(Command("language"))
class ShowLanguagesHandler(StateMassageHandler):
    async def handle(self):
        builder = ReplyKeyboardBuilder()
        for language in Language:
            builder.button(text=language.get_language_name())
        builder.button(text=_("Отмена"))
        await SendMessage(chat_id=self.chat.id, text=_("Выберите язык"),
                          reply_markup=builder.as_markup())
        await self.state.set_state(ChangingLanguage.step)


@language_router.message(ChangingLanguage.step)
class GetLanguageHandler(ShowLanguagesHandler):
    async def handle(self):
        language_code = Language.get_language_code(self.event.text)
        if not language_code:
            return
        await change_language(self.event.from_user.id, language_code)
        await SendMessage(chat_id=self.chat.id,
                          text=_("Вы успешно сменили язык"), reply_markup=None)
        await self.state.clear()
