from typing import Optional

from .models import Media, MediaType


async def get_media(link_id: str, type: MediaType,
                    resolution: Optional[str]) -> Optional[Media]:
    media = await Media.get_or_none(link_id=link_id, type=type,
                                    resolution=resolution)
    return media


async def get_file_id(link_id: str, type: MediaType,
                      resolution: Optional[str]) -> Optional[str]:
    media = await Media.get_or_none(link_id=link_id, type=type,
                                    resolution=resolution)
    return media.file_id if media else None


async def create_media(link_id: str, type: MediaType,
                       resolution: Optional[str]) -> Media:
    media = await Media.create(link_id=link_id, type=type,
                               resolution=resolution)
    await media.save()
    return media
