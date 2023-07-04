from aiogram.dispatcher.router import Router

from .entry_point import entry_point_router


downloading_router = Router()

downloading_router.include_router(entry_point_router)