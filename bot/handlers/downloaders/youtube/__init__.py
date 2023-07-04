from aiogram.dispatcher.router import Router

from .resolution import resolution_router
from .send_media import send_media_router

youtube_router = Router()

youtube_router.include_router(resolution_router)
youtube_router.include_router(send_media_router)
