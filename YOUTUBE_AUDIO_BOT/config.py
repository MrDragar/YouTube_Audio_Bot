from .handlers.common import *
from .handlers.mediaType import *
from .handlers.sendMedia import *
from .handlers.videoResolution import *
from YOUTUBE_AUDIO_BOT import messages as msg

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
    dp.register_message_handler(cancel, Text(equals=["Отмена", "Cancel"]), state="*")
    dp.register_message_handler(choose_language, commands=["language"])
    dp.register_message_handler(chooseMeiaType)
    dp.register_message_handler(send_video_resolutions, Text(equals=["Видео", "Video"]), state=InputUserData.step_1,)
    dp.register_message_handler(send_video, Text(equals=["144p", "360p", "720p", "1080p"]), state=InputUserData.step_2)
    dp.register_message_handler(send_audio, Text(equals=["Аудио", "Audio"]), state=InputUserData.step_1)
    dp.register_message_handler(change_language, Text(equals=list(msg.languages.values())), state=LanguageUserData.step_1)