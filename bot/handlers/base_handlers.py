from abc import ABC

from aiogram.handlers import MessageHandler, ErrorHandler, CallbackQueryHandler
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, error_event


class StateMassageHandler(MessageHandler, ABC):
    state: FSMContext
    event: Message

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = self.data["state"]


class StateCallbackQueryHandler(CallbackQueryHandler, ABC):
    state: FSMContext
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = self.data["state"]



class StateErrorHandler(ErrorHandler, ABC):
    state: FSMContext
    event: error_event.ErrorEvent

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = self.data["state"]
