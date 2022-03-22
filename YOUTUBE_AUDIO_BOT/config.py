from handlers.common import *
from handlers.mediaType import *
from handlers.sendMedia import *
from handlers.videoResolution import *


from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
    dp.register_message_handler(cancel, Text(equals="Отмена"), state=InputUserData.step_1)
    dp.register_message_handler(chooseMeiaType)
    dp.register_message_handler(send_video_resolutions, Text(equals="Видео"), state=InputUserData.step_1,)
    dp.register_message_handler(send_video, Text(equals=["144p", "360p", "720p", "1080p"]), state=InputUserData.step_2)
    dp.register_message_handler(send_audio, Text(equals="Аудио"), state=InputUserData.step_1)
