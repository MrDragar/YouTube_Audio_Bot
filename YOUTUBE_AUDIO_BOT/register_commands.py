from .handlers.common import *
from .handlers.mediaType import *
from .handlers.sendMedia import *
from .handlers.videoResolution import *
from .handlers.feedback import *
from .handlers.admin import *
from YOUTUBE_AUDIO_BOT.config import languages
from YOUTUBE_AUDIO_BOT.states import *

from aiogram.dispatcher.filters import Text


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
    dp.register_message_handler(cancel, Text(equals=["Отмена", "Cancel", "Скасування"]), state="*")
    dp.register_message_handler(cancel, commands=["Cancel", "cancel"], state="*")
    dp.register_message_handler(choose_language, commands=["language"])
    dp.register_message_handler(send_video_resolutions, Text(equals=["Видео", "Video", "Відео"]),
                                state=InputUserData.step_1,)
    dp.register_message_handler(send_video, state=InputUserData.step_2)
    dp.register_message_handler(send_audio, Text(equals=["Аудио", "Audio", "Аудіо"]), state=InputUserData.step_1)
    dp.register_message_handler(change_language, Text(equals=list(languages.values())),
                                state=LanguageUserData.step_1)
    dp.register_message_handler(set_feedback, commands=["send_feedback"])
    dp.register_message_handler(send_feedback, state=FeedBackData.step_1)
    dp.register_message_handler(set_post, is_admin=True, commands=["post"])
    dp.register_message_handler(send_post, state=PostingData.step_1)
    dp.register_message_handler(choose_media_type)


async def register_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("cancel", "Cancel your action"),
            types.BotCommand("send_feedback", "Callback to developers"),
            types.BotCommand("help", "Information about bot"),
            types.BotCommand("language", "Switch language")
        ]
    )
