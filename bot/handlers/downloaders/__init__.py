from aiogram.dispatcher.router import Router

from .youtube import youtube_router
from .entry_point import entry_point_router


downloading_router = Router()

downloading_router.include_router(youtube_router)
downloading_router.include_router(entry_point_router)
