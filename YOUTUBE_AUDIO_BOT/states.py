from aiogram.dispatcher.filters.state import State, StatesGroup


class InputUserData(StatesGroup):
    step_1 = State()
    step_2 = State()


class LanguageUserData(StatesGroup):
    step_1 = State()


class FeedBackData(StatesGroup):
    step_1 = State()


class PostingData(StatesGroup):
    step_1 = State()
