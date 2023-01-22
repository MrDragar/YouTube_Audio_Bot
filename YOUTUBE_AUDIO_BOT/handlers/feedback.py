from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from YOUTUBE_AUDIO_BOT.config import admins_id, bot
from YOUTUBE_AUDIO_BOT.states import FeedBackData
from YOUTUBE_AUDIO_BOT.config import _


async def set_feedback(message: Message):
    await message.answer(_("Напишите ваше сообщение разработчикам. Для отмены пропишите /cancel"))
    await FeedBackData.step_1.set()


async def send_feedback(message: Message, state: FSMContext):
    text = message.text
    for user_id in admins_id:
        await bot.send_message("@" + user_id, text + "\n От " + f"{message.from_user.username}"
                                                              f" {message.from_user.full_name}")
    await state.finish()
