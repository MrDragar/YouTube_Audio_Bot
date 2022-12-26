from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from YOUTUBE_AUDIO_BOT.config import admins_id, bot
from YOUTUBE_AUDIO_BOT.states import FeedBackData
from YOUTUBE_AUDIO_BOT import messages as msg


async def set_feedback(message: Message, language: str):
    await message.answer(msg.feedback[language])
    await FeedBackData.step_1.set()


async def send_feedback(message: Message, state: FSMContext):
    text = message.text
    for user_id in admins_id:
        await bot.send_message(user_id, text + "/n От " + message.from_user.url)
    await state.finish()
