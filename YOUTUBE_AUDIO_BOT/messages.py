from YOUTUBE_AUDIO_BOT.handlers.sendMedia import send_audio

languages = {
    "en": "English",
    "ru": "Русский"
}

wellcoming = {
    "en": "Hello. With this bot you can download any video or audio from YouTube." \
          "To do this, you need to give a link to this video. For all questions, write to yshhenyaev@mail.ru\n" \
          "To change the language, enter \n/language .",
    "ru": "Привет. С помощью этого бота ты можешь скачать любое видео или аудио с Ютуба." \
          "Для этого вам необходимо скинуть ссылку на этот ролик. По всем вопросам пишите на yshhenyaev@mail.ru\n" \
          "Для смены языка пропишите \n/language ."
}

cancellation = {
    "en": "cancellation",
    "ru": "Отмена"
}

choosing_language = {
    "en": """To change the language, select the desired language from the list""",
    "ru": """Для смены языка выберите из списка нужный язык"""
}

changing_language = {
    "en": "You have successfully changed your language to",
    "ru": "Вы успешно изменили свой язык на"
}

media_buttons = {
    "cancel": {
        "en": "Cancel",
        "ru": "Отмена"
    },
    "video": {
        "en": "Video",
        "ru": "Видео"
    },
    "audio": {
        "en": "Audio",
        "ru": "Аудио"
    }
}

choosing_media_type = {
    "en": "Select the file type",
    "ru": "Выберите тип файла"
}

video_resolution = {
    "error": {
        "en": "Some mistake has occurred. You may have given an incorrect link.",
        "ru": "Произошла какая-то ошибка. Возможно вы дали некорректную ссылку."
    },
    "success": {
        "en": "Select the video resolution",
        "ru": "Выберите разрешение видео"
    }
}

sending_audio = {
    "waiting": {
        "en": "Wait",
        "ru": "Подождите"
    },
    "error": {
        "en": "Some mistake has occurred. You may have given an incorrect link.",
        "ru": "Произошла какая-то ошибка. Возможно вы дали некорректную ссылку."
    }
}

sending_video = {
    "waiting": {
        "en": "Wait",
        "ru": "Подождите"
    },
    "error": {
        "en": "Sorry, something went wrong.",
        "ru": "Простите, что-то пошло не так."
    }
}

feedback = {
    "en": "Write your message to developers. For cancel write 'Cancel'.",
    "ru": "Напишите ваше сообщение разработчикам. Для отмены пропишите 'Отмена'."
}
