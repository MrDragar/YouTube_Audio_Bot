from aiogram.methods import SendMessage
from aiogram.utils.i18n import gettext as _
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove

from bot.database.models import Language
from bot.states import ChangingLanguageState
from .base_handlers import StateMassageHandler
from bot.database.user import change_language
from bot.keyboards import get_language_keyboard
from bot.commands import set_commands_for_user


language_router = Router()


@language_router.message(Command("language"))
class ShowLanguagesHandler(StateMassageHandler):
    async def handle(self):
        await SendMessage(chat_id=self.chat.id, text=_("Выберите язык"),
                          reply_markup=get_language_keyboard())
        await self.state.set_state(ChangingLanguageState.step)


@language_router.message(ChangingLanguageState.step)
class GetLanguageHandler(ShowLanguagesHandler):
    async def handle(self):
        language_code = Language.get_language_code(self.event.text)
        if not language_code:
            return
        await change_language(self.event.from_user.id, language_code)
        await SendMessage(chat_id=self.chat.id,
                          text=_("Вы успешно сменили язык",
                                 locale=language_code),
                          reply_markup=ReplyKeyboardRemove())
        await self.state.clear()
        await set_commands_for_user(language_code, self.from_user.id)


def useless_function_for_babel():
    """pybabel не видит использование lazy_gettext, поэтому тут продублирован
     текст для lazy_gettext"""
    _("отмена")
