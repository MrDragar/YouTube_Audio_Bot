from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked, UserDeactivated

from YOUTUBE_AUDIO_BOT.database import get_all_id
from YOUTUBE_AUDIO_BOT.states import PostingData
from YOUTUBE_AUDIO_BOT.config import bot


async def set_post(message: Message):
    await message.answer("Напишите ваше сообщение.")
    await PostingData.step_1.set()


async def send_post(message: Message, state: FSMContext):
    users = get_all_id()
    for user_id in users:
        try:
            await bot.send_message(user_id, message.text)
        except BotBlocked:
            pass
        except UserDeactivated:
            pass

    await state.finish()

