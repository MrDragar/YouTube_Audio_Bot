from aiogram.dispatcher.router import Router

from .youtube import youtube_router
from .tiktok import tiktok_router
from .entry_point import entry_point_router
from .vk import vk_router
from .rutube import rutube_router


downloading_router = Router()

downloading_router.include_router(youtube_router)
downloading_router.include_router(tiktok_router)
downloading_router.include_router(vk_router)
downloading_router.include_router(rutube_router)

downloading_router.include_router(entry_point_router)
