from aiogram.fsm.state import StatesGroup, State


class Youtube(StatesGroup):
    type = State()
    resolution = State()


class ChangingLanguage(StatesGroup):
    step = State()


class FeedBack(StatesGroup):
    step = State()


class Posting(StatesGroup):
    step = State()
