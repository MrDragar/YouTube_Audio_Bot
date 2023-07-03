from aiogram.dispatcher.router import Router

from . import common
from . import language

root_router = Router()

root_router.include_router(common.common_router)
root_router.include_router(language.language_router)
