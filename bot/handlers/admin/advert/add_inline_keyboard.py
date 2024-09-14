from typing import Any

from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.methods import SendMessage

from bot.handlers.base_handlers import StateMassageHandler
from bot.states import AddAdvertInlineKeyboardState
from bot.database.advert import create_keyboard, NoAdvertException

router = Router()


@router.message(Command("add_inline_keyboard_to_advert"))
class EntryPointHandler(StateMassageHandler):
    async def handle(self):
        await self.state.set_state(AddAdvertInlineKeyboardState.getting_advert_id)
        await self.bot(
            SendMessage(chat_id=self.chat.id, text="Напишите id рекламы")
        )


@router.message(AddAdvertInlineKeyboardState.getting_advert_id)
class GetIDHandler(StateMassageHandler):
    async def handle(self):
        if not self.event.text.isdigit():
            return await self.bot(
                SendMessage(
                    chat_id=self.chat.id,
                    text="Ты знаешь, что такое число?")
            )

        await self.state.update_data({"advert_id": int(self.event.text)})
        await self.state.set_state(AddAdvertInlineKeyboardState.getting_text)
        await self.bot(
            SendMessage(
                chat_id=self.chat.id, text="Напишите текст для новой кнопки"
            )
        )


@router.message(AddAdvertInlineKeyboardState.getting_text)
class GetTextHandler(StateMassageHandler):
    async def handle(self) -> Any:
        await self.state.update_data({"text": self.event.text})
        await self.state.set_state(AddAdvertInlineKeyboardState.getting_url)
        await self.bot(
            SendMessage(
                chat_id=self.chat.id, text="Напишите url для новой кнопки"
            )
        )


@router.message(AddAdvertInlineKeyboardState.getting_url)
class GetURLHandler(StateMassageHandler):
    async def handle(self):
        advert_id = (await self.state.get_data())["advert_id"]
        text = (await self.state.get_data())["text"]
        url = self.event.text.strip()
        await self.state.clear()

        try:
            kb_id = await create_keyboard(advert_id, text, url)
        except NoAdvertException:
            return await self.bot(
                SendMessage(chat_id=self.chat.id, text="Нет такой партии")
            )
        except Exception as e:
            raise

        return await self.bot(
            SendMessage(
                chat_id=self.chat.id, text=f"Для рекламы №{advert_id} была добавлена кнопка {kb_id}"
            )
        )
