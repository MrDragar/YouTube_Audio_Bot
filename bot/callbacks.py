from aiogram.filters.callback_data import CallbackData


class FeedbackCallback(CallbackData, prefix="/feedback"):
    user_id: int
