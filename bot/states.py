from aiogram.fsm.state import StatesGroup, State


class YoutubeState(StatesGroup):
    type = State()
    resolution = State()


class ChangingLanguageState(StatesGroup):
    step = State()


class FeedBackState(StatesGroup):
    step = State()


class PostingState(StatesGroup):
    step = State()
