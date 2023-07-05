from aiogram.dispatcher.router import Router

from .send_media import send_media_router


tiktok_router = Router()
tiktok_router.include_router(send_media_router)
