from aiogram.dispatcher.router import Router

from . import common
from . import language
from . import downloaders
from . import admin
from .feedback import feedback_router

root_router = Router()

root_router.include_router(common.common_router)
root_router.include_router(language.language_router)
root_router.include_router(admin.admin_router)
root_router.include_router(feedback_router)
root_router.include_router(downloaders.downloading_router)
