from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.methods import SendMessage

from bot.handlers.base_handlers import StateMassageHandler
from bot.states import EditAdvertTextState
from bot.database.advert import edit_advert_text
from bot.filters import IsAdmin


edit_text_router = Router()


@edit_text_router.message(Command("edit_advert_text"), IsAdmin())
class EditTextHandler(StateMassageHandler):
    async def handle(self):
        await self.state.set_state(EditAdvertTextState.step1)
        await SendMessage(chat_id=self.chat.id, text="Напишите id рекламы")


@edit_text_router.message(EditAdvertTextState.step1)
class GetIdHandler(StateMassageHandler):
    async def handle(self):
        if not self.event.text.isdigit():
            return SendMessage(chat_id=self.chat.id,
                               text="Ты знаешь, что такое число?")

        await self.state.update_data({"advert_id": int(self.event.text)})
        await self.state.set_state(EditAdvertTextState.step2)
        await SendMessage(chat_id=self.chat.id,
                          text="Напишите новый текст для рекламы")


@edit_text_router.message(EditAdvertTextState.step2)
class GetNewTextHandler(StateMassageHandler):
    async def handle(self):
        advert_id = (await self.state.get_data())["advert_id"]
        error = await edit_advert_text(advert_id=advert_id, chat_id=self.chat.id,
                                       message_id=self.event.message_id)
        await self.state.clear()
        if error:
            return SendMessage(chat_id=self.chat.id, text="Нет такой партии")
        return SendMessage(chat_id=self.chat.id,
                           text="Текст рекламы успешно обновлён")
