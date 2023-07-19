from typing import Optional, List
from random import choice

from .models import Advert


async def create_advert(chat_id: int, message_id: int, total_number: int) -> int:
    advert = await Advert.create(chat_id=chat_id, message_id=message_id,
                                 total_number=total_number)
    await advert.save()
    return advert.id


async def get_advert_by_id(advert_id: int) -> Optional[Advert]:
    advert = await Advert.get_or_none(id=advert_id)
    return advert


async def get_all_adverts() -> List[Advert]:
    adverts = await Advert.all()
    return adverts


async def get_active_adverts() -> List[Advert]:
    all_adverts = await get_all_adverts()
    active_adverts = []
    for advert in all_adverts:
        if advert.total_number > advert.current_number:
            active_adverts.append(advert)
    return active_adverts


async def get_random_advert() -> Optional[Advert]:
    adverts = await get_active_adverts()
    if not adverts:
        return None
    return choice(adverts)


async def disable_advert(advert_id: int) -> int:
    """Возвращает 0 в случае успеха"""
    advert = await Advert.get_or_none(id=advert_id)
    if not advert:
        return 1
    advert.total_number = 0
    await advert.save()


async def edit_advert_text(advert_id: int, chat_id: int, message_id: int) -> int:
    """Возвращает 0 в случае успеха"""
    advert = await Advert.get_or_none(id=advert_id)
    if not advert:
        return 1
    advert.chat_id = chat_id
    advert.message_id = message_id
    await advert.save()


async def edit_advert_total_number(advert_id: int, total_number: int) -> int:
    """Возвращает 0 в случае успеха"""
    advert = await Advert.get_or_none(id=advert_id)
    if not advert:
        return 1
    advert.total_number = total_number
    await advert.save()


async def add_current_number_to_advert(advert_id: int) -> int:
    """Возвращает 1 в слуячае конца рекламы"""
    advert = await Advert.get(id=advert_id)
    advert.current_number = advert.current_number + 1
    await advert.save()
    return advert.total_number <= advert.current_number
