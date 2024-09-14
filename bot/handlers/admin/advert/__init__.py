from aiogram.dispatcher.router import Router

from . import new
from . import edit_text
from . import edit_total_number
from . import get
from . import add_inline_keyboard

advert_router = Router()

advert_router.include_router(new.new_router)
advert_router.include_router(edit_text.edit_text_router)
advert_router.include_router(edit_total_number.edit_total_number_router)
advert_router.include_router(get.get_router)
advert_router.include_router(add_inline_keyboard.router)
