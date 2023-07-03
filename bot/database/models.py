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


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    language = fields.CharEnumField(Language)


class Media(Model):
    id = fields.IntField(pk=True)
    link_id = fields.CharField(max_length=50)
    type = fields.CharField(max_length=10)
    resolution = fields.CharField(max_length=10)
