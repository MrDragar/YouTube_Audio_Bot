from aiogram.dispatcher.router import Router

from .resolution import resolution_router
from .send_media import send_media_router


vk_router = Router()

vk_router.include_router(resolution_router)
vk_router.include_router(send_media_router)
