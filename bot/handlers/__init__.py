from aiogram.dispatcher.router import Router

from . import common

root_router = Router()

root_router.include_router(common.router)

