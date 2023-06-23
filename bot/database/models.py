from tortoise import fields
from tortoise.models import Model

from enum import Enum


class Language(str, Enum):
    RUSSIAN = "ru"
    ENGLISH = "en"
    UKRAINIAN = "uk"


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    language = fields.CharEnumField(Language)


class Media(Model):
    id = fields.IntField(pk=True)
    link_id = fields.CharField(max_length=50)
    type = fields.CharField(max_length=10)
    resolution = fields.CharField(max_length=10)
