from tortoise import fields
from tortoise.models import Model

from enum import Enum


class Language(str, Enum):
    RUSSIAN = "ru"
    ENGLISH = "en"
    UKRAINIAN = "uk"

    def get_language_name(self):
        """Возвращает название языка, соответствующее перечислению"""
        if not isinstance(self, Language):
            raise TypeError("Объект должен быть экземпляром класса")
        language_names = {
            self.RUSSIAN: "Русский",
            self.ENGLISH: "English",
            self.UKRAINIAN: "Українська"
        }
        return language_names.get(self, None)

    @classmethod
    def get_language_code(cls, language_name):
        """Возвращает объект enum по названию языка"""
        language_codes = {
            "Русский": cls.RUSSIAN,
            "English": cls.ENGLISH,
            "Українська": cls.UKRAINIAN
        }
        return language_codes.get(language_name, None)


class MediaType(str, Enum):
    VIDEO = "video"
    AUDIO = "audio"


class Platform(str, Enum):
    YOUTUBE = "youtube"
    VK = "vk"
    RUTUBE = "rutube"


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=180)
    language = fields.CharEnumField(Language)


class Media(Model):
    id = fields.IntField(pk=True)
    platform = fields.CharEnumField(Platform, default=Platform.YOUTUBE)
    link_id = fields.CharField(max_length=50)
    type = fields.CharEnumField(MediaType)
    resolution = fields.CharField(max_length=20, default=None, null=True)
    file_id = fields.TextField(default=None, null=True)
    file_unique_id = fields.TextField(default=None, null=True)


class DayStatistic(Model):
    date = fields.DateField(pk=True)
    new_users = fields.IntField(default=0)
    successful_requests = fields.IntField(default=0)
    unsuccessful_requests = fields.IntField(default=0)


class Advert(Model):
    id = fields.IntField(pk=True)
    chat_id = fields.IntField()
    message_id = fields.IntField()
    current_number = fields.IntField(default=0)
    total_number = fields.IntField(default=10)
    inline_keyboards: fields.ForeignKeyRelation["AdvertInlineKeyboard"]


class AdvertInlineKeyboard(Model):
    id = fields.IntField(pk=True)
    advert = fields.ForeignKeyField("models.Advert", related_name="inline_keyboards")
    text = fields.TextField()
    url = fields.TextField(null=True)