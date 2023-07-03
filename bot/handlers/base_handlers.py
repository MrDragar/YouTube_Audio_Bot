from abc import ABC

from aiogram.handlers import MessageHandler
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class StateMassageHandler(MessageHandler, ABC):
    state: FSMContext
    event: Message

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = self.data["state"]
