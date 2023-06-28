from abc import ABC

from aiogram.handlers import MessageHandler
from aiogram.fsm.context import FSMContext


class StateMassageHandler(MessageHandler, ABC):
    state: FSMContext

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = self.data["state"]
